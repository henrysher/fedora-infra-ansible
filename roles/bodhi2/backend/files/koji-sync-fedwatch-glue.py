#!/usr/bin/env python
""" This is a glue script to run /usr/local/bin/owner-sync-pagure on a given
package anytime a ticket gets closed at
https://pagure.io/releng/fedora-scm-requests

Author: Ralph Bean <rbean@redhat.com>
"""

import json
import subprocess as sp
import sys


def handle(content):
    body = content.strip('`').strip()
    body = json.loads(body)
    package = body['repo']
    # XXX If you modify this taglist.  Please also modify the other copy in
    # bodhi2/backend/tasks/main.yml
    taglist = 'f27 f26 f25 f27-container f26-container f25-container epel7 dist-6E-epel module-package-list'
    cmd = [
        '/usr/local/bin/owner-sync-pagure',
        '--package', package,
        '--verbose',
    ] + taglist.split()
    sp.Popen(cmd)


def main(fullname, fields, content):
    if fullname != 'releng/fedora-scm-requests':
        print("Dropping %r.  Not scm request.")
        return False
    if 'close_status' not in fields:
        print("Dropping %r.  Not closed.")
        return False

    handle(content)


if __name__ == '__main__':
    topic = sys.argv[-1]
    if topic != 'io.pagure.prod.pagure.issue.edit':
        # This message wasn't meant for me...
        sys.exit(0)
    fullname, fields, content = sys.argv[-4:-1]
    main(fullname, fields, content)
