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
            'mbs_user': 'mbs/mbs.fedoraproject.org',
            'tags': [
                # Temporary tags
                {
                    "from": "f29-perl",
                    "to": "f29-perl",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f29-kde",
                    "to": "f29-kde",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f29-python",
                    "to": "f29-python",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f29-granite",
                    "to": "f29-granite",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f29-boost",
                    "to": "f29-boost",
                    "key": "fedora-29",
                    "keyid": "429476b4"
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
                {
                    "from": "f28-infra-candidate",
                    "to": "f28-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },

                # Gated rawhide and branched
                {
                    "from": "f29-pending",
                    "to": "f29",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f29-modular-signing-pending",
                    "to": "f29-modular",
                    "key": "fedora-29",
                    "keyid": "429476b4",
                    "type": "modular"
                },
                {
                    "from": "f29-modular-updates-candidate",
                    "to": "f29-modular",
                    "key": "fedora-29",
                    "keyid": "429476b4",
                    "type": "modular"
                },

                # Gated bodhi updates
                {
                    "from": "f28-modular-signing-pending",
                    "to": "f28-modular-updates-testing-pending",
                    "key": "fedora-28",
                    "keyid": "9db62fb1",
                    "type": "modular"
                },
                {
                    "from": "f28-signing-pending",
                    "to": "f28-updates-testing-pending",
                    "key": "fedora-28",
                    "keyid": "9db62fb1"
                },
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
        'fedora/28/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-28'
        },
        'fedora/26/x86_64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-26'
        },
        'fedora/26/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-26'
        },
        'fedora/27/x86_64/updates/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/x86_64/testing/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/x86_64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/ppc64le/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/aarch64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/x86_64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/ppc64le/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/aarch64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/27/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-27'
        },
        'fedora/28/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/ppc64le/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/aarch64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/x86_64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/ppc64le/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/aarch64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/x86_64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/ppc64le/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/aarch64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/rawhide/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-29'
        },
        'fedora/28/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/x86_64/updates/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/28/x86_64/testing/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-28'
        },
        'fedora/rawhide/ppc64le/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-29'
        },
        'fedora/rawhide/aarch64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-29'
        },
        'fedora/rawhide/x86_64/workstation': {
            'directory': '/mnt/fedora_koji/koji/compose/atomic/repo/',
            'key': 'fedora-29'
        },
    }
}
