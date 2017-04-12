from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'beaker'
    display_name = 'Beaker Jobs'
    scopes = {
        'https://beaker-project.org/oidc/scope': {
            'display_name': 'Full access to your beaker account',
            'claims': [],
        },
    }
