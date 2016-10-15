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

        # For fedora-admin
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-admin',
            {% else %}
            nickname='fm-admin',
            {% endif %}
            channel='fedora-admin',
            filters=dict(
                topic=[
                    '^((?!(pagure)).)*$',
                ],
                body=[
                    "^((?!(fedora-infrastructure)).)*$",
                ],
            ),
        ),

        # For fedora-apps
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-apps',
            {% else %}
            nickname='fm-apps',
            {% endif %}
            channel='fedora-apps',
            filters=dict(
                topic=[
                    '^((?!(github\.create|github\.issue\.|github\.pull_request|github\.commit_comment|github\.star|pagure)).)*$',
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
            nickname='fn-stg-hubs',
            {% else %}
            nickname='fm-hubs',
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
                    '^((?!(planet|fedora_elections|meetbot\.meeting\.item\.help|meetbot\.meeting\.complete|fedocal\.meeting\.new|fedocal\.meeting\.update|fedocal\.meeting\.delete|fedocal\.calendar|pagure\.project\.new|askbot\.post\.flag_offensive|anitya\.distro\.add)).)*$',
                ],
            ),
        ),
        # A second bot for that commops crew that watches for the term "commops"
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='commopswatch-s',
            {% else %}
            nickname='commopswatch',
            {% endif %}
            channel='fedora-commops',
            filters=dict(
                topic=[
                    '(planet|fedora_elections|meetbot\.meeting\.item\.help|meetbot\.meeting\.complete|fedocal\.meeting\.new|fedocal\.meeting\.update|fedocal\.meeting\.delete|fedocal\.calendar|fas\.group\.member\.sponsor|pagure\.project\.new|askbot\.post\.flag_offensive|anitya\.distro\.add)',
                ],
                body=['^((?!commops).)*$'],
            ),
        ),

        # For that python3 porting fad.  AMAZING!
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fedmsg-python-s',
            {% else %}
            nickname='fedmsg-python',
            {% endif %}
            channel='fedora-python',
            filters=dict(
                topic=[
                    '^((?!(github)).)*$',
                ],
                body=[
                    '^((?!(portingdb)).)*$',
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
            nickname='fm-stg-ask',
            {% else %}
            nickname='fm-ask',
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
            nickname='fm-stg-releng',
            {% else %}
            nickname='fm-releng',
            {% endif %}
            channel='fedora-releng',
            filters=dict(
                topic=[
                    '^((?!(bodhi.mashtask.complete|pungi.compose.status.change|pkgdb\.package\.update\.status|compose.branched.complete|compose.branched.start|compose.rawhide.complete|compose.rawhide.start|bodhi.updates.|trac.git.receive)).)*$',
                ],
                body=[
                    "^((?!(u'success': False|u'status': u'DOOMED'|u'status': u'Retired'|u'prev_status': u'Retired'|compose|bodhi\.updates\.|\/srv\/git\/releng)).)*$",
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
            nickname='fm-stg-pfi',
            {% else %}
            nickname='fm-pfi',
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
            nickname='fm-stg-latam',
            {% else %}
            nickname='fm-latam',
            {% endif %}
            channel='#fedora-latam',
            # If the word fedora-latam appears in any message, forward it.
            filters=dict(
                body=['^((?!fedora-latam).)*$'],
            ),
        ),

        # And for #fedora-g11n
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-g11n',
            {% else %}
            nickname='fm-g11n',
            {% endif %}
            channel='#fedora-g11n',
            # If the word i18n/g11n appears in any of below topic message, forward it.
            filters=dict(
                topic=[
                    '^((?!(trac|pagure|planet|mailman|meetbot\.meeting\.complete)).)*$',
                ],
                body=['^((?!(i18n|g11n)).)*$'],
            ),
        ),

        # And #ipsilon
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-ipsilon',
            {% else %}
            nickname='fm-ipsilon',
            {% endif %}
            channel='#ipsilon',
            # If the word ipsilon appears in any message, forward it.
            filters=dict(
                topic=[
                    '^((?!(trac|pagure)).)*$',
                ],
                body=['^((?!ipsilon).)*$'],
            ),
        ),


        # Hook up the design-team with badges messages
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-design',
            {% else %}
            nickname='fm-design',
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
            nickname='fm-stg-docs',
            {% else %}
            nickname='fm-docs',
            {% endif %}
            channel='#fedora-docs',
            filters=dict(
                body=['^((?!\/srv\/git\/docs).)*$'],
            ),
        ),

        # And #fedora-websites
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-web',
            {% else %}
            nickname='fm-web',
            {% endif %}
            channel='#fedora-websites',
            # If the word fedora-websites appears in any message, forward it.
            filters=dict(
                topic=[
                    '^((?!(pagure)).)*$',
                ],
                body=['^((?!fedora-websites).)*$'],
            ),
        ),

        # And #fedora-mktg
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-mktg',
            {% else %}
            nickname='fm-mktg',
            {% endif %}
            channel='#fedora-mktg',
            # If the word fedora-mktg appears in any pagure message, forward it.
            filters=dict(
                topic=[
                    '^((?!(pagure)).)*$',
                ],
                body=['^((?!fedora-mktg).)*$'],
            ),
        ),

        # And #fedora-modularity
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-mod',
            {% else %}
            nickname='fm-mod',
            {% endif %}
            channel='#fedora-modularity',
            # If the word modularity appears in any message, forward it.
            filters=dict(
                topic=[
                    # Ignore some of the ansible and copr spamminess
                    'org.fedoraproject.*.copr.*',
                    'org.fedoraproject.*.ansible.*',
                ],
                body=['^((?!(modularity|Modularity)).)*$'],
            ),
        ),

        # And #fedora-diversity
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-diversity',
            {% else %}
            nickname='fm-diversity',
            {% endif %}
            channel='#fedora-diversity',
            # If the word diversity appears in any message, forward it.
            filters=dict(
                body=['^((?!(diversity|Diversity)).)*$'],
            ),
        ),

        # And #fedora-magazine
        dict(
            network='chat.freenode.net',
            port=6667,
            make_pretty=True,
            make_terse=True,

            {% if env == 'staging' %}
            nickname='fm-stg-magazine',
            {% else %}
            nickname='fm-magazine',
            {% endif %}
            channel='#fedora-magazine',
            # If the word modularity appears in any message, forward it.
            filters=dict(
                body=['^((?!(magazine|Magazine)).)*$'],
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
