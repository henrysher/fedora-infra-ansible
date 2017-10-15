#!/usr/bin/python -tt

"""
This script is ran as a cronjob and bastion.

Its goal is to generate all the <pkg>-owner email aliases we provide
"""

import requests

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


def retry_session():
    session = requests.Session()
    retry = Retry(
        total=5,
        read=5,
        connect=5,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


pagure_url = 'https://src.fedoraproject.org/'
pagure_group_url = pagure_url + '/api/0/group/{group}'
project_to_email = {}


def get_pagure_projects():
    pagure_projects_url = pagure_url + '/api/0/projects?page=1&per_page=100&fork=false'
    session = retry_session()
    while pagure_projects_url:
        response = session.get(pagure_projects_url)
        data = response.json()
        for project in data['projects']:
            yield project
        # This is set to None on the last page.
        pagure_projects_url = data['pagination']['next']


session = retry_session()
for project in get_pagure_projects():
    users = set(project['access_users']['owner']) | \
            set(project['access_users']['admin']) | \
            set(project['access_users']['commit'])
    groups = set()
    for group_kind in ('admin', 'commit'):
        for group in project['access_groups'][group_kind]:
            groups.add(group)

    for group in groups:
        group_members = session.get(
            pagure_group_url.format(group=group)).json()['members']
        users = users | set(group_members)

    project_alias = '{0}-owner'.format(project['name'])
    # If there is a namespace, prefix the email with it plus a dash
    if project['namespace'] and project['namespace'] != 'rpms':
        project_alias = '{0}-{1}'.format(project['namespace'], project_alias)

    # Use the @fedoraproject.org email alias instead of looking their email up
    # in FAS
    emails = ['{0}@fedoraproject.org'.format(user) for user in users]

    # Handle case-insensitivity in postfix by unioning things.
    project_alias = project_alias.lower()
    if project_alias in project_to_email:
        project_to_email[project_alias] = project_to_email[project_alias].union(emails)
    else:
        project_to_email[project_alias] = set(emails)


for project_alias, emails in project_to_email.items():
    print('{0}: {1}'.format(project_alias, ','.join(sorted(emails))))
