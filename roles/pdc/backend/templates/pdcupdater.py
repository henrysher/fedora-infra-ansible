# Configuration for the pdc-updater backend.

config = {
    # Should we turn on the realtime updater?
    'pdcupdater.enabled': True,

    {% if inventory_hostname.startswith('pdc-backend01') %}
    # Use only one thread at a time to handle messages.  If we have more than
    # one, then we can end up POSTing multiple enormous JSON blobs to the PDC
    # web frontend, and we'll send it into OOM death.  One at a time, people..
    "moksha.workers_per_consumer": 1,
    {% else %}
    "moksha.workers_per_consumer": 8,
    {% endif %}

    # Credentials to talk to PDC
    'pdcupdater.pdc': {
        {% if env == 'staging' %}
        'server': 'http://pdc-web01.stg.phx2.fedoraproject.org/rest_api/v1/',
        'token': '{{pdc_updater_api_token_stg }}',
        {% else %}
        'server': 'http://pdc-web01.phx2.fedoraproject.org/rest_api/v1/',
        'token': '{{pdc_updater_api_token_prod }}',
        {% endif %}
    },

    # Credentials to talk to FAS
    'pdcupdater.fas': {
        {% if env == 'staging' %}
        'base_url': 'https://admin.stg.fedoraproject.org/accounts',
        {% else %}
        'base_url': 'https://admin.fedoraproject.org/accounts',
        {% endif %}
        'username': '{{ fedoraDummyUser }}',
        'password': '{{ fedoraDummyUserPassword }}',
    },

    # PkgDB details
    {% if env == 'staging' %}
    'pdcupdater.pkgdb_url': 'https://admin.stg.fedoraproject.org/pkgdb',
    {% else %}
    'pdcupdater.pkgdb_url': 'https://admin.fedoraproject.org/pkgdb',
    {% endif %}

    # Koji details
    {% if env == 'staging' %}
    'pdcupdater.koji_url': 'http://koji.stg.fedoraproject.org/kojihub',
    {% else %}
    'pdcupdater.koji_url': 'http://koji01.phx2.fedoraproject.org/kojihub',
    {% endif %}
    # Use 8 threads to talk to koji in parallel.
    'pdcupdater.koji_io_threads': 8,

    # Where to find composes
    {% if env == 'staging' %}
    'pdcupdater.old_composes_url': 'https://kojipkgs.stg.fedoraproject.org/compose/',
    {% else %}
    'pdcupdater.old_composes_url': 'https://kojipkgs.fedoraproject.org/compose/',
    {% endif %}

    # Where to find the fedora-atomic json definitions.
    'pdcupdater.fedora_atomic_git_url': 'https://pagure.io/fedora-atomic/raw/master/f/',

    # We have an explicit list of these in the config so we can turn them on
    # and off individually in production if one is causing an issue.
    'pdcupdater.handlers': [
        # See CSI information on host for info on the different handlers.
        {% if inventory_hostname.startswith('pdc-backend01') %}
        'pdcupdater.handlers.compose:NewComposeHandler',
        {% elif inventory_hostname.startswith('pdc-backend02') %}
        # For MBS https://fedoraproject.org/wiki/Changes/ModuleBuildService
        'pdcupdater.handlers.modules:ModuleStateChangeHandler',
        {% elif inventory_hostname.startswith('pdc-backend03') %}
        ## https://fedoraproject.org/wiki/User:Ralph/Drafts/Infrastructure/Factory2/ModellingDeps
        #'pdcupdater.handlers.depchain.rpms:NewRPMBuildTimeDepChainHandler',
        #'pdcupdater.handlers.depchain.rpms:NewRPMRunTimeDepChainHandler',
        'pdcupdater.handlers.depchain.containers:ContainerRPMInclusionDepChainHandler',
        {% endif %}
        # This just isn't used for now.. but we can re-enable it if we need it.
        #'pdcupdater.handlers.atomic:AtomicComponentGroupHandler',
    ],

    'logging': dict(
        loggers=dict(
            pdcupdater={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
            requests={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console"],
            },
        )
    )
}
