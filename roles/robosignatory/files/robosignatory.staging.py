config = {
    'logging': {
        'loggers': {
            'robosignatory': {
                'handlers': ['console', 'mailer'],
                'level': 'DEBUG',
                'propagate': False
            },
        },
    },

    'robosignatory.enabled.tagsigner': True,
    'robosignatory.enabled.atomicsigner': True,

    # Any tag prefixed with "module-" will be considered a module.
    'robosignatory.module_prefixes': ['module-'],


    'robosignatory.signing': {
        'backend': 'sigul',
        'user': 'autopen',
        'passphrase_file': '/etc/sigul/autosign.pass',
        'config_file': '/etc/sigul/client.conf'
    },

    # The keys here need to be the same in the sigul bridge
    'robosignatory.koji_instances': {
        'primary': {
            'url': 'https://koji.stg.fedoraproject.org/kojihub',
            'options': {
                # Only ssl is supported at the moment
                'authmethod': 'kerberos',
                'principal': 'autosign/autosign01.stg.phx2.fedoraproject.org@STG.FEDORAPROJECT.ORG',
                'keytab': '/etc/krb5.autosign_autosign01.stg.phx2.fedoraproject.org.keytab',
                'krb_rdns': False
            },
            'mbs_user': 'mbs/mbs.stg.fedoraproject.org',
            'tags': [
                # Temporary tags
                # Infra tags
                # Gated coreos-pool tag
                # Gated rawhide and branched
                {
                    "from": "epel8-signing-pending",
                    "to": "epel8-testing-pending",
                    "key": "testkey",
                    "keyid": "d300e724"
                },
                {
                    "from": "f31-updates-candidate",
                    "to": "f31-updates-testing-pending",
                    "key": "testkey",
                    "keyid": "d300e724"
                },
                # Gated bodhi updates
                # Non-gated bodhi triggered
            ],
        },
    },

    'robosignatory.ostree_refs': {
        'fedora/rawhide/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
    }
}
