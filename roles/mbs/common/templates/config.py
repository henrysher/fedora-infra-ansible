from os import path

# FIXME: workaround for this moment till confdir, dbdir (installdir etc.) are
# declared properly somewhere/somehow
confdir = path.abspath(path.dirname(__file__))
# use parent dir as dbdir else fallback to current dir
dbdir = path.abspath(path.join(confdir, '..')) if confdir.endswith('conf') \
        else confdir


class BaseConfiguration(object):
    DEBUG = False
    # Make this random (used to generate session keys)
    SECRET_KEY = '74d9e9f9cd40e66fc6c4c2e9987dce48df3ce98542529fd0'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{0}'.format(path.join(
        dbdir, 'module_build_service.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    # Where we should run when running "manage.py runssl" directly.
    HOST = '0.0.0.0'
    PORT = 5000

    # Global network-related values, in seconds
    NET_TIMEOUT = 120
    NET_RETRY_INTERVAL = 30

    SYSTEM = 'koji'
    MESSAGING = 'fedmsg'  # or amq
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.prod']
    KOJI_CONFIG = '/etc/module-build-service/koji.conf'
    KOJI_PROFILE = 'koji'
    ARCHES = ['i686', 'armv7hl', 'x86_64']
    KOJI_PROXYUSER = True
    KOJI_REPOSITORY_URL = 'https://kojipkgs.stg.fedoraproject.org/repos'
    COPR_CONFIG = '/etc/module-build-service/copr.conf'
    PDC_URL = 'http://modularity.fedorainfracloud.org:8080/rest_api/v1'
    PDC_INSECURE = True
    PDC_DEVELOP = True
    SCMURLS = ["git+https://src.fedoraproject.org/modules/"]

    # How often should we resort to polling, in seconds
    # Set to zero to disable polling
    POLLING_INTERVAL = 3600

    RPMS_DEFAULT_REPOSITORY = 'git+https://src.fedoraproject.org/rpms/'
    RPMS_ALLOW_REPOSITORY = False
    RPMS_DEFAULT_CACHE = 'https://src.fedoraproject.org/repo/pkgs/'
    RPMS_ALLOW_CACHE = False

    MODULES_DEFAULT_REPOSITORY = 'git+https://src.fedoraproject.org/modules/'
    MODULES_ALLOW_REPOSITORY = False

    # Available backends are: console, file, journal.
    LOG_BACKEND = 'journal'

    # Path to log file when LOG_BACKEND is set to "file".
    LOG_FILE = 'module_build_service.log'

    # Available log levels are: debug, info, warn, error.
    LOG_LEVEL = 'info'

    # Settings for Kerberos
    KRB_KEYTAB = None
    KRB_PRINCIPAL = None
    KRB_CCACHE = None

    # AMQ prefixed variables are required only while using 'amq' as messaging backend
    # Addresses to listen to
    AMQ_RECV_ADDRESSES = ['amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.koji',
                          'amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.module_build_service']
    # Address for sending messages
    AMQ_DEST_ADDRESS = 'amqps://messaging.mydomain.com/Consumer.m8y.VirtualTopic.eng.module_build_service'
    AMQ_CERT_FILE = '/etc/module_build_service/msg-m8y-client.crt'
    AMQ_PRIVATE_KEY_FILE = '/etc/module_build_service/msg-m8y-client.key'
    AMQ_TRUSTED_CERT_FILE = '/etc/module_build_service/Root-CA.crt'


class ProdConfiguration(BaseConfiguration):
    DEBUG = False  # Don't turn this on.

    # These groups are allowed to submit builds.
    ALLOWED_GROUPS = [
        # https://pagure.io/fesco/issue/1763
        'packager',
    ]

    # These groups are allowed to cancel the builds of other users.
    ADMIN_GROUPS = [
        'factory2',
        'releng',
    ]

    REBUILD_STRATEGY = 'only-changed'
    REBUILD_STRATEGY_ALLOW_OVERRIDE = True

{% if env == 'staging' %}
    SECRET_KEY = '{{ mbs_stg_secret_key }}'
    SQLALCHEMY_DATABASE_URI = 'postgresql://mbs:{{mbs_stg_db_password}}@db-mbs/mbs'
{% else %}
    SECRET_KEY = '{{ mbs_prod_secret_key }}'
    SQLALCHEMY_DATABASE_URI = 'postgresql://mbs:{{mbs_prod_db_password}}@db-mbs/mbs'
{% endif %}

