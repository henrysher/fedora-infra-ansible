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
            'url': 'https://koji.fedoraproject.org/kojihub',
            'options': {
                # Only ssl is supported at the moment
                'authmethod': 'kerberos',
                'principal': 'autosign/autosign01.phx2.fedoraproject.org@FEDORAPROJECT.ORG',
                'keytab': '/etc/krb5.autosign_autosign01.phx2.fedoraproject.org.keytab',
                'krb_rdns': False
            },
            'module_key': 'fedora-modularity',
            'module_keyid': 'a3cc4e62',
            'tags': [
                # Temporary tags
                {
                    "from": "f28-llvm",
                    "to": "f28-llvm",
                    "key": "fedora-28",
                    "keyid": "9db62fb1"
                },
                {
                    "from": "f27-gnome",
                    "to": "f27-gnome",
                    "key": "fedora-27",
                    "keyid": "f5282ee4"
                },

                # Infra tags
                {
                    "from": "epel6-infra-candidate",
                    "to": "epel6-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "epel7-infra-candidate",
                    "to": "epel7-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f25-infra-candidate",
                    "to": "f25-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f26-infra-candidate",
                    "to": "f26-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f27-infra-candidate",
                    "to": "f27-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },

                # Gated rawhide and branched
                {
                    "from": "f28-pending",
                    "to": "f28",
                    "key": "fedora-28",
                    "keyid": "9db62fb1"
                },

                # Gated bodhi updates
                {
                    "from": "f27-signing-pending",
                    "to": "f27-updates-testing-pending",
                    "key": "fedora-27",
                    "keyid": "f5282ee4"
                },
                {
                    "from": "f26-signing-pending",
                    "to": "f26-updates-testing-pending",
                    "key": "fedora-26",
                    "keyid": "64dab85d"
                },
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

                # Non-gated bodhi triggered
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
            ],
        },
    },

    'robosignatory.ostree_refs': {
        'fedora-atomic/25/x86_64/updates/docker-host': {
            'directory': '/mnt/fedora_koji/koji/mash/atomic/25/',
            'key': 'fedora-25'
        },
        'fedora-atomic/25/x86_64/docker-host': {
            'directory': '/mnt/fedora_koji/koji/mash/atomic/25/',
            'key': 'fedora-25'
        },
        'fedora/25/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/25/',
            'key': 'fedora-25'
        },
        'fedora/26/x86_64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/mash/atomic/26/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/mash/atomic/26/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/mash/atomic/26/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/26/',
            'key': 'fedora-26'
        },
        'fedora/27/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/27/',
            'key': 'fedora-27'
        },
        'fedora/27/ppc64le/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/27/',
            'key': 'fedora-27'
        },
        'fedora/27/aarch64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/27/',
            'key': 'fedora-27'
        },
        'fedora/27/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/27/',
            'key': 'fedora-27'
        },
        'fedora/rawhide/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/rawhide/',
            'key': 'fedora-28'
        },
        'fedora/rawhide/ppc64le/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/rawhide/',
            'key': 'fedora-28'
        },
        'fedora/rawhide/aarch64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/rawhide/',
            'key': 'fedora-28'
        },
        'fedora/rawhide/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/rawhide/',
            'key': 'fedora-28'
        },
    }
}
