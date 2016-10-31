#!/usr/bin/env python
""" Create modules/ pkgdb entries in staging.

"""

import argparse
import sys

import pkgdb2client

parser = argparse.ArgumentParser(description='Create new modules in stg pkgdb')
parser.add_argument('--users',
                    help='A comma separated list of users '
                    'to get acls on the new modules.')
parser.add_argument('--modules',
                    help='A comma separated list of module '
                    'names to be created in staging.')
args = parser.parse_args()
users = [user.strip() for user in args.users.split(',')]
modules = [module.strip() for module in args.modules.split(',')]


print "%r will get full ACLs on new modules %r" % (users, modules)
response = raw_input("Does that look correct?  [y/N]")
if response.lower() != 'y':
    print "Exiting."
    sys.exit(0)
else:
    print "Ok."


client = pkgdb2client.PkgDB(
    'https://admin.stg.fedoraproject.org/pkgdb',
    login_callback=pkgdb2client.ask_password,
)

modules = [ {
    'name': name,
    'summary': 'The %s module' % name,
    'description': 'This is a test entry for modularity development.',
    'review_url': 'https://fedoraproject.org/wiki/Modularity',
    'upstream_url': 'https://fedoraproject.org/wiki/Modularity',
    'status': 'Approved',
    'namespace': 'modules',
} for name in modules]


for module in modules:
    print "Handling %s/%s" % (module['namespace'], module['name'])
    client.create_package(
        pkgname=module['name'],
        summary=module['summary'],
        description=module['description'],
        review_url=module['review_url'],
        status=module['status'],
        shouldopen='whatever',  # unused..
        branches='master',
        poc=users[0],
        upstream_url=module['upstream_url'],
        namespace=module['namespace'],
        critpath=False,
        #monitoring_status=False,
        #koschei=False
    )
    for user in users:
        print "  Granting all to %r" % user
        client.update_acl(
            pkgname=module['name'],
            namespace=module['namespace'],
            branches='master',
            acls=['watchcommits', 'watchbugzilla', 'approveacls', 'commit'],
            status='Approved',
            user=user,
        )
