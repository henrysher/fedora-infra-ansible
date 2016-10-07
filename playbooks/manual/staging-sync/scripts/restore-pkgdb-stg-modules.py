#!/usr/bin/env python
""" Restore modules/ pkgdb entries in staging.

Use this script to restore pkgdb entries in staging after having wiped that db.

The workflow usually goes:

- Run the `export-pkgdb-stg-modules.py` script.  This will save the modules and
  their acls out to a local `old-modules.json` file.
- Run the `playbooks/manual/staging-sync/db-sync.yml` playbook.  This will nuke
  the staging pkgdb db and replace it with a copy of the current production
  pkgdb db.
- Run this `restore-pkgdb-stg-modules.py` script.  It will read in that
  `old-modules.json` script and then recreate those entries in the new fresh
  staging db.

"""

import json

import pkgdb2client

client = pkgdb2client.PkgDB(
    'https://admin.stg.fedoraproject.org/pkgdb',
    login_callback=pkgdb2client.ask_password,
)

with open('old-modules.json', 'rb') as f:
    data = json.loads(f.read().decode('utf-8'))

for package in data['packages']:
    print "Handling %s/%s" % (package['namespace'], package['name'])
    client.create_package(
        pkgname=package['name'],
        summary=package['summary'],
        description=package['description'],
        review_url=package['review_url'],
        status=package['status'],
        shouldopen='whatever',  # unused..
        branches='master',
        poc=package['acls'][0]['point_of_contact'],
        upstream_url=package['upstream_url'],
        namespace=package['namespace'],
        critpath=False,
        #monitoring_status=False,
        #koschei=False
    )
    users = set([i['fas_name'] for i in package['acls'][0]['acls']])
    for user in users:
        print "  Granting all to %r" % user
        client.update_acl(
            pkgname=package['name'],
            namespace=package['namespace'],
            branches='master',
            acls=['watchcommits', 'watchbugzilla', 'approveacls', 'commit'],
            status='Approved',
            user=user,
        )


