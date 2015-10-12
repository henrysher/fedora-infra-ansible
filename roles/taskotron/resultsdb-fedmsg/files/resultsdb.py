config = {
    # This should switch fedmsg from passive mode to active mode
    # which instructs it to connect out to the fedmsg-relay instance described
    # in /etc/fedmsg.d/relay.py instead of binding to ports and waiting for
    # listeners.  We need this so that we can push our messages on to the
    # fedora-infra proper bus from over in the QA network.
    active=True,
}
