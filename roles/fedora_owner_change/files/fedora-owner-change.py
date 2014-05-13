#!/usr/bin/python -tt
#-*- coding: utf-8 -*-

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
This program checks and reports the packages owner change in pkgdb using
its messages catched by datanommer and available via datagrepper.

Dependencies:
* python-requests
* python-argparse
"""

import argparse
import json
import logging
import requests
import smtplib
import sys

from email.mime.text import MIMEText


DATAGREPPER_URL = 'https://apps.fedoraproject.org/datagrepper/raw/'
DELTA = 7 * 24 * 60 * 60  # 7 days
TOPIC = 'org.fedoraproject.prod.pkgdb.owner.update'
EMAIL_TO = ''
EMAIL_FROM = ''
SMTP_SERVER = 'localhost'

# Initial simple logging stuff
logging.basicConfig()
LOG = logging.getLogger("owner-change")


def send_report(report):
    """ This function sends the actual report.
    :arg report: the content to send by email
    """
    report = report.encode('utf-8', 'replace')
    msg = MIMEText(report)
    msg['Subject'] = '[Owner-change] Fedora packages ownership change'
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    s = smtplib.SMTP(SMTP_SERVER)
    s.sendmail(EMAIL_FROM,
               EMAIL_TO,
               msg.as_string())
    s.quit()


def retrieve_pkgdb_change():
    """ Query datagrepper to retrieve the list of change in ownership
    on packages of pkgdb over the DELTA period of time.
    """
    messages = []
    page = 1
    pages = 2
    while page <= pages:
        LOG.debug('Retrieving page %s of %s' % (page, pages))
        data = {'delta': DELTA,
                'topic': [
                    'org.fedoraproject.prod.pkgdb.owner.update',
                    'org.fedoraproject.prod.pkgdb.package.retire',
                ],
                'rows_per_page': 100,
                'page': page,
                'order': 'asc',
                }
        output = requests.get(DATAGREPPER_URL, params=data)
        json_output = json.loads(output.text)
        pages = json_output['pages']
        page += 1
        messages.extend(json_output['raw_messages'])

    LOG.debug('Should have retrieved %s' % json_output['total'])
    return messages


def setup_parser():
    """
    Set the command line arguments.
    """
    parser = argparse.ArgumentParser(
        prog="fedora-owner-change")
    parser.add_argument(
        '--nomail', action='store_true',
        help="Prints the report instead of sending it by email")
    parser.add_argument(
        '--debug', action='store_true',
        help="Outputs debugging info")
    return parser


def __format_dict(dic):
    keys = dic.keys()
    pkgs = [it[0] for it in keys]
    tmp = {}
    for pkg in pkgs:
        lcl_keys = [key for key in keys if pkg in key]
        for key in lcl_keys:
            lcl = json.dumps(dic[key])
            if lcl in tmp:
                tmp[lcl].append(key)
            else:
                tmp[lcl] = [key]

    output = {}
    for key in tmp:
        pkg_name = tmp[key][0][0]
        branches = set([val[1] for val in tmp[key]])
        data = json.loads(key)
        data['pkg_name'] = pkg_name
        data['branches'] = ','.join(sorted(branches, key=unicode.lower))
        output[pkg_name] = data

    return output


def get_category(message):
    """ For a given message specify if it has been orphaned, retired,
    unorphaned, unretired, given or changed.
    """
    output = None
    if 'retirement' in message \
            and message['retirement'] == 'retired':
        output = 'retired'
    elif 'retirement' in message \
            and message['retirement'] == 'unretired':
        output = 'unretired'
    elif 'previous_owner' in message \
            and message['package_listing']['owner'] == 'orphan':
        output = 'orphaned'
    elif 'previous_owner' in message \
            and message['package_listing']['owner'] != 'orphan' \
            and message['previous_owner'] == 'orphan':
        output = 'unorphaned'
    elif 'previous_owner' in message \
            and message['package_listing']['owner'] == message['previous_owner'] \
            and message['previous_owner'] != 'orphan':
        output = 'new'
    elif 'previous_owner' in message \
            and message['package_listing']['owner'] != message['previous_owner'] \
            and message['previous_owner'] != 'orphan':
        output = 'given'
    else:
        LOG.info('Could not parse message %s', message)

    return output


def main():
    """ Retrieve all the change in ownership from pkgdb via datagrepper
    and report the changes either as packages have been orphaned or
    packages changed owner.
    """
    parser = setup_parser()
    args = parser.parse_args()

    global LOG
    if args.debug:
        LOG.setLevel(logging.DEBUG)

    changes = retrieve_pkgdb_change()
    LOG.debug('%s changes retrieved' % len(changes))
    packages = {}
    for change in changes:
        pkg_name = change['msg']['package_listing']['package']['name']
        owner = change['msg']['package_listing']['owner']
        branch = change['msg']['package_listing']['collection']['branchname']
        user = change['msg']['agent']
        LOG.debug('"%s" changed to %s by %s on %s - topic: %s' % (
                  pkg_name, owner, user, branch, change['topic']))

        key = (pkg_name, branch)
        if key not in packages:
            packages[key] = {}
        packages[key]['action'] = get_category(change['msg'])
        packages[key]['msg'] = change['msg']

    actions = {}
    for act in ['orphaned', 'unorphaned', 'retired', 'unretired', 'given',
                'new']:
        actions[act] = {}

    for package in sorted(packages) :
        action = packages[package]['action']
        if package[0] not in actions[action]:
            actions[action][package[0]] = {}
        actions[action][package[0]][package[1]] = packages[package]

    hours = int(DELTA) / 3600
    report = 'Change in package status over the last %s hours\n' % hours
    report += '=' * (45 + len(str(hours))) + '\n'

    report += '\n%s packages were orphaned\n' % len(actions['orphaned'])
    report += '-' * (len(str(len(actions['orphaned']))) + 23) + '\n'
    for pkg in sorted(actions['orphaned']):
        branches = [item for item in actions['orphaned'][pkg]]
        agents = set([
            actions['orphaned'][pkg][item]['msg']['agent']
            for item in actions['orphaned'][pkg]])
        value = u'%s [%s] was orphaned by %s' % (
            pkg,
            ', '.join(branches),
            ', '.join(agents)
        )
        report += value + '\n'
        report += ' ' * 5 + actions['orphaned'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n%s packages unorphaned\n' % len(actions['unorphaned'])
    report += '-' * (len(str(len(actions['unorphaned']))) + 20) + '\n'
    for pkg in sorted(actions['unorphaned']):
        branches = [item for item in actions['unorphaned'][pkg]]
        agents = set([
            actions['unorphaned'][pkg][item]['msg']['agent']
            for item in actions['unorphaned'][pkg]])
        value = u'%s [%s] was unorphaned by %s' % (
            pkg,
            ', '.join(branches),
            ', '.join(agents)
        )
        report += value + '\n'
        report += ' ' * 5 + actions['unorphaned'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n%s packages were retired\n' % len(actions['retired'])
    report += '-' * (len(str(len(actions['retired']))) + 23) + '\n'
    for pkg in sorted(actions['retired']):
        branches = [item for item in actions['retired'][pkg]]
        agents = set([
            actions['retired'][pkg][item]['msg']['agent']
            for item in actions['retired'][pkg]])
        value = u'%s [%s] was retired by %s' % (
            pkg,
            ', '.join(branches),
            ', '.join(agents)
        )
        report += value + '\n'
        report += ' ' * 5 + actions['retired'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n%s packages were unretired\n' % len(actions['unretired'])
    report += '-' * (len(str(len(actions['unretired']))) + 23) + '\n'
    for pkg in sorted(actions['unretired']):
        branches = [item for item in actions['unretired'][pkg]]
        agents = set([
            actions['unretired'][pkg][item]['msg']['agent']
            for item in actions['unretired'][pkg]])
        value = u'%s [%s] was unretired by %s' % (
            pkg,
            ', '.join(branches),
            ', '.join(agents)
        )
        report += value + '\n'
        report += ' ' * 5 + actions['unretired'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n%s packages were given\n' % len(actions['given'])
    report += '-' * (len(str(len(actions['given']))) + 23) + '\n'
    for pkg in sorted(actions['given']):
        branches = [item for item in actions['given'][pkg]]
        agents = set([
            actions['given'][pkg][item]['msg']['agent']
            for item in actions['given'][pkg]])
        owners = set([
            actions['given'][pkg][item]['msg']['package_listing']['owner']
            for item in actions['given'][pkg]])
        value = u'%s [%s] was given by %s to %s' % (
            pkg,
            ', '.join(branches),
            ', '.join(agents),
            ', '.join(owners)
        )
        report += value + '\n'
        report += ' ' * 5 + actions['given'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n%s packages had new branches\n' % len(actions['new'])
    report += '-' * (len(str(len(actions['new']))) + 23) + '\n'
    for pkg in sorted(actions['new']):
        branches = [item for item in actions['new'][pkg]]
        agents = set([
            actions['new'][pkg][item]['msg']['agent']
            for item in actions['new'][pkg]])
        owners = set([
            actions['new'][pkg][item]['msg']['package_listing']['owner']
            for item in actions['new'][pkg]])

        if len(branches) == 1:
            branch = ': %s' % branches[0]
        else:
            branch = 'es: %s' % ', '.join(branches)

        value = u'%s had a new branch%s for %s by %s' % (
            pkg,
            branch,
            ', '.join(owners),
            ', '.join(agents),
        )
        report += value + '\n'
        report += ' ' * 5 + actions['new'][pkg][branches[0]]['msg'][
            'package_listing']['package']['summary'] + '\n'
        report += ' ' * 5 + 'https://admin.fedoraproject.org/pkgdb/'\
            'acls/name/%s\n' % pkg

    report += '\n\nSources: https://github.com/pypingou/fedora-owner-change'

    if args.nomail:
        print report
    else:
        send_report(report)


if __name__ == '__main__':
    import sys
    sys.exit(main())
