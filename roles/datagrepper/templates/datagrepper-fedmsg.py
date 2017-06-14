# Configuration for the datagrepper webapp.
config = {
    # We don't actually want to run the datanommer consumer on this machine.
    'datanommer.enabled': False,

    # Note that this is connecting to db02.  That's fine for now, but we want to
    # move the db for datanommer to a whole other db host in the future.  We
    # expect the amount of data it generates to grow pretty steadily over time
    # and we don't want *read* operations on that database to slow down all our
    # other apps.
    {% if env == "staging" %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer.stg.phx2.fedoraproject.org/datanommer',
    'fedmenu_url': 'https://apps.stg.fedoraproject.org/fedmenu',
    'fedmenu_data_url': 'https://apps.stg.fedoraproject.org/js/data.js',
    {% else %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer02.phx2.fedoraproject.org/datanommer',
    'fedmenu_url': 'https://apps.fedoraproject.org/fedmenu',
    'fedmenu_data_url': 'https://apps.fedoraproject.org/js/data.js',
    {% endif %}

    # Only allow ajax/websockets connections back to our domains.
    # https://github.com/fedora-infra/datagrepper/pull/192
    'content_security_policy': 'connect-src https://*.fedoraproject.org wss://*.fedoraproject.org'
}
