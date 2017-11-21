config = {
    'simple-koji-ci.enabled': True,

    'simple-koji-ci.koji': {
        'server': 'https://koji.stg.fedoraproject.org/kojihub',
        'weburl': 'https://koji.stg.fedoraproject.org/koji',
        # Kerberos configuration to authenticate with Koji. In development
        # environments, use `kinit <fas-name>@FEDORAPROJECT.ORG` to get a
        # Kerberos ticket and use the default settings below.
        'krb_principal': 'simple-koji-ci/simple-koji-ci-dev.fedorainfracloud.org@STG.FEDORAPROJECT.ORG',
        'krb_keytab': '/etc/krb5.simple-koji-ci_simple-koji-ci-dev.fedorainfracloud.org.keytab',
        'krb_ccache': None,
        'krb_proxyuser': None,
        'krb_sessionopts': {'timeout': 3600, 'krb_rdns': False},
        'git_url': 'https://src.stg.fedoraproject.org/rpms/{package}.git',
        'opts': {'scratch': True},
        'priority': 30,
        'target_tag': 'rawhide',

    },

    "simple-koji-ci.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/simple-koji-ci-cache.dbm",
        },
    },

    "simple-koji-ci.pagure_url" : "https://src.stg.fedoraproject.org",
    "simple-koji-ci.pagure_token" : "{{ simple_koji_ci_pagure_token_stg }}",

    # The time in seconds the-new-hotness should wait for a socket to connect
    # before giving up.
    'simple-koji-ci.connect_timeout': 15,
    # The time in seconds the-new-hotness should wait for a read from a socket
    # before giving up.
    'simple-koji-ci.read_timeout': 15,
    # The number of times the-new-hotness should retry a network request that
    # that failed for any reason (e.g. read timeout, DNS error, etc)
    'simple-koji-ci.requests_retries': 3,

    "logging": {
        "loggers": {
            "simple_koji_ci": {
                "level": "INFO",
                "propagate": True,
                "handlers": ["console"],
            },
        },
    }

}
