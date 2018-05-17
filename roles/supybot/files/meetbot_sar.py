#!/usr/bin/python

from __future__ import unicode_literals, print_function

import json
import os
import subprocess
import sys


_logs_folder = '/srv/web/meetbot'
_base_url = 'https://meetbot-raw.fedoraproject.org/'


def main():
    ''' Prints out links to all the meeting where the specified username or
    email are prsent.
    The username must be specified via the SAR_USERNAME environment variable.
    The email must be specified via the SAR_EMAIL environment variable.
    '''

    username = os.getenv('SAR_USERNAME')
    email = os.getenv('SAR_EMAIL')

    if not username and not email:
        print('An username or an email must be specified to query meetbot logs')
        return 1

    output = {}
    output['meetings'] = set()

    os.chdir(_logs_folder)

    def _grep_and_process(command):
        cli_out = subprocess.check_output(command).decode('utf-8')
        lines = cli_out.split('\n')
        for line in lines:
            if line.startswith('./'):
                line = line[2:]
            url = '%s/%s' % (_base_url.rstrip('/'), line)
            output['meetings'].add(url)

    if username:
        command = ['grep', '-iR', '-l', username, '.']
        _grep_and_process(command)

    if email:
        command = ['grep', '-iR', '-l', email, '.']
        _grep_and_process(command)

    output['meetings'] = list(output['meetings'])

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())
