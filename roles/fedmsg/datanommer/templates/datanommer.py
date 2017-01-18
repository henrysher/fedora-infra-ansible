# Configuration for the datanommer consumer.  A plugin for the fedmsg-hub process.
config = {
    'datanommer.enabled': True,
{% if env == "production" %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer02/datanommer',
{% else %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer.stg/datanommer',
{% endif %}
}
