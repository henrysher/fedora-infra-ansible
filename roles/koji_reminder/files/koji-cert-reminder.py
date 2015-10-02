#!/usr/bin/env python
""" Send emails to Fedora users whose koji certs are about to expire.

We first get a list of Fedora users in the cla_done group.  Then we query
datagrepper for the history of when each user last changed their cert.  If that
event occurred inside a window (between 5.75 months ago and 6 months ago), then
send them an email letting them know their cert is about to expire.

Requires:   python-arrow python-fedora python-requests fedmsg
License:    LGPLv2+
Authors:    Ralph Bean <rbean@redhat.com>
"""

import arrow
import datetime
import email
import fedmsg
import fedora.client.fas2
import getpass
import smtplib
import requests
import operator
import sys

# This is a flag used to turn off email to the actual users
DEVELOPMENT = False

datagrepper_url = 'https://apps.fedoraproject.org/datagrepper/raw'

from_address = 'admin@fedoraproject.org'
mail_server = 'bastion.phx2.fedoraproject.org'
message_template = u"""{human_name}/{username}:

This is an automated email sent to inform you that your Fedora Project Koji
certificate is about to expire.  Koji certificates are valid for 6 months and
our records indicate that you last recreated yours about {change_human}
on {change_date}.

Please run the following command to regenerate your certificate:

    $ /usr/bin/fedora-cert -n

For more information, see the following wiki page:
https://fedoraproject.org/wiki/Using_the_Koji_build_system#Fedora_Certificates
"""

# We want to alert users if their cert is going to expire this week.
now = arrow.utcnow()
six_months = 1.57785e7
one_week = 604800

window_delta = one_week
window_max = six_months
window_min = window_max - window_delta
start = now.timestamp - window_max

# Use a requests session to minimize tcp setup/teardown.
session = requests.session()

def cert_changes(user):
    """ Generator that returns all the koji cert changes for a user.

    >>> user = 'ralph'
    >>> for change in cert_changes(user):
    ...     print change.humanize(), "on", change.format('YYYY-MM-DD')
    21 hours ago on 2014-04-08
    2 months ago on 2014-02-09
    8 months ago on 2013-08-12

    """

    def get_page(page):
        params = dict(
            rows_per_page=100,
            topic='org.fedoraproject.prod.fas.user.update',
            user=user,
            page=page,
            start=start,
        )
        return session.get(datagrepper_url, params=params).json()

    data = get_page(1)
    pages = data['pages']

    for page in range(1, pages + 1):
        data = get_page(page)
        for message in data['raw_messages']:
            if 'certificate' in message['msg']['fields']:
                yield arrow.get(message['timestamp'])


def test_cert_changes():
    """ Just messing around... """
    for user in ['kevin', 'ralph', 'lmacken', 'pingou']:
        for change in cert_changes(user):
            print user, change.humanize(), "on", change.format('YYYY-MM-DD')


def fedora_users(credentials):
    return fedora.client.fas2.AccountSystem(
        username=credentials['username'],
        password=credentials['password'],
    ).people_by_groupname('cla_done')


def total_seconds(td):
    """ Take a datetime.timedelta object and return the total seconds.

    td.total_seconds() exists in the python 2.7 stdlib, but not in python 2.6.
    """
    return td.days * 24 * 60 * 60 + td.seconds + td.microseconds / 1000000.0


def to_address(user):
    if DEVELOPMENT:
        return 'ralph@fedoraproject.org'
    else:
        return user['email']


def send_email(user, last_change):
    print "send an email to %r since they last changed on %r" % (
        user, last_change.format('YYYY-MM-DD'))
    sys.stdout.flush()

    message = email.Message.Message()
    message.add_header('To', to_address(user))
    message.add_header('From', from_address)
    subject = 'Your Koji certificate expires within a week'
    message.add_header('Subject', subject)

    content = message_template.format(
        change_human=last_change.humanize(),
        change_date=last_change.format('YYYY-MM-DD'),
        **user
    )
    message.set_payload(content.encode('utf-8'))

    server = smtplib.SMTP(mail_server)
    server.sendmail(
        from_address.encode('utf-8'),
        [to_address(user).encode('utf-8')],
        message.as_string().encode('utf-8'),
    )
    server.quit()


def main(credentials):
    print "* Querying FAS for a list of users"
    sys.stdout.flush()
    users = fedora_users(credentials)
    print "* Found %r people" % len(users)
    sys.stdout.flush()
    for user in sorted(users, key=operator.itemgetter('username')):
        #print "* Querying datagrepper for %r." % user['username'],
        #sys.stdout.flush()
        changes = cert_changes(user['username'])

        try:
            latest = changes.next()
        except StopIteration:
            # Then the user has no changes in the fedmsg history.
            #print "No record of %r changing a cert." % user['username']
            #sys.stdout.flush()
            continue

        print user['username'], "changed", latest.humanize(),
        print "on", latest.format('YYYY-MM-DD')
        sys.stdout.flush()

        delta = total_seconds(now - latest)
        if delta >= window_min and delta <= window_max:
            send_email(user, latest)


if __name__ == '__main__':
    # Load credentials from /etc/fedmsg.d/
    config = fedmsg.config.load_config()

    if 'fas_credentials' not in config:
        print "No 'fas_credentials' found in `fedmsg-config`..."
        sys.stdout.flush()
        username = raw_input("Enter your fas username: ")
        password = getpass.getpass("Enter your fas password: ")
        config['fas_credentials'] = dict(username=username, password=password)

    main(config['fas_credentials'])
