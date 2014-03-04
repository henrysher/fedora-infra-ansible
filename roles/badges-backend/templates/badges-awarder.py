config = {
    # We need to tell the fedmsg-hub that it should load our consumer on start.
    "fedmsg.consumers.badges.enabled": True,

    # This tells the consumer where to look for its BadgeRule definitions.  It
    # may be a relative or an absolute path on the file system.
    "badges.yaml.directory": "/usr/share/badges/rules",

    # This is a dictionary of tahrir-related configuration
    "badges_global": {

        # This is a sqlalchemy URI that points to the tahrir DB.
        "database_uri": "postgresql://{{tahrirDBUser}}:{{tahrirDBPassword}}@db-tahrir/tahrir",

        # This is a set of data that tells our consumer what Open Badges Issuer
        # should be kept as the issuer of all the badges we create.
        "badge_issuer": dict(
            issuer_id='Fedora Project',
            issuer_origin='https://apps.fedoraproject.org',
            issuer_name='Fedora Project',
            issuer_org='http://fedoraproject.org',
            issuer_contact='badges@fedoraproject.org',
        ),
    },

    # The badges backend (fedmsg-hub) uses this to build a fas cache of ircnicks
    # to fas usernames so it can act appropriately on certain message types.
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
    },

    # Stuff used for caching packagedb relations.
    "fedbadges.rules.utils.use_pkgdb2": False,
    "fedbadges.rules.utils.pkgdb_url": "https://admin.fedoraproject.org/pkgdb",
    #"fedbadges.rules.utils.pkgdb_url": "http://209.132.184.188/api/",
    "fedbadges.rules.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/fedbadges-cache.dbm",
        },
    },
}
