#!/usr/bin/python

from __future__ import unicode_literals, print_function

import os
import json
import sys


if 'FEDOCAL_CONFIG' not in os.environ \
        and os.path.exists('/etc/fedocal/fedocal.cfg'):
    os.environ['FEDOCAL_CONFIG'] = '/etc/fedocal/fedocal.cfg'


from fedocal import SESSION  # noqa
from fedocal.fedocallib import model  # noqa


def get_user_calendars(email):
    ''' Return fedocal.fedocallib.model.Calendar objects related to the
    specified user.
    '''
    query = SESSION.query(
        model.Calendar
    ).filter(
        model.Calendar.calendar_contact == email
    ).order_by(
        model.Calendar.calendar_name
    )
    return query.all()


def get_user_meetings(username):
    ''' Return fedocal.fedocallib.model.Meeting objects related to the
    specified user.
    '''
    query = SESSION.query(
        model.Meeting
    ).filter(
        model.Meeting.meeting_id == model.MeetingsUsers.meeting_id
    ).filter(
        model.MeetingsUsers.username == username
    ).order_by(
        model.Meeting.meeting_id
    )
    return query.all()


def main():
    ''' Prints out all the calendar and meeting related to the username
    specified in the SAR_USERNAME environment variable.
    If no such environment variable is available, the script will bail.
    '''
    email = os.getenv('SAR_EMAIL')
    username = os.getenv('SAR_USERNAME')
    if not username:
        print('An username is required to query fedocal')
        return 1

    output = {}
    # Get all calendar related to this user.
    output['calendars'] = [
        calendar.to_json()
        for calendar in get_user_calendars(email)
    ]
    output['meetings'] = [
        meeting.to_json()
        for meeting in get_user_meetings(username)
    ]

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())
