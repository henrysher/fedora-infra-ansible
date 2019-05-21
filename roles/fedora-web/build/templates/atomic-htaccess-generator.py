#!/usr/bin/python
""" Return the results of the atomic release engine from datagrepper.

For the Two-Week Atomic Change (F23)

Deps:  $ sudo dnf install python-requests

Author:     Ralph Bean <rbean@redhat.com>
License:    LGPLv2+
"""

from __future__ import print_function

import collections
import functools
import json
import logging
import os
import sys
import socket

from datetime import datetime, timedelta

import dateutil.relativedelta
import dateutil.tz
import dogpile.cache
import requests

log = logging.getLogger("atomic_vars")

base_url = 'https://apps.fedoraproject.org/datagrepper/raw'
topic = "org.fedoraproject.prod.releng.atomic.twoweek.complete"

UTC = dateutil.tz.tzutc()

session = requests.session()

cache = dogpile.cache.make_region().configure(
    "dogpile.cache.dbm",
    # 'make clean' does not remove this cache, but we let the values expire
    # once every this many seconds (once a day)
    expiration_time=86400,
    arguments={
        "filename": os.path.join(os.getcwd(), 'build/atomic.cache')
    },
)

# Are we running in fedora-infra or on someone's laptop?
hostname = socket.gethostname()
if '.phx2.fedoraproject.org' in hostname:
    DL_URL_PREFIX = 'http://dl.phx2.fedoraproject.org'
else:
    DL_URL_PREFIX = 'https://dl.fedoraproject.org'

download_fpo = 'https://download.fedoraproject.org'


def get_page(page, pages):
    """ Retrieve the JSON for a particular page of datagrepper results """
    log.debug("Getting page %i of %s", page, pages)
    params = dict(
        delta=2419200, # 4 weeks in seconds
        topic=topic,
        page=page,
        rows_per_page=1,
    )
    response = session.get(base_url, params=params)
    if not bool(response):
        raise IOError("Failed to talk to %r %r" % (response.url, response))
    return response.json()


# A list of fedmsg messages ideas that were produced erroneously.
# We don't want to use them, so ban them from our results.
blacklist = [
    '2016-dd05c4b7-958b-439f-90d6-e5ca0af2197c',
    '2016-b2a2eb00-acef-4a1f-bc6a-ad5aa9d81eee',
    '2016-0307f681-1eae-4aeb-9126-8a43b7a378e2',
]

def get_messages(target):
    """ Generator that yields messages from datagrepper """

    # Get the first page
    data = get_page(1, 'unknown')
    for message in data['raw_messages']:
        if message['msg_id'] in blacklist:
            continue
        if target in json.dumps(message):
            yield message

    more = functools.partial(get_page, pages=data['pages'])

    # Get all subsequent pages (if there are any...)
    for page in range(1, data['pages']):
        data = more(page + 1)

        for message in data['raw_messages']:
            if message['msg_id'] in blacklist:
                continue
            if target in json.dumps(message):
                yield message


def make_templates(curr_atomic_id, next_atomic_id):
    return [
        # As things stand now, we only do two-week-atomic stuff for the current
        # stable release.
        (curr_atomic_id, '', ''),

        # If we ever move to doing pre-release versions as well, just uncomment
        # the following line and it should all work. We leave it commented out
        # now because querying datagrepper for pre-release results that are not
        # there is much more slow than querying for something that exists.
        #(next_atomic_id, 'pre_atomic_', 'pre_'),
    ]


