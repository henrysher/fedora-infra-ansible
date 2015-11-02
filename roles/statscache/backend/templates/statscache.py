import datetime


config = {
    "statscache.datagrepper.profile": False,

    # Consumer stuff
    "statscache.consumer.enabled": True,

    "statscache.sqlalchemy.uri": "postgres://statscache:{{statscache_db_password}}@db01/statscache",

    # stats models will go back at least this far (current value arbitrary)
    "statscache.consumer.epoch": datetime.datetime(year=2015, month=8, day=8),

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
