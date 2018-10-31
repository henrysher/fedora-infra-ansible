SECRET_KEY = '{{ resultsdb_secret_key }}'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{{ resultsdb_db_user }}:{{ resultsdb_db_password }}@{{ resultsdb_db_host }}:{{ resultsdb_db_port }}/{{ resultsdb_db_name }}'
FILE_LOGGING = False
LOGFILE = '/var/log/resultsdb/resultsdb.log'
SYSLOG_LOGGING = False
STREAM_LOGGING = True

MESSAGE_BUS_PUBLISH = False
MESSAGE_BUS_PUBLISH_TASKOTRON = False

MESSAGE_BUS_PLUGIN = 'fedmsg'
MESSAGE_BUS_KWARGS = {'modname': 'resultsdb'}

