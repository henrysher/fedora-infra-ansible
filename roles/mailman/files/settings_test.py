#-*- coding: utf-8 -*-

"""
Copy of the Django settings file, but with the database set for unit tests.
"""

from settings import *
try:
    from settings_local import *
except ImportError:
    pass

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Mailman API credentials for testing Postorius
MAILMAN_API_URL = 'http://localhost:9001'
MAILMAN_USER = 'restadmin'
MAILMAN_PASS = 'restpass'

VCR_RECORD_MODE = 'once'
USE_SSL = False
