#!/usr/bin/python -tt
#-*- coding: utf-8 -*-

#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

"""
The idea of this program is to gather tickets from different project
which are marked as 'easyfix' (or any other keyword for that matter).

This version is a simple proof of concept, eventually it should be
converted to an html page and this script run by a cron job of some sort.

The different project to suscribe by email or a git repo or a page on
the wiki. To be sorted out...
"""

import argparse
import datetime
import json
import logging
import os
import re
import urllib2
import xmlrpclib
from bugzilla.rhbugzilla import RHBugzilla
import fedora.client
from kitchen.text.converters import to_bytes
# Let's import template stuff
from jinja2 import Template

__version__ = '0.1.1'
bzclient = RHBugzilla(url='https://bugzilla.redhat.com/xmlrpc.cgi', cookiefile=None, tokenfile=None)
# So the bugzilla module has some way to complain
logging.basicConfig()
logger = logging.getLogger('bugzilla')
#logger.setLevel(logging.DEBUG)

RETRIES = 2


class MediaWikiException(Exception):
    """ MediaWikiException class.
    Exception class generated when something has gone wrong while
    querying the MediaWiki instance of the project.
    """
    pass


class MediaWiki(fedora.client.Wiki):
    """ Mediawiki class.
    Handles interaction with the Mediawiki.
    Code stolen from cnucnu:
    https://fedorapeople.org/gitweb?p=till/public_git/cnucnu.git;a=summary
    """

