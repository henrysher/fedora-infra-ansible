import sys
sys.path.insert(1, '/etc/module-build-service')

import base_config as base
from base_config import confdir, dbdir


class ProdConfiguration(base.ProdConfiguration):
    SYSTEM = 'copr'
    SECRET_KEY = '{{ copr_mbs_secret_key }}'

    YAML_SUBMIT_ALLOWED = True

    # Only copr-frontend is allowed to communicate with this mbs instance
    # Therefore we don't require it to authenicate first, we trust it
    NO_AUTH = True

    # Use production instances of PDC and Koji
    KOJI_REPOSITORY_URL = 'https://kojipkgs.fedoraproject.org/repos'
    PDC_URL = 'http://pdc.fedoraproject.org/rest_api/v1'

    # When building from scmurl,
    # only such URLs that starts with some of these are allowed
    # Currently it is not possible to turn this feature off
    # and allow everything, so let's allow at least something
    SCMURLS = ["git://pkgs.stg.fedoraproject.org/modules/",
               "git://pkgs.fedoraproject.org/modules/"]

{% if env == 'staging' %}
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.dev', 'org.fedoraproject.stg']
{% else %}
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.prod', 'org.fedoraproject.dev']
{% endif %}

    # Allow custom component repositories
    RPMS_ALLOW_REPOSITORY = True
    RPMS_ALLOW_CACHE = True
    MODULES_ALLOW_REPOSITORY = True


class DevConfiguration(base.DevConfiguration):
    SYSTEM = 'copr'


class BaseConfiguration(base.BaseConfiguration):
    pass


class TestConfiguration(base.TestConfiguration):
    pass