{% if env == 'staging' %}
    KRB_PRINCIPAL = 'mbs/mbs.stg.fedoraproject.org@STG.FEDORAPROJECT.ORG'
{% else %}
    KRB_PRINCIPAL = 'mbs/mbs.fedoraproject.org@FEDORAPROJECT.ORG'
{% endif %}

    KRB_KEYTAB = '/etc/krb5.mbs_mbs{{env_suffix}}.fedoraproject.org.keytab'
    KRB_CCACHE = '/var/cache/fedmsg/mbs-krb5cc'

    # https://pagure.io/fm-orchestrator/issue/334
    KOJI_PROXYUSER = False

    LOG_LEVEL = 'debug'
    LOG_BACKEND = 'console'

    # Our per-build logs for the koji-content generator go here.
    # CG imports are controlled by KOJI_ENABLE_CONTENT_GENERATOR
    BUILD_LOGS_DIR = '/var/tmp'

    # Yes, use tls.
    PDC_INSECURE = False
    # No, don't try to obtain a token (we just read.  we don't write.)
    PDC_DEVELOP = True

    KOJI_CONFIG = path.join(confdir, 'koji.conf')
{% if env == 'staging' %}
    KOJI_PROFILE = 'staging'
    ARCHES = ['aarch64', 'x86_64']
    BASE_MODULE_ARCHES = {
        # Fedora 31 and later drop 'i686'. Keep it around for older releases.
        # https://fedoraproject.org/wiki/Changes/Noi686Repositories
        'platform:f28': ['aarch64', 'x86_64', 'i686'],
        'platform:f29': ['aarch64', 'x86_64', 'i686'],
        'platform:f30': ['aarch64', 'x86_64', 'i686'],
    }
    KOJI_REPOSITORY_URL = 'https://kojipkgs.stg.fedoraproject.org/repos'
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.stg']
    PDC_URL = 'https://pdc.stg.fedoraproject.org/rest_api/v1'
    SCMURLS = ['git+https://src.stg.fedoraproject.org/modules/',
               'https://src.stg.fedoraproject.org/modules/',
               'https://src.stg.fedoraproject.org/git/modules/',
               'git+https://src.stg.fedoraproject.org/flatpaks/',
               'https://src.stg.fedoraproject.org/flatpaks/',
               'https://src.stg.fedoraproject.org/git/flatpaks/']
    RPMS_DEFAULT_REPOSITORY = 'git+https://src.stg.fedoraproject.org/rpms/'
    RPMS_DEFAULT_CACHE = 'https://src.stg.fedoraproject.org/repo/pkgs/'
    MODULES_DEFAULT_REPOSITORY = 'git+https://src.stg.fedoraproject.org/modules/'

{% else %}
    KOJI_PROFILE = 'production'
    ARCHES = ['aarch64', 'armv7hl', 'i686', 'ppc64le', 'x86_64', 's390x']
    BASE_MODULE_ARCHES = {
        # Fedora 28 includes 'ppc64'.  F29 and later drops it.
        # https://fedoraproject.org/wiki/Changes/DiscontinuePPC64
        'platform:f28': ['aarch64', 'armv7hl', 'i686', 'ppc64', 'ppc64le', 'x86_64', 's390x'],
    }
    KOJI_REPOSITORY_URL = 'https://kojipkgs.fedoraproject.org/repos'
    MESSAGING_TOPIC_PREFIX = ['org.fedoraproject.prod']
    PDC_URL = 'https://pdc.fedoraproject.org/rest_api/v1'
    SCMURLS = ['git+https://src.fedoraproject.org/modules/',
               'https://src.fedoraproject.org/modules/',
               'https://src.fedoraproject.org/git/modules/',
               'git+https://src.fedoraproject.org/flatpaks/',
               'https://src.fedoraproject.org/flatpaks/',
               'https://src.fedoraproject.org/git/flatpaks/']
    KOJI_TAG_EXTRA_OPTS = {
        "mock.package_manager": "dnf",
        "repo_include_all": True,
        "mock.new_chroot": 0,
        "mock.yum.module_hotfixes": 1,
    }
{% endif %}

    RESOLVER = "db"

    # Made possible by https://pagure.io/releng/issue/6799
    KOJI_ENABLE_CONTENT_GENERATOR = True

    # See https://pagure.io/releng/issue/7012
    BASE_MODULE_NAMES = set(['platform', 'bootstrap'])
    KOJI_CG_BUILD_TAG_TEMPLATE = "{}-modular-updates-candidate"
    KOJI_CG_DEFAULT_BUILD_TAG = "modular-updates-candidate"

    # This is a whitelist of prefixes of koji tags we're allowed to manipulate
    KOJI_TAG_PREFIXES = [
        # This is our standard prefix.  All module tags should start with this.
        'module',
        # Our very first manually bootstrapped tag has this name.
        'f26-modularity',
        # Scratch module builds have this prefix
        'scrmod',
    ]

    # If this is too long, we could change it to 'fm_' some day.
    DEFAULT_DIST_TAG_PREFIX = 'module_'

    # Delete module-* targets one hour after build
    KOJI_TARGET_DELETE_TIME = 3600

    # These aren't really secret.
    OIDC_CLIENT_SECRETS = path.join(confdir, 'client_secrets.json')
    OIDC_REQUIRED_SCOPE = 'https://mbs.fedoraproject.org/oidc/submit-build'

    # yes, we want everyone to authenticate
    NO_AUTH = False  # Obviously.

    # Don't let people submit yaml directly.  it has to come from dist-git
    YAML_SUBMIT_ALLOWED = False

    # Relative Koji task priority (0 means default priority of 20).
    KOJI_BUILD_PRIORITY = 0

    # Check branch EOL before building.  Block EOL modules from building.
    # https://pagure.io/fm-orchestrator/issue/960
    # Because of https://lists.fedoraproject.org/archives/list/devel@lists.fedoraproject.org/thread/KGXBMTUR72FHQEG7IBHDPPX276QHSD2I/#MFT5SAWPKMCNLKAWEJFCFIVX5GJ7RBSP
    # we decided to hold on to this and ask the maintainers to create a
    # releng ticket to retire their modules.
    CHECK_FOR_EOL = False 

    # Koji Content Generator "-devel" modules aren't used in Fedora, so we can just disable them
    KOJI_CG_DEVEL_MODULE = False

    MODULES_ALLOW_SCRATCH = True

    # By default, MBS allows buildrequiring only modules built against
    # compatible version of platform base module. By compatible, we mean
    # less or equal minor number of "stream_version". For example, when building module
    # against platform:f30, it wouldn't be possible to buildrequire a module
    # built against platform:f29. This is not intended behaviour in Fedora
    # and therefore we want to turn this feature off.
    ALLOW_ONLY_COMPATIBLE_BASE_MODULES = False

