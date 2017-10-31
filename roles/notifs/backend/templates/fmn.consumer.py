{% if env == 'staging' %}
domain = "stg.fedoraproject.org"
ircnick = "fedora-notifstg"
{% else %}
domain = "fedoraproject.org"
ircnick = "fedora-notif"
{% endif %}

base = "https://apps.%s/notifications/" % domain

{% if env != 'staging' %}

from dogpile.core.readwrite_lock import ReadWriteMutex
from dogpile.cache.backends.file import AbstractFileLock

class MutexLock(AbstractFileLock):
    """ Use an in-memory lock for our dogpile cache
    in an attempt to reduce thread competition.
    """
    def __init__(self, filename):
        self.mutex = ReadWriteMutex()

    def acquire_read_lock(self, wait):
        ret = self.mutex.acquire_read_lock(wait)
        return wait or ret

    def acquire_write_lock(self, wait):
        ret = self.mutex.acquire_write_lock(wait)
        return wait or ret

    def release_read_lock(self):
        return self.mutex.release_read_lock()

    def release_write_lock(self):
        return self.mutex.release_write_lock()

    @classmethod
    def __json__(cls):
        return repr(cls)
{% endif %}


config = {
    {% if env == 'staging' %}
    # Pull in messages from production so we can more thoroughly test in stg.
    "endpoints": {
        "loopback-from-production": [
            "tcp://hub.fedoraproject.org:9940",
            "tcp://fedmsg-relay.ci.centos.org:9940",
        ],
    },
    {% else %}
    "endpoints": {
        "centos_ci_relay": [
            "tcp://fedmsg-relay.ci.centos.org:9940",
        ],
    },
    {% endif %}

    {% if env == 'staging' %}
    "fmn.topics": [b'org.fedoraproject.*', b'org.centos.*'],
    {% else %}
    "fmn.topics": [b'org.fedoraproject.prod.*', b'org.centos.prod.*'],
    {% endif %}

    # Consumer stuff
    "fmn.consumer.enabled": True,
    "fmn.sqlalchemy.uri": "postgresql://{{notifs_db_user}}:{{notifs_db_password}}@db-notifs/notifications",

    {% if env != 'staging' %}
    # Auto create accounts for new packagers.
    "fmn.autocreate": True,
    {% else %}
    # Don't auto create accounts for new packagers in staging.
    "fmn.autocreate": False,
    {% endif %}

    # Ignore rubygems coprs
    "ignored_copr_owners": ["@rubygems"],

    # Just drop these topics without considering any preferences.  They are noise that just clog us up.
    "fmn.junk_suffixes": [
        '.buildsys.package.list.change',
        '.buildsys.tag',
        '.buildsys.untag',
        '.buildsys.repo.init',
        '.buildsys.repo.done',
        '.buildsys.rpm.sign',
        '.faf.report.threshold1',
        '.github.status',
    ],

    # This sets up four threads to handle incoming messages.  At the time of
    # this commit, all of our fedmsg daemons are running in single-threaded
    # mode.  If we turn it on globally, we should remove this setting.
    "moksha.workers_per_consumer": 3,
    "moksha.threadpool_size": 12,

    # Some configuration for the rule processors
    {% if env == 'staging' %}
    "fmn.rules.utils.use_pkgdb2": False,
    'fmn.rules.utils.use_pagure_for_ownership': True,
    'fmn.rules.utils.pagure_api_url': 'https://src.stg.fedoraproject.org/api/',
    "fmn.rules.utils.pkgdb_url": "https://admin.stg.fedoraproject.org/pkgdb/api",
    {% else %}
    "fmn.rules.utils.use_pkgdb2": False,
    'fmn.rules.utils.use_pagure_for_ownership': True,
    'fmn.rules.utils.pagure_api_url': 'https://src.fedoraproject.org/api/',
    "fmn.rules.utils.pkgdb_url": "http://pkgdb01.phx2.fedoraproject.org/pkgdb/api",
    {% endif %}
    "fmn.rules.cache": {
	"backend": "dogpile.cache.redis",
        "arguments": {
            "host": "localhost",
            "port": 6379,
            "db": 0,
            "redis_expiration_time": 60*60*2,   # 2 hours
            "distributed_lock": True
        },
    },

    # The notification backend uses this to build a fas cache of ircnicks
    # to fas usernames so it can act appropriately on certain message types.
    {% if env == 'staging' -%}
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
        "base_url": "https://admin.stg.fedoraproject.org/accounts",
    },
    {% else -%}
    "fas_credentials": {
        "username": "{{fedoraDummyUser}}",
        "password": "{{fedoraDummyUserPassword}}",
    },
    {% endif %}


    ## Backend stuff ##
    {% if env == 'staging' %}
    "fmn.backends": ["email", "irc", "android"],
    {% else %}
    "fmn.backends": ["email", "irc"],  # android is disabled.
    {% endif %}

    # Email
    "fmn.email.mailserver": "bastion01.phx2.fedoraproject.org:25",
    "fmn.email.from_address": "notifications@" + domain,

    # IRC
    "fmn.irc.network": "irc.freenode.net",
    "fmn.irc.nickname": ircnick,
    "fmn.irc.timeout": 120,
    "fmn.irc.port": 6697,
    "fmn.irc.use_ssl": True,
    {% if env == 'staging' %}
    "fmn.irc.nickserv_pass": "{{fedora_notifstg_freenode_pass}}",
    {% else %}
    "fmn.irc.nickserv_pass": "{{fedora_notif_freenode_pass}}",
    {% endif %}

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
        "anitya": "light cyan",
        "fmn": "light blue",
        "hotness": "light green",
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
    {% if env == 'staging' %}
    "logging": dict(
        loggers=dict(
            fmn={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
        ),
        root={
            'level': 'INFO',
             'handlers': ['console', 'mailer'],
        },
    ),
    {% else %}
    "logging": dict(
        loggers=dict(
            fmn={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
        ),
    ),
    {% endif %}
}
