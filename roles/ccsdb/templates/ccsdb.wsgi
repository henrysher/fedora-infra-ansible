import os
os.environ['CCSDB_CONFIG'] = '/etc/ccsdb/ccsdb.cfg'

from ccsdb.app import _app as application
