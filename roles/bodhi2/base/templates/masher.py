{% if env == 'staging' %}
suffix = 'stg.phx2.fedoraproject.org'
{% else %}
suffix = 'phx2.fedoraproject.org'
{% endif %}

config = dict(
    masher=True,
    masher_topic='bodhi.masher.start',
    releng_fedmsg_certname='shell-bodhi-backend01.%s' % suffix,
)
