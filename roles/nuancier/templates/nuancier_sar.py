#!/usr/bin/python

from __future__ import unicode_literals, print_function

import os
import json
import sys


if 'NUANCIER_CONFIG' not in os.environ \
        and os.path.exists('/etc/nuancier/nuancier.cfg'):
    os.environ['NUANCIER_CONFIG'] = '/etc/nuancier/nuancier.cfg'


from nuancier import SESSION  # noqa
from nuancier.lib import model  # noqa

_base_url = 'https://apps.fedoraproject.org/'\
    'nuancier/pictures/{folder}/{filename}'


def get_user_candidates_by_name(username):
    ''' Return nuancier.lib.model.Candidate objects related to the
    specified username.
    '''
    query = SESSION.query(
        model.Candidates
    ).filter(
        model.Candidates.candidate_submitter == username
    ).order_by(
        model.Candidates.date_created
    )

    return query.all()


def get_user_candidates_by_email(email):
    ''' Return nuancier.lib.model.Candidate objects related to the
    specified email address.
    '''
    query = SESSION.query(
        model.Candidates
    ).filter(
        model.Candidates.submitter_email == email
    ).order_by(
        model.Candidates.date_created
    )

    return query.all()


def main():
    ''' Prints out all the candidates related to the username specified in
    the SAR_USERNAME environment variable or the email address specified
    in the SAR_EMAIL environment.
    If no such SAR_USERNAME is available, the script will bail.
    '''
    email = os.getenv('SAR_EMAIL')
    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query nuancier')
        return 1

    output = {}
    output['candidates'] = []
    # Get all candidates related to this user.
    for candidate in get_user_candidates_by_name(username):
        cand_json = candidate.api_repr(1)
        cand_json['election'] = candidate.election.api_repr(1)
        # Convert dates
        for key in ['submission_date_start', 'submission_date_end',
                    'date_start', 'date_end']:
            cand_json['election'][key] = \
                cand_json['election'][key].isoformat()

        # Add url to the candidate image
        folder = candidate.election.election_folder
        filename = candidate.candidate_file
        cand_json['url'] = _base_url.format(
            folder=folder, filename=filename)
        output['candidates'].append(cand_json)

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())
