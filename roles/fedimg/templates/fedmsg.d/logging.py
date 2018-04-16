# Setup fedmsg logging.
# See the following for constraints on this format https://bit.ly/Xn1WDn
config = dict(
    logging=dict(
        loggers=dict(
            fedimg={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console"],
            },
        ),
    ),
)
