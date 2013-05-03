
config = dict(
    # Set this to dev if you're hacking on fedmsg or an app locally.
    # Set to stg or prod if running in the Fedora Infrastructure.
    environment="prod",

    # Default is 0
    high_water_mark=0,
    io_threads=1,

    # We almost always want the fedmsg-hub to be sending messages with zmq as
    # opposed to amqp or stomp.  The only exception will be the bugzilla
    # amqp<->zmq bridge service.
    zmq_enabled=True,

    # When subscribing to messages, we want to allow splats ('*') so we tell the
    # hub to not be strict when comparing messages topics to subscription
    # topics.
    zmq_strict=False,
)
