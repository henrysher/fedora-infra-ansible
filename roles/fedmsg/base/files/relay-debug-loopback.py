## WARNING ##
# This file is a replacement for the *regular* relay.py file we ship to all
# fedora infra prod/stg hosts.
# If you are seeing this file on a host, that is because it has
# fedmsg_debug_loopback set to 'true' in our ansible config.  That should be an
# exceptional thing used only for debugging.
#
# Things to know:
#
# * No 'fedmsg-logger' statements on this host will make it to the real bus
# * They will only be broadcast locally (on this box)
# * No messages from the main fedmsg-relay on our bus will make it to this box.
# * Other messages from persistent fedmsg services will make it here.
#
# You can use this to test services locally with 'fedmsg-dg-replay'.  Messages
# rebroadcast by that command will be replayed locally, to only this host.

config = dict(
    endpoints={
        "relay_outbound": [
            "tcp://127.0.0.1:3999",
        ],
    },
    relay_inbound=[
        "tcp://127.0.0.1:9941",
    ],
)
