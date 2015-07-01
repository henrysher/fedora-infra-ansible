config = dict(
    irc=[
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-stg',
            {% else %}
            nickname='fedmsg-bot',
            {% endif %}
            channel='fedora-fedmsg',

            filters=dict(
                topic=[
                    # Ignore some of the koji spamminess
                    'buildsys.repo.init',
                    'buildsys.repo.done',
                    'buildsys.untag',
                    'buildsys.tag',
                    # And some of the FAF/ABRT spamminess
                    'faf.report.threshold1',
                    'faf.problem.threshold1',
                ],
                body=[],
            ),
        ),

        # For fedora-apps
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-apps-s',
            {% else %}
            nickname='fedmsg-apps',
            {% endif %}
            channel='fedora-apps',
            filters=dict(
                topic=[
                    '^((?!(github\.create|github\.issue\.|github\.pull_request\.|github\.commit_comment|github\.star|pagure)).)*$',
                ],
                body=[
                    "^((?!(fedora-infra|u'name': u'pagure')).)*$",
                ],
            ),
        ),

        # For fedora-hubs (not fedora-apps)
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-hubs-s',
            {% else %}
            nickname='fedmsg-hubs',
            {% endif %}
            channel='fedora-hubs',
            filters=dict(
                topic=[
                    '^((?!(github\.create|github\.issue\.|github\.pull_request\.|github\.commit_comment|github\.star|pagure)).)*$',
                ],
                body=[
                    "^((?!(fedora-hubs)).)*$",
                ],
            ),
        ),

        # For that commops crew!
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='commopsbot-s',
            {% else %}
            nickname='commopsbot',
            {% endif %}
            channel='fedora-commops',
            filters=dict(
                topic=[
                    '^((?!(planet)).)*$',
                ],
            ),
        ),

        # Just for the Ask Fedora crew in #fedora-ask
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-ask-stg',
            {% else %}
            nickname='fedmsg-ask',
            {% endif %}
            channel='fedora-ask',
            # Only show AskFedora messages
            filters=dict(
                topic=['^((?!askbot).)*$'],
            ),
        ),

        # Show only pkgdb retirement msgs and compose msgs to the releng crew.
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-releng-s',
            {% else %}
            nickname='fedmsg-releng',
            {% endif %}
            channel='fedora-releng',
            filters=dict(
                topic=[
                    '^((?!(pkgdb\.package\.update\.status|compose.branched.complete|compose.branched.start|compose.rawhide.complete|compose.rawhide.start|bodhi.updates.|trac.git.receive)).)*$',
                ],
                body=[
                    "^((?!(u'status': u'Retired'|u'prev_status': u'Retired'|compose|bodhi\.updates\.|\/srv\/git\/releng)).)*$",
                ],
            ),
        ),

        # The proyectofedora crew wants trac messages.
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-pfi-stg',
            {% else %}
            nickname='fedmsg-pfi',
            {% endif %}
            channel='#proyecto-fedora',
            # If the word proyecto appears in any message, forward it.
            filters=dict(
                body=['^((?!proyecto).)*$'],
            ),
        ),

        # Similarly for #fedora-latam.
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-latam-stg',
            {% else %}
            nickname='fedmsg-latam',
            {% endif %}
            channel='#fedora-latam',
            # If the word fedora-latam appears in any message, forward it.
            filters=dict(
                body=['^((?!fedora-latam).)*$'],
            ),
        ),

        # Hook up the design-team with badges messages
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-design-stg',
            {% else %}
            nickname='fedmsg-design',
            {% endif %}
            channel='#fedora-design',
            filters=dict(
                body=['^((?!(fedora-badges|design-team|fedoradesign)).)*$'],
            ),
        ),

        # And #fedora-docs wants in on the action
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,
            make_short=True,

            {% if env == 'staging' %}
            nickname='fedmsg-docs-stg',
            {% else %}
            nickname='fedmsg-docs',
            {% endif %}
            channel='#fedora-docs',
            filters=dict(
                body=['^((?!\/srv\/git\/docs).)*$'],
            ),
        ),
    ],

    ### Possible colors are ###
    # "white",
    # "black",
    # "blue",
    # "green",
    # "red",
    # "brown",
    # "purple",
    # "orange",
    # "yellow",
    # "light green",
    # "teal",
    # "light cyan",
    # "light blue",
    # "pink",
    # "grey",
    # "light grey",
    irc_color_lookup = {
        "fas": "light blue",
        "bodhi": "green",
        "git": "red",
        "fedoratagger": "brown",
        "wiki": "purple",
        "logger": "orange",
        "pkgdb": "teal",
        "buildsys": "yellow",
        "fedoraplanet": "light green",
        "trac": "pink",
        "askbot": "light cyan",
        "fedbadges": "brown",
        "fedocal": "purple",
        "copr": "red",
        "anitya": "light cyan",
        "fmn": "light blue",
        "hotness": "light green",
    },

    # This may be 'notice' or 'msg'
    irc_method='msg',
)