# We cache this guy on disk so we don't hit datagrepper over and over.
@cache.cache_on_arguments()
def collect(curr_atomic_id, next_atomic_id):
    results = collections.defaultdict(dict)

    # This is the information needed to provide "latest" download targets that
    # redirect to the actual mirrormanager url via htpasswd file
    results['release']['redir_map'] = collections.defaultdict(dict)

    for idx, composedate_prefix, iso_size_prefix in make_templates(curr_atomic_id, next_atomic_id):

        log.info("Looking for latest atomic release for %s" % idx)
        # Get the *latest* atomic release information.
        messages = get_messages('-%s-' % idx)
        try:
            message = messages.next()
        except StopIteration:
            log.warn("Couldn't find any two-week-atomic content for %r" % idx)
            continue

        # Parse the composedate out of the image_name
        image_name = message['msg']['x86_64']['atomic_qcow2']['image_name']
        composedate = '.'.join(image_name.split('-')[-1].split('.')[:-2])
        log.info("    Found composedate: %s" % composedate)
        results['release'][composedate_prefix + 'atomic_composedate'] = composedate

        # Save the timestamp so we can compute the age later, off-cache.
        results['release'][composedate_prefix + 'atomic_ts'] = message['timestamp']

        # Get the sizes of the isos in megabytes.  To do this, we need...
        # A mapping between what the release-engine tool calls each artifact,
        # and what we call them.
        mapping = {
            'atomic_qcow2': 'atomic_qcow2_cloud',
            'atomic_raw': 'atomic_raw_cloud',
            'atomic_vagrant_libvirt': 'atomic_libvag_cloud',
            'atomic_vagrant_virtualbox': 'atomic_VBvag_cloud',
            'atomic_dvd_ostree': 'atomic_dvd_iso',
        }

        for arch, items in message['msg'].items():       
            for key, entry in items.items():
                # There are some other keys in there we don't care about.
                if not key.startswith('atomic_'):
                    continue

                url = entry['image_url']
                download_url = entry['image_url']
                if not url.startswith('http'):
                    url = DL_URL_PREFIX + url
                    download_url = download_fpo + entry['image_url']

                length = int(entry['size']) / (1024 * 1024)
                # Provide the download URL
                url_key = mapping[key] + "_url"
                results['release'][url_key] = download_url

                # Provide the redirect rule mapping
                img_filename = download_url.split('/')[-1]
                results['release']['redir_map'][key+'_'+arch] = {}
                results['release']['redir_map'][key+'_'+arch]['redirect'] = download_url
                results['release']['redir_map'][key+'_'+arch]['filename'] = img_filename
                results['release']['redir_map'][key+'_'+arch]['iso_size'] = str(length)

                # Figure out which of our vars we're going to set, and set it
                iso_size_key = iso_size_prefix + mapping[key]
                results['iso_size'][iso_size_key] = str(length)
            results['release']['redir_map']['atomic_images_checksum_' + arch] = {}
            results['release']['redir_map']['atomic_images_checksum_' + arch]['redirect']=\
                download_fpo + '/pub/alt/atomic/stable/Fedora-Atomic-' + idx + '-' + composedate +\
                '/AtomicHost/' + arch + '/images/Fedora-AtomicHost-' + idx + '-' + composedate + '-' + arch + '-CHECKSUM'
            results['release']['redir_map']['atomic_images_checksum_' + arch]['filename'] = \
                'Fedora-AtomicHost-' + idx + '-' + composedate + '-' + arch + '-CHECKSUM'

            results['release']['redir_map']['atomic_dvd_ostree_checksum_' + arch] = {}
            results['release']['redir_map']['atomic_dvd_ostree_checksum_' + arch]['redirect'] = \
                download_fpo + '/pub/alt/atomic/stable/Fedora-Atomic-' + idx + '-' + composedate + \
                '/AtomicHost/' + arch + '/iso/Fedora-AtomicHost-' + idx + '-' + composedate + '-' + arch + '-CHECKSUM'
            results['release']['redir_map']['atomic_dvd_ostree_checksum_' + arch]['filename'] = \
                'Fedora-AtomicHost-' + idx + '-' + composedate + '-' + arch + '-CHECKSUM'

    return results


# Note, this is *not* cached, since we need to update it frequently.
def update_age(release):
    """ Is it old and stale?

    We aim to produce new atomic releases every two weeks at minimum.  If we're
    older than two weeks, we should put up a warning on the websites.  Here we
    just compute a flag that gets checked in the template.  If this latest
    release if younger than two weeks, call it "fresh".  If it is older than
    two weeks, it is no longer fresh.
    http://taiga.cloud.fedoraproject.org/project/acarter-fedora-docker-atomic-tooling/us/31
    """

    results = collections.defaultdict(dict)
    templates = make_templates(release['curr_atomic_id'], release['next_atomic_id'])
    for idx, composedate_prefix, iso_size_prefix in templates:
        two_weeks_ago = datetime.now(UTC) - timedelta(days=14)
        timestamp = release[composedate_prefix + 'atomic_ts']
        latest = datetime.fromtimestamp(timestamp, UTC)
        freshness = bool(latest >= two_weeks_ago)
        relative_delta = datetime.now(UTC) - latest
        casual_delta = relative_delta.days
        results['release'][composedate_prefix + 'atomic_freshness'] = freshness
        results['release'][composedate_prefix + 'atomic_age'] = casual_delta
    return results

# Go get two-week-atomic release info from datagrepper
collected_atomic_vars = collect(
    '29',
    '31'
)

# Write htaccess rewrite and informational files for 'latest'
with open(os.path.join("out", ".htaccess"), 'w') as htaccess_f:
    for artifact in collected_atomic_vars['release']['redir_map']:
        htaccess_f.write('Redirect 302 "/{}_latest" "{}"\n'.format(
            artifact,
            collected_atomic_vars['release']['redir_map'][artifact]['redirect']
            )
        )
# Write a file that returns the artifact name that corresponds to
# the current 'latest' (for scripting purposes).
for artifact in collected_atomic_vars['release']['redir_map']:
    with open(os.path.join("out", "{}_latest_filename".format(artifact)), 'w') as artifact_f:
        artifact_f.write(
            collected_atomic_vars['release']['redir_map'][artifact]['filename']
        )
# Maintain legacy atomic latest urls for existing users
artifacts_redirect = ['atomic_qcow2', 'atomic_raw', 'atomic_vagrant_libvirt',
                      'atomic_vagrant_virtualbox', 'atomic_iso']
with open(os.path.join("out", ".htaccess"), 'a') as htaccess_f:
    for artifact in artifacts_redirect:
        if artifact is 'atomic_iso':
            htaccess_f.write('Redirect 302 "/{}_latest"'
                             ' "/atomic_dvd_ostree_x86_64_latest"\n'.format(artifact))
            htaccess_f.write('Redirect 302 "/{}_latest_filename"'
                             ' "/atomic_dvd_ostree_x86_64_latest_filename"\n'.format( artifact))
        else:
            htaccess_f.write('Redirect 302 "/{}_latest" "/{}_x86_64_latest"\n'.format(
                artifact, artifact))
            htaccess_f.write('Redirect 302 "/{}_latest_filename" "/{}_x86_64_latest_filename"\n'.format(
                artifact, artifact))
