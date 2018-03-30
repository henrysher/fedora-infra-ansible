from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'pagure'
    display_name = 'Pagure.io'
    scopes = {
        'https://pagure.io/oidc/pull_request_merge': {
            'display_name': 'Permission to merge a pull-request',
            'claims': [],
        },
        'https://pagure.io/oidc/pull_request_close': {
            'display_name': 'Permission to close a pull-request',
            'claims': [],
        },
        'https://pagure.io/oidc/pull_request_comment': {
            'display_name': 'Permission to comment a pull-request',
            'claims': [],
        },
        'https://pagure.io/oidc/pull_request_flag': {
            'display_name': 'Permission to flag a pull-request with a CI status',
            'claims': [],
        },
        'https://pagure.io/oidc/pull_request_subscribe': {
            'display_name': 'Permission to subscribe a user to a pull-request',
            'claims': [],
        },
        'https://pagure.io/oidc/pull_request_create': {
            'display_name': 'Permission to create a pull-request',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_create': {
            'display_name': 'Permission to create an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_update': {
            'display_name': 'Permission to update an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_change_status': {
            'display_name': 'Permission to change the status of an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_update_milestone': {
            'display_name': 'Permission to update the milestone of an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_comment': {
            'display_name': 'Permission to comment on an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_assign': {
            'display_name': 'Permission to assign an issue to a user',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_subscribe': {
            'display_name': 'Permission to subscribe a user to an issue',
            'claims': [],
        },
        'https://pagure.io/oidc/issue_update_custom_fields': {
            'display_name': 'Permission to update an issue custom fields',
            'claims': [],
        },
        'https://pagure.io/oidc/create_project': {
            'display_name': 'Permission to create a project',
            'claims': [],
        },
        'https://pagure.io/oidc/modify_project': {
            'display_name': 'Permission to modify a project',
            'claims': [],
        },
        'https://pagure.io/oidc/fork_project': {
            'display_name': 'Permission to fork a project',
            'claims': [],
        },
        'https://pagure.io/oidc/generate_acls_project': {
            'display_name': 'Permission to generate the gitolite ACLs of a project',
            'claims': [],
        },
        'https://pagure.io/oidc/commit_flag': {
            'display_name': 'Permission to flag a commit with a CI results',
            'claims': [],
        },
    }
