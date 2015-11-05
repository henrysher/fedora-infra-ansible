import datetime


config = {
    "statscache.datagrepper.profile": False,
    {% if env == 'staging' %}
    #"statscache.datagrepper.endpoint": "https://apps.stg.fedoraproject.org/datagrepper/raw",

    # Consume production fedmsg data in staging for now.
    "statscache.datagrepper.endpoint": "https://apps.fedoraproject.org/datagrepper/raw",
    "endpoints": {
        "production-loopback": [
            "tcp://10.5.126.51:9940",
        ],
    },

    {% else %}
    "statscache.datagrepper.endpoint": "https://apps.fedoraproject.org/datagrepper/raw",
    {% endif %}

    # Consumer stuff
    "statscache.consumer.enabled": True,

    "statscache.sqlalchemy.uri": "postgres://statscache:{{statscache_db_password}}@db01/statscache",

    # stats models will go back at least this far (current value arbitrary)
    {% if env == 'staging' %}
    "statscache.consumer.epoch": datetime.datetime(year=2015, month=10, day=1),
    {% else %}
    "statscache.consumer.epoch": datetime.datetime(year=2014, month=1, day=1),
    {% endif %}

    # stats models are updated at this frequency
    "statscache.producer.frequency": datetime.timedelta(seconds=1),

    # Configuration of web API
    "statscache.app.maximum_rows_per_page": 100,
    "statscache.app.default_rows_per_page": 100,

    # Turn on logging for statscache
    "logging": dict(
        loggers=dict(
            statscache={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
            statscache_plugins={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
}