{% if env == 'staging' %}
    def __init__(self, base_url='https://stg.fedoraproject.org/w/', *args,
{% else %}
    def __init__(self, base_url='https://fedoraproject.org/w/', *args,
{% endif %}
        **kwargs):
        """ Instanciate a Mediawiki client.
        :arg base_url: base url of the mediawiki to query.
        """
        super(MediaWiki, self).__init__(base_url, *args, **kwargs)

    def json_request(self, method="api.php", req_params=None,
        auth=False, **kwargs):
        """ Perform a json request to retrieve the content of a page.
        """
        if req_params:
            req_params["format"] = "json"

        data = None
        for i in range(0, RETRIES+1):
            try:
                data = self.send_request(method, req_params, auth, **kwargs)
            except fedora.client.ServerError, ex:
                if i >= RETRIES:
                    raise MediaWikiException(
                    'Could not contact the wiki -- error: %s' % ex)
            else:
                break

        if 'error' in data:
            raise MediaWikiException(data['error']['info'])
        return data

    def get_pagesource(self, titles):
        """ Retrieve the content of a given page from Mediawiki.
        :arg titles, the title of the page to return
        """
        data = self.json_request(req_params={
                'action': 'query',
                'titles': titles,
                'prop': 'revisions',
                'rvprop': 'content'
                }
                )
        return data['query']['pages'].popitem()[1]['revisions'][0]['*']


class Project(object):
    """ Simple object representation of a project. """

    def __init__(self):
        self.name = ""
        self.url = ""
        self.site = ""
        self.owner = ""
        self.tag = ""
        self.tickets = []


class Ticket(object):
    """ Simple object representation of a ticket. """

    def __init__(self):
        self.id = ""
        self.url = ""
        self.title = ""
        self.status = ""
        self.type = ""
        self.component = ""


def gather_bugzilla_easyfix():
    """ From the Red Hat bugzilla, retrieve all new tickets flagged as
    easyfix.
    """
    bugbz = bzclient.query(
         {'f1': 'keywords',
         'o1': 'allwords',
         'v1': 'easyfix',
         'query_format': 'advanced',
         'bug_status': ['NEW'],
         'classification': 'Fedora'})
    #print " {0} easyfix bugs retrieve from the BZ ".format(len(bugbz))
    return bugbz


def gather_project():
    """ Retrieve all the projects which have subscribed to this idea.
    """
{% if env == 'staging' %}
    wiki = MediaWiki(base_url='https://stg.fedoraproject.org/w/')
{% else %}
    wiki = MediaWiki(base_url='https://fedoraproject.org/w/')
{% endif %}
    page = wiki.get_pagesource("Easyfix")
    projects = []
    for row in page.split('\n'):
        regex = re.search(' \* ([^ ]*) ([^ ]*)( [^ ]*)?', row)
        if regex:
            project = Project()
            project.name = regex.group(1)
            project.tag = regex.group(2)
            project.owner = regex.group(3)
            projects.append(project)
    return projects


def parse_arguments():
    parser = argparse.ArgumentParser(__doc__)
    parser.add_argument(
        '--fedmenu-url', help="URL of the fedmenu resources (optional)")
    parser.add_argument(
        '--fedmenu-data-url', help="URL of the fedmenu data source (optional)")
    args = parser.parse_args()
    result = {}
    for key in ['fedmenu_url', 'fedmenu_data_url']:
        if getattr(args, key):
            result[key] = getattr(args, key)
    return result


def main():
    """ For each projects which have suscribed in the correct place
    (fedoraproject wiki page), gather all the tickets containing the
    provided keyword.
    """

    extra_kwargs = parse_arguments()

    template = '/etc/fedora-gather-easyfix/template.html'
    if not os.path.exists(template):
        template = './template.html'
    if not os.path.exists(template):
        print 'No template found'
        return 1

    try:
        projects = gather_project()
    except MediaWikiException, ex:
        print ex
        return
    ticket_num = 0
    for project in projects:
        #print 'Project: %s' % project.name
        tickets = []
        if project.name.startswith('github:'):
            project.name = project.name.split('github:')[1]
            project.url = 'https://github.com/%s/' % (project.name)
            project.site = 'github'
            url = 'https://api.github.com/repos/%s/issues' \
                '?labels=%s&state=open' % (project.name, project.tag)
            stream = urllib2.urlopen(url)
            output = stream.read()
            jsonobj = json.loads(output)
            if jsonobj:
                for ticket in jsonobj:
                    ticket_num = ticket_num + 1
                    ticketobj = Ticket()
                    ticketobj.id = ticket['number']
                    ticketobj.title = ticket['title']
                    ticketobj.url = ticket['html_url']
                    ticketobj.status = ticket['state']
                    tickets.append(ticketobj)
        elif project.name.startswith('pagure.io:'):
            project.name = project.name.split('pagure.io:')[1]
            project.url = 'https://pagure.io/%s/' % (project.name)
            project.site = 'pagure.io'
            url = 'https://pagure.io/api/0/%s/issues' \
                '?status=Open&tags=%s' % (project.name, project.tag)
            stream = urllib2.urlopen(url)
            output = stream.read()
            jsonobj = json.loads(output)
            if jsonobj:
                for ticket in jsonobj['issues']:
                    ticket_num = ticket_num + 1
                    ticketobj = Ticket()
                    ticketobj.id = ticket['id']
                    ticketobj.title = ticket['title']
                    ticketobj.url = 'https://pagure.io/%s/issue/%s' % (
                        project.name, ticket['id'])
                    ticketobj.status = ticket['status']
                    tickets.append(ticketobj)
        project.tickets = tickets

    bzbugs = gather_bugzilla_easyfix()

    try:
        # Read in template
        stream = open(template, 'r')
        tplfile = stream.read()
        stream.close()
        # Fill the template
        mytemplate = Template(tplfile)
        html = mytemplate.render(
            projects=projects,
            bzbugs=bzbugs,
            ticket_num=ticket_num,
            bzbugs_num=len(bzbugs),
            date=datetime.datetime.now().strftime("%a %b %d %Y %H:%M"),
            **extra_kwargs
        )
        # Write down the page
        stream = open('index.html', 'w')
        stream.write(to_bytes(html))
        stream.close()
    except IOError, err:
        print 'ERROR: %s' % err


if __name__ == '__main__':
    main()
