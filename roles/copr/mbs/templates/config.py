import sys
sys.path.insert(1, '/etc/module-build-service')

import base_config as base
from base_config import confdir, dbdir


class ProdConfiguration(base.ProdConfiguration):
    SYSTEM = 'copr'
    REQUIRE_PACKAGER = False
    SECRET_KEY = '{{ copr_mbs_secret_key }}'
    NO_AUTH = True


class DevConfiguration(base.DevConfiguration):
    SYSTEM = 'copr'


class BaseConfiguration(base.BaseConfiguration):
    pass


class TestConfiguration(base.TestConfiguration):
    pass
