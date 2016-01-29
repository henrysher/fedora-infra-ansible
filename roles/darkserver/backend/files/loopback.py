# This file is for staging only.
# It instructs all fedmsg processes on this machine to listen to the production
# bus.. as a kind of loopback.  We have this here so staging darkserver can test
# against all of the prod activity.
config = {
    'endpoints': {
        'production-loopback': [
            'tcp://hub.fedoraproject.org:9940',
        ],
    },
}
