config = {
    # We need to tell the fedmsg-hub that it should load our consumer on start.
    "fedmsg.consumers.badges.enabled": True,

    # This sets up four threads to handle incoming messages.  At the time of
    # this commit, all of our fedmsg daemons are running in single-threaded
    # mode.  If we turn it on globally, we should remove this setting.
    "moksha.workers_per_consumer": 8,
    "moksha.threadpool_size": 20,

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
    {% if env == 'staging' %}
        "base_url": "https://admin.stg.fedoraproject.org/accounts/",
    {% endif %}
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
    },

    # Stuff used for caching packagedb relations.
    "fedbadges.rules.utils.use_pkgdb2": True,
    {% if env == 'staging' %}
    "fedbadges.rules.utils.pkgdb_url": "https://admin.stg.fedoraproject.org/pkgdb/api",
    {% else %}
    "fedbadges.rules.utils.pkgdb_url": "https://admin.fedoraproject.org/pkgdb/api",
    {% endif %}
    "fedbadges.rules.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/fedbadges-cache.dbm",
        },
    },
}
