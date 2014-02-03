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

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": False,
    "fmn.rules.utils.pkgdb2_api_url": "http://209.132.184.188/api/",
    "fmn.rules.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 300,
        "arguments": {
            "filename": "/var/tmp/fmn-cache.dbm",
        },
    },

    # The notification backend uses this to build a fas cache of ircnicks
    # to fas usernames so it can act appropriately on certain message types.
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
    },

    ## Backend stuff ##
    # Email
    "fmn.email.mailserver": "bastion01.phx2.fedoraproject.org:25",
    "fmn.email.from_address": "notifications@" + domain,

    # IRC
    "fmn.irc.network": "chat.freenode.net",
    "fmn.irc.nickname": ircnick,
    "fmn.irc.port": 6667,
    "fmn.irc.timeout": 120,

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
                "handlers": ["console"],
            },
        ),
    ),
}
