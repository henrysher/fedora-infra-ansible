config = {
    # This is for *our* database
    "fmn.sqlalchemy.uri": "postgresql://{{notifs_db_user}}:{{notifs_db_password}}@db-notifs/notifications",
    # And this is for the datanommer database
    "datanommer.sqlalchemy.url": "postgresql://{{datanommerDBUser}}:{{datanommerDBPassword}}@db-datanommer/datanommer",

    {% if env == 'staging' %}
    "fmn.backends": ["email", "irc", "android"],
    {% else %}
    "fmn.backends": ["email", "irc"],  # android is disabled.
    {% endif %}

    "fmn.web.default_login": "fedora_login",

    # Some configuration for the rule processors
    "fmn.rules.utils.use_pkgdb2": True,
    {% if env == 'staging' %}
    "fmn.rules.utils.pkgdb_url": "https://admin.stg.fedoraproject.org/pkgdb/api",
    {% else %}
    "fmn.rules.utils.pkgdb_url": "https://admin.fedoraproject.org/pkgdb/api",
    {% endif %}
    "fmn.rules.cache": {
        "backend": "dogpile.cache.dbm",
        "expiration_time": 3600,  # 3600 is 1 hour
        "arguments": {
            "filename": "/var/tmp/fmn-cache.dbm",
        },
    },
}
