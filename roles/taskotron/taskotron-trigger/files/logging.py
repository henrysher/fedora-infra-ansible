# Setup fedmsg logging.
# See the following for constraints on this format http://bit.ly/Xn1WDn
bare_format = "[%(asctime)s][%(name)10s %(levelname)7s] %(message)s"

config = dict(
    logging=dict(
        version=1,
        formatters=dict(
            bare={
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": bare_format
            },
        ),
        handlers=dict(
            console={
                "class": "logging.StreamHandler",
                "formatter": "bare",
                "level": "INFO",
                "stream": "ext://sys.stdout",
            },
            filelog={
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "bare",
                "level": "INFO",
                "filename": "/var/log/fedmsg/taskotron-trigger.log",
                "mode": "a",
                          }
        ),
        loggers=dict(
            fedmsg={
                "level": "INFO",
                "propagate": False,
                "handlers": ["filelog"],
            },
            moksha={
                "level": "INFO",
                "propagate": False,
                "handlers": ["filelog"],
            },
        ),
    ),
)
