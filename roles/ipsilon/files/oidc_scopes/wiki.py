from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'wiki'
    display_name = 'Fedora Wiki'
    scopes = {
        'https://fedoraproject.org/wiki/api': {
            'display_name': 'Fedora Wiki API access',
            'claims': [],
        },
    }
