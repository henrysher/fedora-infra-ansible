from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'waiverdb'
    display_name = 'Waiver DB'
    scopes = {
        'https://waiverdb.fedoraproject.org/oidc/create-waiver': {
            'display_name': 'Permission to create new waivers',
            'claims': [],
        },
    }
