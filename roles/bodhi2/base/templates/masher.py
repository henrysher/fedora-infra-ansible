{% if env == 'staging' %}
suffix = 'stg.phx2.fedoraproject.org'
{% else %}
suffix = 'phx2.fedoraproject.org'
{% endif %}

config = dict(
    # Note, the masher runs on bodhi-backend01, while other consumers will run
    # on bodhi-backend02.
    masher={{bodhi_masher_enabled}},
    masher_topic='bodhi.masher.start',
    releng_fedmsg_certname='shell-bodhi-backend01.%s' % suffix,
)
