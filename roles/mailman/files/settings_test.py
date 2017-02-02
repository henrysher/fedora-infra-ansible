#-*- coding: utf-8 -*-

"""
Copy of the Django settings file, but with the database set for unit tests.
"""

from settings import *
try:
    from settings_local import *
except ImportError:
    pass

TESTING = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Mailman API credentials for testing Postorius
MAILMAN_REST_API_URL = 'http://localhost:9001'
MAILMAN_REST_API_USER = 'restadmin'
MAILMAN_REST_API_PASS = 'restpass'

VCR_RECORD_MODE = 'once'
USE_SSL = False

COMPRESS_ENABLED = False
# Empty the precompilers mapping for testing: django-compressor will run them
# even if compress_enabled is false, no idea why
COMPRESS_PRECOMPILERS = ()

#
# Full-text search engine
#
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': ':memory:',
        'STORAGE': 'ram',
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

LOGGING = {}

# Disable caching
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
