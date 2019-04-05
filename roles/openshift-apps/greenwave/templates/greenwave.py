import socket

config = dict(
    sign_messages=True,
    active=True,
    cert_prefix="greenwave",
    certnames={
      "greenwave." + socket.gethostname(): "greenwave",
    },

    logging={
      "loggers": {
          "greenwave": {
              "handlers": ["console"], "propagate": False, "level": "DEBUG"},
          "fedmsg": {
              "handlers": ["console"], "propagate": False, "level": "DEBUG"},
          "moksha": {
              "handlers": ["console"], "propagate": False, "level": "DEBUG"},
          "requests": {
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
    },

    greenwave_cache={
      'backend': 'dogpile.cache.memcached',
      'expiration_time': 3600, # 3600 is 1 hour
      'arguments': {
          'url': 'greenwave-memcached:11211',
          'distributed_lock': True
      }
    },
    resultsdb_topic_suffix="resultsdb.result.new",

    {% if env == 'staging' %}
    environment='stg',
    relay_inbound=["tcp://busgateway01.stg.phx2.fedoraproject.org:9941"],
    greenwave_api_url='https://greenwave-web-greenwave.app.os.stg.fedoraproject.org/api/v1.0',
    # STG greenwave should listen to the STG bus.
    endpoints=dict(
        staging_gateway=[
            'tcp://stg.fedoraproject.org:9940',
        ],
    ),
    {% else %}
    environment='prod',
    relay_inbound=["tcp://busgateway01.phx2.fedoraproject.org:9941"],
    greenwave_api_url='https://greenwave-web-greenwave.app.os.fedoraproject.org/api/v1.0'
    {% endif %}
)
