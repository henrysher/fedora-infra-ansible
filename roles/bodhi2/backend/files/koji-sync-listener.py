#!/usr/bin/env python
""" This is a glue script to run /usr/local/bin/owner-sync-pagure on a given
package anytime a ticket gets closed at
https://pagure.io/releng/fedora-scm-requests

Author: Ralph Bean <rbean@redhat.com>
"""

import json
import logging.config
import subprocess as sp
import sys

import fedmsg


def handle(content):
    body = content.strip('`').strip()
    body = json.loads(body)
    package = body['repo']
    # XXX If you modify this taglist.  Please also modify the other copy in
    # bodhi2/backend/tasks/main.yml
    taglist = 'f28 f27 f26 f25 f28-container f27-container f26-container f25-container f28-docker f27-docker f26-docker f25-docker epel7 dist-6E-epel module-package-list'
    cmd = [
        '/usr/local/bin/owner-sync-pagure',
        '--package', package,
        '--verbose',
    ] + taglist.split()
    print("Running %r" % cmd)
    proc = sp.Popen(cmd)
    status = proc.wait()
    if status:
        raise RuntimeError("%r gave return code %r" % (cmd, status))


def main(fullname, fields, content):
    if fullname != 'releng/fedora-scm-requests':
        print("Dropping %r.  Not scm request." % fullname)
        return False
    if 'close_status' not in fields:
        print("Dropping %r %r.  Not closed." % (fullname, fields))
        return False

    handle(content)


if __name__ == '__main__':
    config = fedmsg.config.load_config()
    logging.config.dictConfig(config['logging'])
    topic = 'io.pagure.prod.pagure.issue.edit'
    for _, _, topic, msg in fedmsg.tail_messages(topic=topic):
        # Extract some useful information for debugging
        title, subtitle, link, idx = [None] * 4
        try:
            title = fedmsg.meta.msg2title(msg, **config)
            subtitle = fedmsg.meta.msg2subtitle(msg, **config)
            link = fedmsg.meta.msg2link(msg, **config)
            idx = msg.get('msg_id')
        except Exception as e:
            print("!! Failed to determine title, subtitle, link")
        print("Inspecting {title}, {subtitle}, {link}, {idx}".format(
            title=title, subtitle=subtitle, link=link, idx=idx))

        # Extract values we need to actually process the message
        fullname = msg['msg']['project']['fullname']
        fields = msg['msg']['fields']
        content = msg['msg']['issue']['content']

        # Do the work.
        main(fullname, fields, content)
