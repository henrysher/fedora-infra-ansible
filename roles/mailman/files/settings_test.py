#-*- coding: utf-8 -*-

"""
Copy of the Django settings file, but with databases set for unit tests.
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
KITTYSTORE_URL = 'sqlite:'
