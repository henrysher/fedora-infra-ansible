import sys
sys.path.insert(1, '/etc/module-build-service')

import base_config as base
from base_config import confdir, dbdir


class ProdConfiguration(base.ProdConfiguration):
    SYSTEM = 'copr'
    FAS_USERNAME = 'someuser'
    FAS_PASSWORD = 'secretkey'
    OIDC_CLIENT_SECRETS = '/etc/module-build-service/client_secrets.json'


class DevConfiguration(base.DevConfiguration):
    SYSTEM = 'copr'


class BaseConfiguration(base.BaseConfiguration):
    pass


class TestConfiguration(base.TestConfiguration):
    pass
