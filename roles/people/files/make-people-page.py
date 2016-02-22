#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2016 Chaoyi Zha <cydrobolt@fedoraproject.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import subprocess, os, hashlib, stat, grp
from jinja2 import Template

page_jinja_template = """
<DOCTYPE html>
<html>
<head>
    <title>Fedora People</title>
    <link rel='stylesheet' href='/static/datatables.min.css'>
    <link rel='stylesheet' href='//getfedora.org/static/css/bootstrap-theme.css'>
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        .center {
            text-align: center;
        }

        footer {
            margin-bottom: 45px;
        }

        .user-avatar {
            display: inline;
            height: 20px;
        }
    </style>
</head>
<body>
    <div class="jumbotron">
        <div class="container-fluid center">
            <img class="fedoralogotext" class="img-responsive center-block" src="//getfedora.org/static/images/fedora-logotext.png" alt="Fedora Logotext">
        </div>
    </div>
    <div class="container pagebody">
        <h3>Fedora People</h3>
        <p>A repository with web and <code>git</code> resources from the people behind Fedora.</p>
        <p class='text-muted'>
            <a target='_blank' href='//fedoraproject.org/wiki/Infrastructure/fedorapeople.org'>FAQ</a> on using your public space.
        </p>

        <table class='table table-hover' id='peopleTable' >
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Public Resources</th>
                </tr>
            </thead>
            <tbody>


            {% for username, user in users %}
                {% if (user['has_public_html'] or user['has_public_git']) %}
                <tr>
                    <td>
                        <img class='user-avatar' src='/static/grey.jpg' alt='Avatar for {{username}}' data-src='https://seccdn.libravatar.org/avatar/{{user['openid_hash']}}?s=20&d=retro'>
                        {{user.name.strip()}} <span class='text-muted'>({{username}})</span>
                    </td>


                    <td>
                        {% if user['has_public_git'] %}
                        <div>
                            <a href="https://fedorapeople.org/cgit/{{username}}/">Git repositories</a>
                        </div>
                        {% endif %}

                        {% if user['has_public_html'] %}
                        <div>
                            <a href="https://{{username}}.fedorapeople.org">{{username}}'s homepage</a>
                        </div>
                        {% endif %}
                        <div>
                            <a href="https://fedoraproject.org/wiki/user:{{username}}">{{username}}'s wiki page</a>
                        </div>
                    </td>
                </tr>
                {% endif %}
            {% endfor %}
        </tbody>
    </table>
    </div>

    <hr>

    <footer class='center text-muted'>
        <p class="copy">
            &copy; 2016 Chaoyi Zha, Red Hat, Inc., and others.
            Please send any comments or corrections to the <a href="mailto:admin@fedoraproject.org">infrastructure team</a>.
        </p>
        <p class="disclaimer">
            The Fedora Project is maintained and driven by the community and sponsored by Red Hat.  This is a community maintained site.  Red Hat is not responsible for content.
        </p>
            <a href="http://fedoraproject.org/wiki/Legal:Main">Legal</a> &middot; <a href="http://fedoraproject.org/wiki/Legal:Trademark_guidelines">Trademark Guidelines</a>
    </footer>

    <script src='/static/jquery.dataTables.min.js'></script>
    <script src='/static/jquery.unveil.js'></script>


    <script>
        $(document).ready(function() {
            $('table').DataTable({
                'pageLength': 50,
                'initComplete': function(settings, json) {
                    $('img').unveil();
                }
            });
            $('.table').on('draw.dt', function() {
                /* on each table draw */
                $('img').unveil();
            });
        });
    </script>

</body>
</html>
"""

# Fedora people users separated by newlines
users_list = subprocess.check_output("getent passwd | sort | cut -d: -f1,6 | grep /home/fedora/", shell=True)

# Fedora people users array with a subarray for each user containing [username, homedir]
users_list_array = [a.split(':') for a in users_list.split('\n')][:-1]

users = dict()

for user in users_list_array:
    username = user[0]
    user_homedir = user[1]
    user_name = subprocess.check_output("getent passwd {} | cut -d: -f5".format(username), shell=True)
    user_name = user_name.decode('utf-8')

    prefix_length = len("{} : ".format(user[0]))
    user_groups = subprocess.check_output(["groups", user[0]])[prefix_length:-1]

    has_public_html = os.path.isdir("{}/public_html/".format(user_homedir))
    has_public_git = os.path.isdir("{}/public_git/".format(user_homedir))

    users[username] = dict()

    users[username]['name'] = user_name

    users[username]['homedir'] = user_homedir
    users[username]['groups'] = user_groups
    users[username]['has_public_html'] = has_public_html
    users[username]['has_public_git'] = has_public_git

    user_fedora_email = '{}@fedoraproject.org'.format(username).encode('utf-8')
    user_fedora_openid = 'http://{}.id.fedoraproject.org/'.format(username).encode('utf-8')
    users[username]['email_hash'] = hashlib.md5(user_fedora_email.strip().lower()).hexdigest()
    users[username]['openid_hash'] = hashlib.sha256(user_fedora_openid.strip().lower()).hexdigest()

page_jinja_template_obj = Template(page_jinja_template)
page_output = page_jinja_template_obj.render(users=sorted(users.items()))

out_file = '/srv/people/site/index.html'

# get gid for web group
out_file_grp = grp.getgrnam("web").gr_gid;

with open(out_file, 'w') as handle:
    handle.write(page_output.encode('utf-8'))

# keep current owner uid
out_file_uid = os.stat(out_file).st_uid

# give write permissions to group
os.chmod(out_file, stat.S_IWGRP)
# chown out file to group
os.chown(out_file, out_file_uid, out_file_grp)
