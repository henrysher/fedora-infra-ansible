# Configuration for the datanommer consumer.  A plugin for the fedmsg-hub process.
config = {
    'datanommer.enabled': True,
{% if 'transitional' in inventory_hostname %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ transitionalDatanommerDBUser }}:{{ transitionalDatanommerDBPassword }}@db-datanommer01/datanommer',
{% elif env == "production" %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer02/datanommer',
{% else %}
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer.stg.phx2.fedoraproject.org/datanommer',
{% endif %}
}
