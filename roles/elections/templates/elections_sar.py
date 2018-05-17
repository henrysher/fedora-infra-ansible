#!/usr/bin/python

from __future__ import unicode_literals, print_function

import json
import os
import sys

import sqlalchemy


if 'FEDORA_ELECTIONS_CONFIG' not in os.environ \
        and os.path.exists('/etc/fedora-elections/fedora-elections.cfg'):
    os.environ['FEDORA_ELECTIONS_CONFIG'] = '/etc/fedora-elections/'\
        'fedora-elections.cfg'


from fedora_elections import SESSION
from fedora_elections import models


def get_candidate_users(session, username):
    ''' Return all fedora_elections.models.Candidate related to the username
    provided
    '''
    query = SESSION.query(
        models.Candidate
    ).filter(
        sqlalchemy.or_(
            models.Candidate.name.ilike('%{0}%'.format(username)),
            models.Candidate.fas_name.ilike('%s%'.format(username))
        )
    )

    return query.all()


def main():
    ''' Prints out all the election involving the username specified in the
    SAR_USERNAME environment variable.
    '''

    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query datagrepper')
        return 1

    output = {}
    output['candidates'] = []

    for candidate in get_candidate_users(SESSION, username):
        tmp = candidate.to_json()
        tmp['election'] = candidate.election.to_json()
        output['candidates'].append(tmp)

    SESSION.remove()

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())
