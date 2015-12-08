config = {
    # Consumer stuff
    "bugyou.consumer.enabled": True,

    # Turn on the logging for bugyou
    "logging": dict(
        loggers=dict(
            bugyou={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ['console'],
            },
        ),
    },
}
