# Override the default fedmsg logging configuration
config = {
    "logging": dict(
        loggers=dict(
            fmn={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
            moksha={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
            celery={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
            twisted={
                "level": "INFO",
                "propagate": False,
                "handlers": ["console", "mailer"],
            },
        ),
        root={
            'level': 'WARNING',
             'handlers': ['console', 'mailer'],
        },
    ),
}
