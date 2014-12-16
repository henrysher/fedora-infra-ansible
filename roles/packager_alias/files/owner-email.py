#!/usr/bin/python -tt

"""
This script is ran as a cronjob and bastion.

Its goal is to generate all the <pkg>-owner email aliases we provide
"""

import os
import sys
import urllib2
from fedora.client import BaseClient, ServerError, AuthError
import ConfigParser
import requests

config = ConfigParser.ConfigParser()
config.read('/etc/fas.conf')


pkgdb_url = 'https://admin.fedoraproject.org/pkgdb'
fas = BaseClient('https://admin.fedoraproject.org/accounts',
    username=config.get('global', 'login').strip('"'),
    password=config.get('global', 'password').strip('"'))

try:
    pkgdb_data = requests.get('%s/api/notify/?format=json' % pkgdb_url,
        verify=False).json()
    fas_data = fas.send_request('/user/email_list', auth=True)
    fas_groups = fas.send_request(
        '/group/type_list', auth=True, req_params={'grptype': 'pkgdb'})
except ServerError, e:
    print >> sys.stderr, '%s' % e
    sys.exit(1)
except AuthError, e:
    print >> sys.stderr, '%s: %s' % (e.exc, e.message)
    sys.exit(1)
except (urllib2.HTTPError,urllib2.URLError), e:
    print >> sys.stderr, '%s' % e
    sys.exit(1)

else:
    pkgs = pkgdb_data['packages']
    if len(pkgs) < 500:
        print >> sys.stderr, 'Too few packages, something is wrong'
        sys.exit(1)
    email_list = fas_data['emails']
    group_mail = {}
    for group in fas_groups.groups:
        group_mail[group.name] = group.mailing_list

    contactlist = {}
    for pkg, ccusers in pkgs.iteritems():
        emails = []
        for user in ccusers:
            if user in email_list:
                emails.append(email_list[user])
            elif user.startswith('group::'):
                user = user.replace('group::', '')
                if user in group_mail and group_mail[user]:
                    emails.append(group_mail[user])
                else:
                    print >> sys.stderr, 'Strange user `%s`, not in '\
                        'email_list nor in group_mail, badly set-up '\
                        'group?\n' % user
            else:
                print >> sys.stderr, 'Strange user `%s`, not in '\
                    'email_list and not a group\n' % user

        if pkg.lower() in contactlist:
            contactlist[pkg.lower()] = contactlist[pkg.lower()].union(emails)
        else:
            contactlist[pkg.lower()] = set(emails)

    for pkg, emails in sorted(contactlist.iteritems()):
        print '%s-owner: %s' % (pkg.lower(),','.join(sorted(emails)))

    for group in fas_groups.groups:
        print '{0}: {1}'.format(group.name, group.mailing_list)
        
