# This should get merged smartly with the site-wide fedmsg.d/logging.py we have
# installed everywhere.
config = dict(
    logging=dict(
        loggers=dict(
            bodhi={
                "level": "DEBUG",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
            sqlalchemy={
                "level": "WARN",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
            root={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
        ),
    ),
)
