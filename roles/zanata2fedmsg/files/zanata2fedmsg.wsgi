import sys
sys.stdout = sys.stderr

import os
os.environ['PYTHON_EGG_CACHE'] = '/var/www/.python-eggs'

from zanata2fedmsg import app as application
