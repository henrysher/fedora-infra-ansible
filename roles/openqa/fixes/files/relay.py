config = dict(
    endpoints={
        # This is the output side of the relay to which all other
        # services can listen.
        "relay_outbound": [
            "tcp://127.0.0.1:4001",
        ],
    },
    relay_inbound=[
        
        # Stuff from the cloud has to go through our external proxy first..
        #"tcp://hub.fedoraproject.org:9941",

        # ...and normally, we'd like them to go through round-robin, but we're
        # not getting messages in from proxies across the vpn.  So, only use
        # proxy01 for now.
        "tcp://209.132.181.16:9941",
            ],
)
