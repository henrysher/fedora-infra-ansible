# Feel free to `cp settings_local.py.dist settings.local.py`
# and customize your settings, changes here will be populated
# automatically.
#
# This file only contains the minimized settings you should do,
# please look into settings.py to see the whole avaiable settings
# you can do for your PDC instance.
#
# NOTE: For developers or others who want to extend the default
#       settings, please remember to update your settings_local.py
#       when the items you extended got updated in settings.py.

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'pdc.apps.auth.authentication.TokenAuthenticationWithChangeSet',
        'rest_framework.authentication.SessionAuthentication',
    ),

    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    ],

    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

    'DEFAULT_METADATA_CLASS': 'contrib.bulk_operations.metadata.BulkMetadata',

    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
        'pdc.apps.common.renderers.ReadOnlyBrowsableAPIRenderer',
    ),

    'EXCEPTION_HANDLER': 'pdc.apps.common.handlers.exception_handler',

    'DEFAULT_PAGINATION_CLASS': 'pdc.apps.common.pagination.AutoDetectedPageNumberPagination',
}


import os.path

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = False

# NOTE: this is needed when DEGUB is False.
#       https://docs.djangoproject.com/en/1.8/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['{{ hostname }}']

# Database settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ pdc_db_name }}',
        'USER': '{{ pdc_db_user }}',
        'PASSWORD': '{{ pdc_db_pass }}',
        'HOST': '{{ pdc_db_host }}',
        # 'PORT': '',
    }
}

REST_API_URL = 'rest_api/'
REST_API_VERSION = 'v1'

BROWSABLE_DOCUMENT_MACROS = {
    # need to be rewrite with the real host name when deploy.
    'HOST_NAME': 'http://{{ hostname }}:80',
    # make consistent with rest api root.
    'API_PATH': '%s%s' % (REST_API_URL, REST_API_VERSION),
}

def get_setting(setting):
    import pdc.settings
    return getattr(pdc.settings, setting)

# ======== Email configuration =========
# Email addresses who would like to receive email
ADMINS = (
    ('PDC Admins', 'rbean@redhat.com'),
    ('PDC Admins', 'pingou@fedoraproject.org'),
)
MANAGERS = ADMINS

# Email SMTP HOST configuration
EMAIL_HOST = 'localhost'
# Email sender's address
SERVER_EMAIL = 'nobody@fedoraproject.org'
EMAIL_SUBJECT_PREFIX = '[PDC]'

# un-comment below 4 lines if enable email notification as meet any error
#get_setting('LOGGING').get('loggers').update({'pdc.apps.common.handlers': {
#    'handlers': ['mail_admins'],
#    'level': 'ERROR',
#}})

