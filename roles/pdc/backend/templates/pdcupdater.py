# Configuration for the pdc-updater backend.

config = {
    # Should we turn on the realtime updater?
    'pdcupdater.enabled': True,

    # Credentials to talk to PDC
    'pdcupdater.pdc': {
        {% if env == 'staging' %}
        'server': 'https://pdc.stg.fedoraproject.org/rest_api/v1/',
        'insecure': False,
        'token': '{{pdc_updater_api_token_stg }}',
        {% else %}
        'server': 'https://pdc.fedoraproject.org/rest_api/v1/',
        'insecure': False,
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
    'pdcupdater.koji_url': 'http://koji.fedoraproject.org/kojihub',
    {% endif %}

    # Where to find composes
    {% if env == 'staging' %}
    'pdcupdater.old_composes_url': 'https://kojipkgs.stg.fedoraproject.org/compose/',
    {% else %}
    'pdcupdater.old_composes_url': 'https://kojipkgs.fedoraproject.org/compose/',
    {% endif %}

    # We have an explicit list of these in the config so we can turn them on
    # and off individually in production if one is causing an issue.
    'pdcupdater.handlers': [
        'pdcupdater.handlers.pkgdb:NewPackageHandler',
        'pdcupdater.handlers.pkgdb:NewPackageBranchHandler',
        'pdcupdater.handlers.rpms:NewRPMHandler',
        'pdcupdater.handlers.compose:NewComposeHandler',
        'pdcupdater.handlers.persons:NewPersonHandler',
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
