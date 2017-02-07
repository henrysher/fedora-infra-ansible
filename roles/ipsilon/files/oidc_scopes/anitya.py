from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'anitya'
    display_name = 'Release Monitoring'
    scopes = {
        'https://release-monitoring.org/oidc/upstream': {
            'display_name': 'Permission to register new upstream projects for monitoring',
            'claims': []
        },
        'https://release-monitoring.org/oidc/downstream': {
            'display_name': 'Permission to register new distros and new upstream/downstream mappings',
            'claims': []
        },
    }
