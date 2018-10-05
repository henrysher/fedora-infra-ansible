from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'fpdc'
    display_name = 'Fedora Product Definition Center'
    scopes = {
        'https://fpdc.fedoraproject.org/oidc/create-release': {
            'display_name': 'Create a Release record',
            'claims': [],
        },
        'https://fpdc.fedoraproject.org/oidc/update-release': {
            'display_name': 'Update a Release record',
            'claims': [],
        },
        'https://fpdc.fedoraproject.org/oidc/delete-release': {
            'display_name': 'Delete a Release record',
            'claims': [],
        },
    }
