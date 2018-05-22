#!/usr/bin/python

from __future__ import unicode_literals, print_function

import os
import string
import subprocess
import sys


def main():
    ''' Prints out all the datagrepper messages related to the username
    specified in the SAR_USERNAME environment variable.
    If no such environment variable is available, the script will bail.
    '''

    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query datagrepper')
        return 1

    # Get all messages related to this user.
    query = '''
COPY (
  SELECT DISTINCT messages FROM messages WHERE
  messages.id IN (
      SELECT messages.id
      FROM messages, user_messages
      WHERE messages.id = user_messages.msg
      AND user_messages.username = '{username}'
    UNION
      SELECt messages.id
      FROM messages
      WHERE messages.username = '{username}'
  )
)
TO STDOUT delimiter ',' CSV header;
'''
    query = query.format(username=username)
    command = ['sudo', '-u', 'postgres', 'psql', 'datanommer', '-c', '"%s"' % query]
    subprocess.check_call(' '.join(command), shell=True, cwd='/tmp')


if __name__ == '__main__':
    sys.exit(main())
