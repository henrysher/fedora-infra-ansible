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
}
