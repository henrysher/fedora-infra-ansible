from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'fedora-account'
    display_name = 'Fedora Account Information'
    scopes = {
        'fedora': {  # NOTE: This is temporary! DO NOT USE IN NEW PROJECTS!
            'display_name': 'Fedora',
            'claims': ['cla', 'zoneinfo', 'groups']
        },
        'https://id.fedoraproject.org/scope/groups': {
            'display_name': 'Fedora Account Groups list',
            'claims': ['groups']
        },
        'https://id.fedoraproject.org/scope/cla': {
            'display_name': 'Fedora Account CLA status',
            'claims': ['cla']
        },
    }
