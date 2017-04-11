config = dict(

    sign_messages=False,
    validate_signatures=False,

    endpoints={
        # This is the output side of the relay to which all other
        # services can listen.
        "relay_outbound": [
            "tcp://{{ copr_backend_ips[0] }}:4001",
        ],
    },

    # This is the address of an active->passive relay.  It is used for the
    # fedmsg-logger command which requires another service with a stable
    # listening address for it to send messages to.
    # It is also used by the git-hook, for the same reason.
    # It is also used by the mediawiki php plugin which, due to the oddities of
    # php, can't maintain a single passive-bind endpoint of it's own.
    relay_inbound=[
        "tcp://{{ copr_backend_ips[0] }}:2003",
    ],
)
