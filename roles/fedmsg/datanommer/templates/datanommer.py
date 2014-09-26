# Configuration for the datanommer consumer.  A plugin for the fedmsg-hub process.
config = {
    'datanommer.enabled': True,
    'datanommer.sqlalchemy.url': 'postgresql://{{ datanommerDBUser }}:{{ datanommerDBPassword }}@db-datanommer02/datanommer',
}
