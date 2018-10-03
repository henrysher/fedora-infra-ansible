suffix = 'phx2.fedoraproject.org'
non_phx_suffix = 'fedoraproject.org'

config = dict(
    # This is a dict of possible addresses from which fedmsg can send
    # messages.  fedmsg.init(...) requires that a 'name' argument be passed
    # to it which corresponds with one of the keys in this dict.
    endpoints = {
        # This is the output side of the relay to which all other
        # services can listen.
        "relay_outbound": [
            "tcp://busgateway01.%s:3999" % suffix,
        ],

        # For other, more 'normal' services, fedmsg will try to guess the
        # name of it's calling module to determine which endpoint definition
        # to use.  This can be overridden by explicitly providing the name in
        # the initial call to fedmsg.init(...).
        "bodhi.app01": [
            "tcp://app01.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "bodhi.app02": [
            "tcp://app02.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "bodhi.branched-composer": [
            "tcp://branched-composer.%s:3000" % suffix
        ],
        "bodhi.rawhide-composer": [
            "tcp://rawhide-composer.%s:3000" % suffix
        ],
        "bodhi.app03": [
            "tcp://app03.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "bodhi.app04": [
            "tcp://app04.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "bodhi.app05": [
            "tcp://app05.%s:300%i" % (non_phx_suffix, i)
            for i in range(8)
        ],
        "bodhi.app07": [
            "tcp://app07.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "bodhi.app08": [
            "tcp://app08.%s:300%i" % (non_phx_suffix, i)
            for i in range(8)
        ],
        "bodhi.releng04": [
            "tcp://releng04.%s:3000" % suffix
        ],
        "bodhi.relepel01": [
            "tcp://relepel01.%s:3000" % suffix
        ],
        "fas.fas01": [
            "tcp://fas01.%s:300%i" % (suffix, i)
            for i in range(8)
        ],
        "busmon.app01": [
            "tcp://app01.%s:3008" % suffix,
        ],
        "busmon.app02": [
            "tcp://app02.%s:3008" % suffix,
        ],
        "supybot.value03": [
            "tcp://value03.%s:3000" % suffix,
        ],
    },

    # This is the address of an active->passive relay.  It is used for the
    # fedmsg-logger command which requires another service with a stable
    # listening address for it to send messages to.
    # It is also used by the git-hook, for the same reason.
    # It is also used by the mediawiki php plugin which, due to the oddities of
    # php, can't maintain a single passive-bind endpoint of it's own.
    relay_inbound="tcp://busgateway01.%s:9941" % suffix,
)
