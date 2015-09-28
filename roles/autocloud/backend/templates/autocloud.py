config = {
    # Consumer stuff
    "autocloud.consumer.enabled": True,
{% if env == 'staging' %}
    "autocloud.sqlalchemy.uri": "postgres://autocloud:{{autocloud_db_password_stg}}@db01.stg/autocloud",
{% else %}
    "autocloud.sqlalchemy.uri": "postgres://autocloud:{{autocloud_db_password}}@db01/autocloud",
{% endif %}

    # Turn on logging for autocloud
    "logging": dict(
        loggers=dict(
            autocloud={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}

