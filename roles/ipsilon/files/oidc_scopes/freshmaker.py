from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'freshmaker'
    display_name = 'Freshmaker Rebuilds'
    scopes = {
        'https://pagure.io/freshmaker/manual-trigger': {
            'display_name': 'Permission to submit manual triggers of rebuilds',
            'claims': [],
        },
    }
