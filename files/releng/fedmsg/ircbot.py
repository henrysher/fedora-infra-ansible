config = dict(
    irc=[
        dict(
            network='irc.freenode.net',
            port=6667,
            nickname='fedmsg-bot',
            channel='fedora-fedmsg',
            make_pretty=True,
            make_terse=True,
            # Don't show busmon or the heartbeat... gross.
            # any httpd topics would also be a huge source of spam.
            filters=dict(
                topic=['busmon', 'httpd'],
                body=['lub-dub'],
            ),
        ),
    ],
)
