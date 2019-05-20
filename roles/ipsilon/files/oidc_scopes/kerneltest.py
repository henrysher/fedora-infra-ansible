from __future__ import absolute_import

from ipsilon.providers.openidc.plugins.common import OpenidCExtensionBase


class OpenidCExtension(OpenidCExtensionBase):
    name = 'kerneltest'
    display_name = 'Fedora Kernel tests'
    scopes = {
        'https://github.com/jmflinuxtx/kerneltest-harness/oidc/upload_test_run': {
            'display_name': 'Upload the results of a test run',
            'claims': [],
        },
    }
