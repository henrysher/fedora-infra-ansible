config = {
    'robosignatory.enabled.tagsigner': True,
    'robosignatory.signing.user': 'autopen',
    'robosignatory.signing.passphrase_file': '/etc/sigul/autosign.pass',
    'robosignatory.signing.config_file': '/etc/sigul/client.conf',

    # The keys here need to be the same in the sigul bridge
    'robosignatory.koji_instances': {
        'primary': {
            'url': 'https://koji.fedoraproject.org/kojihub',
            'options': {
                # Only ssl is supported at the moment
                'authmethod': 'ssl',
                'cert': '/etc/sigul/autopen.pem',
                'serverca': '/etc/sigul/fedoraca.pem',
            },
            'tags': [
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
                    "from": "f26-pending",
                    "to": "f26",
                    "key": "fedora-26",
                    "keyid": "64dab85d"
                }
            ]
        },
    },
}
