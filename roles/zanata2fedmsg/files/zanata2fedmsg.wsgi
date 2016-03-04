import sys
sys.stdout = sys.stderr

import os
os.environ['PYTHON_EGG_CACHE'] = '/var/www/.python-eggs'
os.environ['ZANATA2FEDMSG_CONFIG'] = '/etc/zanata2fedmsg.ini'

import logging
logging.basicConfig(level='INFO')

from zanata2fedmsg import app as application
