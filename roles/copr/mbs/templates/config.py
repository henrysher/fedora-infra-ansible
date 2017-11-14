import sys
sys.path.insert(1, '/etc/module-build-service')

import base_config as base
from base_config import confdir, dbdir


class ProdConfiguration(base.ProdConfiguration):
    SYSTEM = 'copr'
    SECRET_KEY = '{{ copr_mbs_secret_key }}'

    YAML_SUBMIT_ALLOWED = True

    PDC_INSECURE = False

    # Only copr-frontend is allowed to communicate with this mbs instance
    # Therefore we don't require it to authenicate first, we trust it
    NO_AUTH = True

    # Use production instances of PDC and Koji
    KOJI_REPOSITORY_URL = 'https://kojipkgs.fedoraproject.org/repos'
    PDC_URL = 'https://pdc.fedoraproject.org/rest_api/v1'

    # Do not restrict to only trusted repositories, allow everything
    SCMURLS = []
    ALLOW_CUSTOM_SCMURLS = True

{% if env == 'staging' %}
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.dev', 'org.fedoraproject.stg']
{% else %}
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.prod', 'org.fedoraproject.dev']
{% endif %}

    # Allow custom component repositories
    RPMS_ALLOW_REPOSITORY = True
    RPMS_ALLOW_CACHE = True
    MODULES_ALLOW_REPOSITORY = True

    # Determines how many builds can be submitted to the builder
    # and be in the build state at a time. Set this to 0 for no restrictions
    # We can set some limit in the future, once we need it
    NUM_CONSECUTIVE_BUILDS = 0

    # When MBS frontend runs on same machine as scheduler,
    # it is fine to set this to localhost
    SERVER_NAME = 'localhost'


class DevConfiguration(base.DevConfiguration):
    SYSTEM = 'copr'


class BaseConfiguration(base.BaseConfiguration):
    pass


class TestConfiguration(base.TestConfiguration):
    pass
