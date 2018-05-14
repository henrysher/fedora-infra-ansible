#!/usr/bin/python2
# Copyright (c) 2018 Red Hat, Inc.
#
# This file is part of Bodhi.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
"""This script will print out SAR data for a FAS account given as the SAR_USERNAME env var."""

import json
import os

import sqlalchemy

from bodhi.server import config, initialize_db, models


initialize_db(config.config)


sar_data = {}


if os.environ['SAR_USERNAME']:
    user = None

    try:
        user = models.User.query.filter_by(name=os.environ['SAR_USERNAME']).one()
    except sqlalchemy.orm.exc.NoResultFound:
        # User not found so nothing to do.
        pass

    if user is not None:
        sar_data[user.name] = {}
        sar_data[user.name]['comments'] = [
            {'karma': c.karma, 'karma_critpath': c.karma_critpath, 'text': c.text,
             'anonymous': c.anonymous, 'timestamp': c.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
             'update_alias': c.update.alias, 'username': c.user.name}
            for c in user.comments]
        sar_data[user.name]['updates'] = [
            {'autokarma': u.autokarma, 'stable_karma': u.stable_karma,
             'unstable_karma': u.unstable_karma, 'requirements': u.requirements,
             'require_bugs': u.require_bugs, 'require_testcases': u.require_testcases,
             'notes': u.notes, 'type': str(u.type), 'severity': str(u.severity),
             'suggest': str(u.suggest), 'close_bugs': u.close_bugs, 'alias': u.alias,
             'builds': [b.nvr for b in u.builds], 'release_name': u.release.name,
             'bugs': [b.bug_id for b in u.bugs], 'user': u.user.name,
             'date_submitted': u.date_submitted.strftime('%Y-%m-%d %H:%M:%S')}
            for u in user.updates]


print(json.dumps(sar_data))
