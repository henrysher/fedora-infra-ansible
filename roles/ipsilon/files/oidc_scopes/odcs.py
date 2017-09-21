from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'odcs'
    display_name = 'On Demand Composes'
    scopes = {
        'https://pagure.io/odcs/new-compose': {
            'display_name': 'Permission to request new composes',
            'claims': [],
        },
        'https://pagure.io/odcs/renew-compose': {
            'display_name': 'Permission to renew the expiry on composes',
            'claims': [],
        },
        'https://pagure.io/odcs/delete-compose': {
            'display_name': 'Permission to delete composes',
            'claims': [],
        },
    }
