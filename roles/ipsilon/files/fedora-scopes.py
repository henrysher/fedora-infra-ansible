from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'fedora'
    display_name = 'Fedora'
    scopes = {
        'fedora': {
            'display_name': 'Fedora',
            'claims': ['cla', 'zoneinfo', 'groups']
        }
    }
