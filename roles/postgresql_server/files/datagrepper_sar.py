#!/usr/bin/python

from __future__ import unicode_literals, print_function

import os
import random
import string
import subprocess
import sys
import tempfile


def main():
    ''' Prints out all the datagrepper messages related to the username
    specified in the SAR_USERNAME environment variable.
    If no such environment variable is available, the script will bail.
    '''

    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query datagrepper')
        return 1

    tempfilename = '/tmp/sar_{0}_{1}'.format(username, ''.join(
        [random.choice(string.ascii_letters + string.digits)
         for n in xrange(10)]
    ))

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
TO '{tmpfile}' delimiter ',' CSV header;
'''
    query = query.format(username=username, tmpfile=tempfilename)
    command = ['sudo', '-u', 'postgres', 'psql', 'datanommer', '-c', '"%s"' % query]
    subprocess.check_call(
        ' '.join(command), shell=True, stdout=subprocess.PIPE)
    with open(tempfilename) as stream:
        data = stream.read()
    os.unlink(tempfilename)
    print(data)


if __name__ == '__main__':
    sys.exit(main())
