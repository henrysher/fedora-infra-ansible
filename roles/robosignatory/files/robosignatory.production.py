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
    'robosignatory.signing.user': 'autopen',
    'robosignatory.signing.passphrase_file': '/etc/sigul/autosign.pass',
    'robosignatory.signing.config_file': '/etc/sigul/client.conf',

    # The keys here need to be the same in the sigul bridge
    'robosignatory.koji_instances': {
        'primary': {
            'url': 'https://koji.fedoraproject.org/kojihub',
            'options': {
                # Only ssl is supported at the moment
                'authmethod': 'kerberos',
                'principal': 'autosign/autosign01.phx2.fedoraproject.org@FEDORAPROJECT.ORG',
                'keytab': '/etc/krb5.autosign_autosign01.phx2.fedoraproject.org.keytab'
            },
            'tags': [
                # Temporary tags for rebuilds
                {
                    "from": "f26-ruby24",
                    "to": "f26-ruby24",
                    "key": "fedora-26",
                    "keyid": "64dab85d"
                },
                # Normal tags
                {
                    "from": "epel6-infra-candidate",
                    "to": "epel6-infra",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "epel7-infra-candidate",
                    "to": "epel7-infra",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f23-infra-candidate",
                    "to": "f23-infra",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f24-infra-candidate",
                    "to": "f24-infra",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f25-infra-candidate",
                    "to": "f25-infra",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f26",
                    "to": "f26",
                    "key": "fedora-26",
                    "keyid": "64dab85d"
                },
                {
                    "from": "f26-pending",
                    "to": "f26",
                    "key": "fedora-26",
                    "keyid": "64dab85d"
                },

                {
                    "from": "f25-updates-testing-pending",
                    "to": "f25-updates-testing-pending",
                    "key": "fedora-25",
                    "keyid": "fdb19c98"
                },
                {
                    "from": "f24-updates-testing-pending",
                    "to": "f24-updates-testing-pending",
                    "key": "fedora-24",
                    "keyid": "81b46521"
                },
                {
                    "from": "f23-updates-testing-pending",
                    "to": "f23-updates-testing-pending",
                    "key": "fedora-23",
                    "keyid": "34ec9cba"
                },
                {
                    "from": "epel7-testing-pending",
                    "to": "epel7-testing-pending",
                    "key": "epel-7",
                    "keyid": "352c64e5"
                },
                {
                    "from": "dist-6E-epel-testing-candidate",
                    "to": "dist-6E-epel-testing-candidate",
                    "key": "epel-6",
                    "keyid": "0608b895"
                },
                {
                    "from": "dist-5E-epel-testing-candidate",
                    "to": "dist-5E-epel-testing-candidate",
                    "key": "epel-5",
                    "keyid": "217521f6"
                },

                # For transitional during new bodhi release
                {
                    "from": "f25-signing-pending",
                    "to": "f25-updates-testing-pending",
                    "key": "fedora-25",
                    "keyid": "fdb19c98"
                },
                {
                    "from": "f24-signing-pending",
                    "to": "f24-updates-testing-pending",
                    "key": "fedora-24",
                    "keyid": "81b46521"
                },
                {
                    "from": "f23-signing-pending",
                    "to": "f23-updates-testing-pending",
                    "key": "fedora-23",
                    "keyid": "34ec9cba"
                },
                {
                    "from": "epel7-signing-pending",
                    "to": "epel7-testing-pending",
                    "key": "epel-7",
                    "keyid": "352c64e5"
                },
            ]
        },
    },

    'robosignatory.ostree_refs': {
        'fedora-atomic/25/x86_64/docker-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/25/',
            'key': 'fedora-25'
        },
        'fedora/25/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/25/',
            'key': 'fedora-25'
        },
        'fedora-atomic/rawhide/x86_64/docker-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/rawhide/',
            'key': 'fedora-26'
        },
        'fedora-atomic/rawhide/aarch64/docker-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/rawhide/',
            'key': 'fedora-26'
        },
        'fedora/rawhide/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/rawhide/',
            'key': 'fedora-26'
        },
    }
}
