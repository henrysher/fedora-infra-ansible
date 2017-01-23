import sys
sys.path.insert(1, '/etc/module-build-service')

from base_config import confdir, dbdir, \
                        BaseConfiguration, \
                        DevConfiguration, \
                        TestConfiguration


class ProdConfiguration(BaseConfiguration):
    SYSTEM = 'copr'
    FAS_USERNAME = 'someuser'
    FAS_PASSWORD = 'secretpassword'
    OIDC_CLIENT_SECRETS = '/etc/module-build-service/client_secrets.json'
