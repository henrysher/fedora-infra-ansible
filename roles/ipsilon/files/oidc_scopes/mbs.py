from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'mbs'
    display_name = 'Module Builds'
    scopes = {
        'https://mbs.fedoraproject.org/oidc/submit-build': {
            'display_name': 'Permission to submit new module builds',
            'claims': [],
        },
    }
