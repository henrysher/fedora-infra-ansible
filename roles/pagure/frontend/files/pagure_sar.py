#!/usr/bin/python

from __future__ import unicode_literals, print_function

import json
import os
import sys

import sqlalchemy

import pagure.config
import pagure.lib
from pagure.lib import model


if 'PAGURE_CONFIG' not in os.environ \
        and os.path.exists('/etc/pagure/pagure.cfg'):
    os.environ['PAGURE_CONFIG'] = '/etc/pagure/pagure.cfg'


_config = pagure.config.reload_config()
session = pagure.lib.create_session(_config['DB_URL'])


def get_issue_users(session, user_id):
    ''' Return all pagure.lib.model.Issue related to the usernames provided
    '''
    query1 = session.query(
        model.Issue.uid
    ).filter(
        sqlalchemy.or_(
            model.Issue.assignee_id == user_id,
            model.Issue.user_id == user_id
        )
    )
    query2 = session.query(
        model.Issue.uid
    ).filter(
        model.Issue.uid == model.IssueComment.issue_uid
    ).filter(
        model.IssueComment.user_id == user_id
    )

    query = session.query(
        model.Issue
    ).filter(
        sqlalchemy.or_(
            model.Issue.uid.in_(query1.subquery()),
            model.Issue.uid.in_(query2.subquery())
        )
    ).order_by(
        model.Issue.date_created
    )

    return query.all()


def get_pr_users(session, user_id):
    ''' Return all pagure.lib.model.PullRequest related to the usernames provided
    '''
    query1 = session.query(
        model.PullRequest.uid
    ).filter(
        sqlalchemy.or_(
            model.PullRequest.assignee_id == user_id,
            model.PullRequest.user_id == user_id
        )
    )
    query2 = session.query(
        model.PullRequest.uid
    ).filter(
        model.PullRequest.uid == model.PullRequestComment.pull_request_uid
    ).filter(
        model.PullRequestComment.user_id == user_id
    )

    query = session.query(
        model.PullRequest
    ).filter(
        sqlalchemy.or_(
            model.PullRequest.uid.in_(query1.subquery()),
            model.PullRequest.uid.in_(query2.subquery())
        )
    ).order_by(
        model.PullRequest.date_created
    )

    return query.all()


def main():
    ''' Prints out all the pagure project and comment related to the username
    specified in the SAR_USERNAME environment variable or the email
    specified in the SAR_EMAIL environment variable..
    '''

    username = os.getenv('SAR_USERNAME')
    email = os.getenv('SAR_EMAIL')

    users = []
    if username:
        users.append(pagure.lib.search_user(session, username=username))
    if email:
        user_email = pagure.lib.search_user(session, email=email)
        if user_email not in users:
            users.append(user_email)

    output = {}

    for user in users:
        temp = {}
        temp['user_info'] = user.to_json(public=False)

        projects = pagure.lib.search_projects(session, user.username)
        projects = [
            project.to_json()
            for project in projects
        ]
        temp['projects'] = projects

        issues = get_issue_users(session, user.id)
        issues_json = []
        for issue in issues:
            tmp = issue.to_json()
            comments = []
            for comment in tmp['comments']:
                if comment['user']['name'] != username:
                    continue
                comments.append(comment)
            tmp['comments'] = comments
            issues_json.append(tmp)
        temp['issues'] = issues_json

        prs = get_pr_users(session, user.id)
        prs_json = []
        for pr in prs:
            tmp = pr.to_json()
            comments = []
            for comment in tmp['comments']:
                if comment['user']['name'] != username:
                    continue
                comments.append(comment)
            tmp['comments'] = comments
            prs_json.append(tmp)
        temp['pull_requests'] = prs_json

        output[user.username] = temp

    session.remove()

    print(json.dumps(
        output, sort_keys=True, indent=4, separators=(',', ': ')
    ).encode('utf-8'))


if __name__ == '__main__':
    sys.exit(main())
