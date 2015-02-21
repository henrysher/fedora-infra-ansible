{% if env == 'staging' %}
domain = "stg.fedoraproject.org"
ircnick = "fedora-notifstg"
{% else %}
domain = "fedoraproject.org"
ircnick = "fedora-notifs"
{% endif %}

base = "https://apps.%s/notifications/" % domain

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

    # Auto create accounts for new packagers.
    "fmn.autocreate": True,

    # Just drop these topics without considering any preferences.  They are noise that just clog us up.
    "fmn.junk_suffixes": [
        '.buildsys.package.list.change',
        '.buildsys.tag',
        '.buildsys.untag',
        '.buildsys.repo.init',
        '.buildsys.repo.done',
        '.buildsys.rpm.sign',
    ],

    # This sets up four threads to handle incoming messages.  At the time of
    # this commit, all of our fedmsg daemons are running in single-threaded
    # mode.  If we turn it on globally, we should remove this setting.
    "moksha.workers_per_consumer": 3,
    "moksha.threadpool_size": 12,

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": True,
    {% if env == 'staging' %}
    "fmn.rules.utils.pkgdb_url": "https://admin.stg.fedoraproject.org/pkgdb/api",
    {% else %}
    "fmn.rules.utils.pkgdb_url": "http://pkgdb01.phx2.fedoraproject.org/pkgdb/api",
    {% endif %}
    "fmn.rules.cache": {
        "backend": "dogpile.cache.dbm",
        # 56700 is 16 hours.. a really long time.
        # As of this commit:  http://da.gd/oZBe that should be okay, because our
        # backend should intelligently invalidate its pkgdb2 cache if it
        # receives a pkgdb2 message.
        "expiration_time": 56700,
        "arguments": {
            "filename": "/dev/shm/fmn-cache.dbm",
            "lock_factory": MutexLock,  # Use on-disk cache but in-memory lock.
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
    "fmn.irc.network": "irc.freenode.net",
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
