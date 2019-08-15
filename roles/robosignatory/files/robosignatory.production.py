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
                    "from": "f32-python",
                    "to": "f32-python",
                    "key": "fedora-32",
                    "keyid": "12c944d0"
                },
                {
                    "from": "f31-kde",
                    "to": "f31-kde",
                    "key": "fedora-31",
                    "keyid": "3c3359c4"
                },
                {
                    "from": "f31-python",
                    "to": "f31-python",
                    "key": "fedora-31",
                    "keyid": "3c3359c4"
                },
                {
                    "from": "f30-kde",
                    "to": "f30-kde",
                    "key": "fedora-30",
                    "keyid": "cfc659b9"
                },
                {
                    "from": "f29-kde",
                    "to": "f29-kde",
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
                    "from": "epel8-infra-candidate",
                    "to": "epel8-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f29-infra-candidate",
                    "to": "f29-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },
                {
                    "from": "f30-infra-candidate",
                    "to": "f30-infra-stg",
                    "key": "fedora-infra",
                    "keyid": "47dd8ef9"
                },

                # Gated coreos-pool tag
                {
                    "from": "f29-coreos-signing-pending",
                    "to": "coreos-pool",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "f30-coreos-signing-pending",
                    "to": "coreos-pool",
                    "key": "fedora-30",
                    "keyid": "cfc659b9"
                },
                {
                    "from": "f31-coreos-signing-pending",
                    "to": "coreos-pool",
                    "key": "fedora-31",
                    "keyid": "3c3359c4"
                },
                {
                    "from": "f32-coreos-signing-pending",
                    "to": "coreos-pool",
                    "key": "fedora-32",
                    "keyid": "12c944d0"
                },

                # Gated rawhide and branched
                {
                    "from": "f32-updates-candidate",
                    "to": "f32-updates-testing-pending",
                    "key": "fedora-32",
                    "keyid": "12c944d0"
                },
                {
                    "from": "f32-pending",
                    "to": "f32",
                    "key": "fedora-32",
                    "keyid": "12c944d0"
                },
                {
                    "from": "f32-modular-pending",
                    "to": "f32-modular",
                    "key": "fedora-32",
                    "keyid": "12c944d0",
                    "type": "modular"
                },
                {
                    "from": "f32-modular-updates-candidate",
                    "to": "f32-modular",
                    "key": "fedora-32",
                    "keyid": "12c944d0",
                    "type": "modular"
                },
                {
                    "from": "f31-signing-pending",
                    "to": "f31-updates-testing-pending",
                    "key": "fedora-31",
                    "keyid": "3c3359c4"
                },
                {
                    "from": "f31-modular-signing-pending",
                    "to": "f31-modular-updates-testing-pending",
                    "key": "fedora-31",
                    "keyid": "3c3359c4",
                    "type": "modular"
                },
                {
                    "from": "f31-pending",
                    "to": "f31",
                    "key": "fedora-31",
                    "keyid": "3c3359c4"
                },
                {
                    "from": "f31-modular-pending",
                    "to": "f31-modular",
                    "key": "fedora-31",
                    "keyid": "3c3359c4",
                    "type": "modular"
                },
                {
                    "from": "f31-modular-updates-candidate",
                    "to": "f31-modular",
                    "key": "fedora-31",
                    "keyid": "3c3359c4",
                    "type": "modular"
                },

                # Gated bodhi updates
                {
                    "from": "f30-signing-pending",
                    "to": "f30-updates-testing-pending",
                    "key": "fedora-30",
                    "keyid": "cfc659b9"
                },
                {
                    "from": "f30-modular-signing-pending",
                    "to": "f30-modular-updates-testing-pending",
                    "key": "fedora-30",
                    "keyid": "cfc659b9",
                    "type": "modular"
                },
                {
                    "from": "f29-modular-signing-pending",
                    "to": "f29-modular-updates-testing-pending",
                    "key": "fedora-29",
                    "keyid": "429476b4",
                    "type": "modular"
                },
                {
                    "from": "f29-signing-pending",
                    "to": "f29-updates-testing-pending",
                    "key": "fedora-29",
                    "keyid": "429476b4"
                },
                {
                    "from": "epel8-signing-pending",
                    "to": "epel8-testing-pending",
                    "key": "epel-8",
                    "keyid": "2f86d6a1"
                },
                {
                    "from": "epel8-playground-pending",
                    "to": "epel8-playground",
                    "key": "epel-8",
                    "keyid": "2f86d6a1"
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
            ],
        },
    },

    'robosignatory.ostree_refs': {
        'fedora/rawhide/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/rawhide/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/rawhide/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/devel/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/devel/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/devel/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/stable/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/stable/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/stable/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-iot-2019'
        },
        'fedora/31/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-31'
        },
        'fedora/30/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-30'
        },
        'fedora/30/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-30'
        },
        'fedora/30/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-30'
        },
        'fedora/29/x86_64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/aarch64/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/armhfp/iot': {
            'directory': '/mnt/fedora_koji/koji/compose/iot/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/ppc64le/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/aarch64/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/ppc64le/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/aarch64/updates/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/ppc64le/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/aarch64/testing/atomic-host': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/updates/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/29/x86_64/testing/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-29'
        },
        'fedora/30/x86_64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-30'
        },
        'fedora/30/x86_64/updates/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-30'
        },
        'fedora/30/x86_64/testing/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-30'
        },
        'fedora/31/x86_64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/aarch64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/ppc64le/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/x86_64/updates/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-31'
        },
        'fedora/31/x86_64/testing/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-31'
        },
        'fedora/rawhide/aarch64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-32'
        },
        'fedora/rawhide/ppc64le/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-32'
        },
        'fedora/rawhide/x86_64/silverblue': {
            'directory': '/mnt/fedora_koji/koji/compose/ostree/repo/',
            'key': 'fedora-32'
        },
    }
}
