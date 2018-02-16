from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'src'
    display_name = 'Dist-Git'
    scopes = {
        'https://src.fedoraproject.org/push': {
            'display_name': 'Push to Fedora Dist-Git',
            'claims': [],
        },
    }
