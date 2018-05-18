#!/usr/bin/python

from __future__ import unicode_literals, print_function

import os
import json
import subprocess
import sys
import time

import koji


def get_user_tasks(session, user_id):
    ''' Return all the tasks related to the specified user
    '''

    callopts = {
        'state': [koji.TASK_STATES[s] for s in ('FREE', 'OPEN', 'ASSIGNED')],
        'decode': True,
        'owner': user_id,
    }
    qopts = {'order': 'priority,create_time'}

    tasklist = session.listTasks(callopts, qopts)
    tasks = dict([(x['id'], x) for x in tasklist])

    # thread the tasks
    for t in tasklist:
        if t['parent'] is not None:
            parent = tasks.get(t['parent'])
            if parent:
                parent.setdefault('children', [])
                parent['children'].append(t)
                t['sub'] = True

    return tasklist


def get_user_builds(session, user_id):
    ''' Return all the builds related to the specified user
    '''

    callopts = {
        'userID': user_id,
    }

    data = session.listBuilds(**callopts)
    data = sorted(data, key=lambda b: [b.get(k) for k in ['nvr']],
                  reverse=False)
    for build in data:
        build['state'] = koji.BUILD_STATES[build['state']]

    buildlist = []
    for build in data:
        buildlist.append(build)

    return buildlist


def get_user_packages(session, user_id):
    ''' Return all the packages related to the specified user
    '''

    callopts = {
        'userID': user_id,
    }

    data = session.listPackages(**callopts)
    data = sorted(data, key=lambda b: [b.get(k) for k in ['nvr']],
                  reverse=False)

    pkglist = []
    for pkg in data:
        pkglist.append(pkg)

    return pkglist


def get_user_history(session, username):
    ''' Return all the history related to the specified user
    '''
    command = ['koji', 'list-history', '--user', username, '--all']
    output = subprocess.check_output(command)

    return output.split('\n')


def main():
    ''' Prints out all the calendar and meeting related to the username
    specified in the SAR_USERNAME environment variable.
    If no such environment variable is available, the script will bail.
    '''

    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query koji')
        return 1

    session = koji.ClientSession('https://koji.fedoraproject.org/kojihub')

    output = {}
    # Get the user information
    user = session.getUser(username)
    output['user_info'] = user
    # Get all tasks related to this user.
    output['tasks'] = get_user_tasks(session, user['id'])
    # Get all builds related to this user.
    output['builds'] = get_user_builds(session, user['id'])
    # Get all packages related to this user.
    output['packages'] = get_user_packages(session, user['id'])
    # Get all history related to this user. -- This is very long...
    output['history'] = get_user_history(session, username)

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))

    try:
        session.logout()
    except:
        pass


if __name__ == '__main__':
    sys.exit(main())
