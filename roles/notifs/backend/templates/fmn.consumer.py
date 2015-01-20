{% if env == 'staging' %}
domain = "stg.fedoraproject.org"
ircnick = "fedora-notifstg"
{% else %}
domain = "fedoraproject.org"
ircnick = "fedora-notifs"
{% endif %}

base = "https://apps.%s/notifications/" % domain

config = {
    {% if env == 'staging' %}
    # Pull in messages from production so we can more thoroughly test in stg.
    "endpoints": {
        "loopback-from-production": [
            "tcp://hub.fedoraproject.org:9940",
        ],
    },
    {% endif %}

    # Consumer stuff
    "fmn.consumer.enabled": True,
    "fmn.sqlalchemy.uri": "postgresql://{{notifs_db_user}}:{{notifs_db_password}}@db-notifs/notifications",

    # This sets up four threads to handle incoming messages.  At the time of
    # this commit, all of our fedmsg daemons are running in single-threaded
    # mode.  If we turn it on globally, we should remove this setting.
    "moksha.workers_per_consumer": 6,
    "moksha.threadpool_size": 20,

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": True,
    {% if env == 'staging' %}
    "fmn.rules.utils.pkgdb_url": "https://admin.stg.fedoraproject.org/pkgdb/api",
    {% else %}
    "fmn.rules.utils.pkgdb_url": "https://admin.fedoraproject.org/pkgdb/api",
    {% endif %}
    "fmn.rules.cache": {
        "backend": "dogpile.cache.dbm",
        # 28800 is 8 hours.. a really long time.
        # As of this commit:  http://da.gd/oZBe that should be okay, because our
        # backend should intelligently invalidate its pkgdb2 cache if it
        # receives a pkgdb2 message.
        "expiration_time": 28800,
        "arguments": {
            "filename": "/dev/shm/fmn-cache.dbm",
        },
    },

    # The notification backend uses this to build a fas cache of ircnicks
    # to fas usernames so it can act appropriately on certain message types.
    {% if env == 'staging' %}
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
        "base_url": "https://admin.stg.fedoraproject.org/accounts",
    },
    {% else %}
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
    },
    {% endif %}


    ## Backend stuff ##
    {% if env == 'staging' %}
    "fmn.backends": ["irc", "android"],
    {% else %}
    "fmn.backends": ["email", "irc"],  # android is disabled.
    {% endif %}

    # Email
    "fmn.email.mailserver": "bastion01.phx2.fedoraproject.org:25",
    "fmn.email.from_address": "notifications@" + domain,

    # IRC
    "fmn.irc.network": "chat.freenode.net",
    "fmn.irc.nickname": ircnick,
    "fmn.irc.port": 6667,
    "fmn.irc.timeout": 120,

    # Colors:
    "irc_color_lookup": {
        "fas": "light blue",
        "bodhi": "green",
        "git": "red",
        "tagger": "brown",
        "wiki": "purple",
        "logger": "orange",
        "pkgdb": "teal",
        "buildsys": "yellow",
        "planet": "light green",
        "fmn": "purple",
    },

    # GCM - Android notifs
    "fmn.gcm.post_url": "{{ notifs_gcm_post_url }}",
    "fmn.gcm.api_key": "{{ notifs_gcm_api_key }}",

    # Confirmation urls:
    "fmn.base_url": base,
    "fmn.acceptance_url": base + "confirm/accept/{secret}",
    "fmn.rejection_url": base + "confirm/reject/{secret}",
    "fmn.support_email": "notifications@" + domain,

    # Generic stuff
    "logging": dict(
        loggers=dict(
            fmn={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
        ),
    ),
}
