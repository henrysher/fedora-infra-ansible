import socket

hostname = socket.gethostname().split('.', 1)[0]
config = {
    'sign_messages': True,
    'active': True,
    'cert_prefix': 'fedmsg-migration-tools',
    'certnames': {'fedmsg-migration-tools.{}'.format(socket.gethostname()): 'fedmsg-migration-tools'},
    'relay_inbound': 'tcp://busgateway01{{ env_suffix }}.phx2.fedoraproject.org:9941',
{% if env == 'staging' %}
# stg should listen to the stg bus
    'endpoints': {
        'staging_gateway': ['tcp://stg.fedoraproject.org:9940']
    },
    'environment': 'stg',
{% else %}
    'environment': 'prod',
{% endif %}
    "validate_signatures": True,
    "crypto_backend": 'x509',
    "crypto_validate_backends": ['x509'],
    "ssldir": "/opt/app-root/etc/pki/fedmsg",
    "crl_location": "https://fedoraproject.org/fedmsg/crl.pem",
    "crl_cache": "/tmp/fedmsg/crl.pem",
    "crl_cache_expiry": 3600,
    "ca_cert_location": "https://fedoraproject.org/fedmsg/ca.crt",
    "ca_cert_cache": "/tmp/fedmsg/ca.crt",
    "ca_cert_cache_expiry": 0,  # Never expires
    # A mapping of fully qualified topics to a list of cert names for which
    # a valid signature is to be considered authorized.  Messages on topics not
    # listed here are considered automatically authorized.
    # ** policy dynamically generated from inventory vars
    # See ansible/filter_plugins/fedmsg.py for this inversion filter.
    "routing_policy": {
    {% for topic, certs in groups | invert_fedmsg_policy(hostvars, env) %}
        "{{topic}}": [
    {% for cert in certs %}
        "{{ cert }}",
{% endfor %}
"fedmsg-migration-tools-fedmsg-migration-tools{{env_suffix}}.fedoraproject.org",
        ],
{% endfor %}
    },
    # Set this to True if you want messages to be dropped that aren't
    # explicitly whitelisted in the routing_policy.
    # When this is False, only messages that have a topic in the routing_policy
    # but whose cert names aren't in the associated list are dropped; messages
    # whose topics do not appear in the routing_policy are not dropped.
    "routing_nitpicky": False,
    # Logging
    "logging": {
        "version": 1,
        "loggers": {
            "fedmsg_migration_tools": {
                "handlers": ["console"], "propagate": False, "level": "DEBUG"},
            "fedmsg": {
                "handlers": ["console"], "propagate": False, "level": "DEBUG"},
            "moksha": {
                "handlers": ["console"], "propagate": False, "level": "DEBUG"},
        },
        "handlers": {
            "console": {
                "formatter": "bare",
                "class": "logging.StreamHandler",
                "stream": "ext://sys.stdout",
                "level": "DEBUG"
            }
        },
        "formatters": {
            "bare": {
                "datefmt": "%Y-%m-%d %H:%M:%S",
                "format": "[%(asctime)s][%(name)10s %(levelname)7s] %(message)s"
            },
        },
    },
}
