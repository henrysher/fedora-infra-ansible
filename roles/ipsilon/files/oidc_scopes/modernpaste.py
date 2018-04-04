from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'modernpaste'
    display_name = 'Modern Paste'
    scopes = {
        'https://paste.fedoraproject.org/' {
            'display_name': 'authenticated modernpaste access',
            'claims': [],
        },
    }
