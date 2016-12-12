config = {
    # This is just a key to tell the fedmsg-hub to initialize us.
    'summershum.enabled': True,
    'summershum.sqlalchemy.url': 'postgresql://{{summershum_db_user}}:{{summershum_db_password}}@db-summershum/summershum',
    'summershum.lookaside': 'http://src.fedoraproject.org/lookaside/pkgs/',
    'summershum.datagrepper': 'https://apps.fedoraproject.org/datagrepper/',

    'logging': {
        'loggers': {
            'summershum': {
                'handlers': ['console', 'mailer'],
                'level': 'DEBUG',
                'propagate': False
            },
        },
    },
}
