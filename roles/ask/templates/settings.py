## Django settings for ASKBOT enabled project.
import os.path
import logging
import sys
import askbot
import site

#this line is added so that we can import pre-packaged askbot dependencies
ASKBOT_ROOT = os.path.abspath(os.path.dirname(askbot.__file__))
site.addsitedir(os.path.join(ASKBOT_ROOT, 'deps'))

DEBUG = False#set to True to enable debugging
TEMPLATE_DEBUG = False#keep false when debugging jinja2 templates
INTERNAL_IPS = ('127.0.0.1',)
ALLOWED_HOSTS = ['*',]#change this for better security on your site

ADMINS = (
    ('AskFedora Sysadmins', 'sysadmin-ask-members@fedoraproject.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'askfedora',
        'USER': 'askfedora',                      # Not used with sqlite3.
        'PASSWORD': '{{ askbotDBPassword }}',                  # Not used with sqlite3.
	'HOST' : 'db-ask',         # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
        'TEST_CHARSET': 'utf8',              # Setting the character set and collation to utf-8
        'TEST_COLLATION': 'utf8_general_ci', # is necessary for MySQL tests to work properly.
    }
}

#outgoing mail server settings
SERVER_EMAIL = 'nobody@fedoraproject.org'
DEFAULT_FROM_EMAIL = 'nobody@fedoraproject.org'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_SUBJECT_PREFIX = ''
EMAIL_HOST='bastion'
EMAIL_PORT='25'
EMAIL_USE_TLS=False
EMAIL_BACKEND = 'post_office.EmailBackend'
FEEDBACK_EMAILS = 'sysadmin-ask-members@fedoraproject.org'

#incoming mail settings
#after filling out these settings - please
#go to the site's live settings and enable the feature
#"Email settings" -> "allow asking by email"
#
#   WARNING: command post_emailed_questions DELETES all
#            emails from the mailbox each time
#            do not use your personal mail box here!!!
#
IMAP_HOST = ''
IMAP_HOST_USER = ''
IMAP_HOST_PASSWORD = ''
IMAP_PORT = ''
IMAP_USE_TLS = False

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'UTC'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True
LANGUAGE_CODE = 'en'

# Absolute path to the directory that holds uploaded media
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = '/srv/askbot-uploaded'
MEDIA_URL = '/upfiles/'
STATIC_URL = '/m/'#this must be different from MEDIA_URL

PROJECT_ROOT = os.path.dirname(__file__)
#STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_ROOT = '/var/www/html/askbot/static'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

# Make up some unique string, and don't share it with anybody.
SECRET_KEY = '{{ askbotSecretKeyPassword }}'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'askbot.skins.loaders.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.filesystem.Loader',
    #'django.template.loaders.eggs.load_template_source',
)


MIDDLEWARE_CLASSES = (
    #'django.middleware.gzip.GZipMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    ## Enable the following middleware if you want to enable
    ## language selection in the site settings.
    #'askbot.middleware.locale.LocaleMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    #'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.common.CommonMiddleware',
    #'django.middleware.cache.FetchFromCacheMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.middleware.sqlprint.SqlPrintingMiddleware',

    # Enable outgoing fedmsg messages
    'askbot_fedmsg.NOOPMiddleware',

    #below is askbot stuff for this tuple
    'askbot.middleware.anon_user.ConnectToSessionMessagesMiddleware',
    'askbot.middleware.forum_mode.ForumModeMiddleware',
    'askbot.middleware.cancel.CancelActionMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
    'askbot.middleware.view_log.ViewLogMiddleware',
    'askbot.middleware.spaceless.SpacelessMiddleware',
{% if env == "staging" %}
#    'stopforumspam.middleware.StopForumSpamMiddleware',
{% endif %}
)


ROOT_URLCONF = os.path.basename(os.path.dirname(__file__)) + '.urls'


#UPLOAD SETTINGS
FILE_UPLOAD_TEMP_DIR = os.path.join(
                                os.path.dirname(__file__),
                                'tmp'
                            ).replace('\\','/')

FILE_UPLOAD_HANDLERS = (
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
)
ASKBOT_ALLOWED_UPLOAD_FILE_TYPES = ('.jpg', '.jpeg', '.gif', '.bmp', '.png', '.tiff')
ASKBOT_MAX_UPLOAD_FILE_SIZE = 1024 * 1024 #result in bytes
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'


#TEMPLATE_DIRS = (,) #template have no effect in askbot, use the variable below
{% if env == "staging" %}
ASKBOT_EXTRA_SKINS_DIR = '/usr/share/askbot/skins'
{% endif %}
#ASKBOT_EXTRA_SKINS_DIR = #path to your private skin collection
#take a look here http://askbot.org/en/question/207/

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.request',
    'askbot.context.application_settings',
    #'django.core.context_processors.i18n',
    'askbot.user_messages.context_processors.user_messages',#must be before auth
    'django.contrib.auth.context_processors.auth', #this is required for the admin app
    'django.core.context_processors.csrf', #necessary for csrf protection
)


INSTALLED_APPS = (
    'longerusername',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',

    #all of these are needed for the askbot
    'django.contrib.admin',
    'django.contrib.humanize',
    'django.contrib.sitemaps',
    'django.contrib.messages',
    #'debug_toolbar',
    #Optional, to enable haystack search
    #'haystack',
    'compressor',
    'askbot',
    'askbot.deps.django_authopenid',
    #'askbot.importers.stackexchange', #se loader
    'south',
    'askbot.deps.livesettings',
    'keyedcache',
    'robots',
    'django_countries',
    'djcelery',
    'djkombu',
    'followit',
    'tinymce',
    'group_messaging',
    #'avatar',#experimental use git clone git://github.com/ericflo/django-avatar.git$
    'post_office',
{% if env == "staging" %}
#    'stopforumspam',
{% endif %}
)

{% if env == "staging" %}
SFS_ALL_POST_REQUESTS = True
SFS_FORCE_ALL_REQUESTS = True
SFS_CACHE_EXPIRE = 1
SFS_LOG_EXPIRE = 7
SFS_HTTP_HEADER = "X-Forwarded-For"
SFS_SOURCE_ZIP = "file:///var/cache/askbot/listed_ip_7.zip"
{% endif %}

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_TIMEOUT = 600

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'askbot.deps.django_authopenid.backends.AuthBackend',
)

#logging settings
LOG_FILENAME = 'askfedora.log'
logging.basicConfig(
    filename=os.path.join('/var', 'log', 'askbot', LOG_FILENAME),
    level=logging.CRITICAL,
    format='%(pathname)s TIME: %(asctime)s MSG: %(filename)s:%(funcName)s:%(lineno)d %(message)s',
)

###########################
#
#   this will allow running your forum with url like http://site.com/forum
#
#   ASKBOT_URL = 'forum/'
#
ASKBOT_URL = '' #no leading slash, default = '' empty string
ASKBOT_TRANSLATE_URL = False #translate specific URLs
_ = lambda v:v #fake translation function for the login url
LOGIN_URL = '/%s%s%s' % (ASKBOT_URL,_('account/'),_('signin/'))
LOGIN_REDIRECT_URL = ASKBOT_URL #adjust, if needed
#note - it is important that upload dir url is NOT translated!!!
#also, this url must not have the leading slash
ALLOW_UNICODE_SLUGS = False
ASKBOT_USE_STACKEXCHANGE_URLS = False #mimic url scheme of stackexchange

#Celery Settings
BROKER_TRANSPORT = "djkombu.transport.DatabaseTransport"
CELERY_ALWAYS_EAGER = True

#
# Only enable languages where we have active moderators
# In staging we have a few more for communities to test with before commiting. 
# 
# locmem cache in staging and use memcached04 in production. 
#

{% if env == "staging" %}
DOMAIN_NAME = 'ask.stg.fedoraproject.org'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'ask-staging'
    }
}
gettext = lambda s: s
LANGUAGES = (
    ('pt-br', gettext('Brazilian Portuguese')),
    ('ca', gettext('Catalan')),
    ('es', gettext('Spanish')),
    ('en', gettext('English')),
    ('ru', gettext('Russian')),
    ('zh-cn', gettext('Simplified Chinese')),
    ('zh-tw', gettext('Traditional Chinese')),
    ('fr', gettext('French')),
    ('el', gettext('Greek')),
    ('id', gettext('Indonesian')),
    ('hu', gettext('Hungarian')),
)
{% else %}
DOMAIN_NAME = 'ask.fedoraproject.org'
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'KEY_PREFIX': 'askfedora',
        'LOCATION': [
            'memcached02:11211',
        ]
    }
}
gettext = lambda s: s
LANGUAGES = (
    ('ca', gettext('Catalan')),
    ('el', gettext('Greek')),
    ('es', gettext('Spanish')),
    ('en', gettext('English')),
    ('pt-br', gettext('Brazilian Portuguese')),
    ('ru', gettext('Russian')),
    ('id', gettext('Indonesian')),
    ('zh-cn', gettext('Simplified Chinese')),
)
{% endif %}

#https://docs.djangoproject.com/en/1.3/ref/contrib/csrf/
CSRF_COOKIE_DOMAIN = DOMAIN_NAME

#STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATICFILES_DIRS = (
    ('default/media', os.path.join(ASKBOT_ROOT, 'media')),
{% if env == "staging" %}
    ASKBOT_EXTRA_SKINS_DIR,
{% endif %}
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Since Django 1.2.7 we need to add this or it will not forward openid requests correctly.
USE_X_FORWARDED_HOST = True

# Since askbot 0.7.32 we need to have a redirect url after login 
LOGIN_REDIRECT_URL = ASKBOT_URL

RECAPTCHA_USE_SSL = True

#HAYSTACK_SETTINGS
ENABLE_HAYSTACK_SEARCH = False
HAYSTACK_SITECONF = "askbot.search.haystack"
#Uncomment for multilingual setup:
#HAYSTACK_ROUTERS = ['askbot.search.haystack.routers.LanguageRouter',]

#Uncomment if you use haystack
#More info in http://django-haystack.readthedocs.org/en/latest/settings.html
#HAYSTACK_CONNECTIONS = {
#            'default': {
#                        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
#            }
#}


TINYMCE_COMPRESSOR = True
TINYMCE_SPELLCHECKER = False
TINYMCE_JS_ROOT = os.path.join(STATIC_ROOT, 'default/media/js/tinymce/')
#TINYMCE_JS_URL = STATIC_URL + 'default/media/js/tinymce/tiny_mce.js'
TINYMCE_URL = STATIC_URL + 'default/media/js/tinymce/'
TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'convert_urls': False,
    'theme': 'advanced',
    'content_css': STATIC_URL + 'default/media/style/tinymce/content.css',
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'mode' : 'textareas',
    'oninit': "TinyMCE.onInitHook",
    'plugins': 'askbot_imageuploader,askbot_attachment',
    'theme_advanced_toolbar_location' : 'top',
    'theme_advanced_toolbar_align': 'left',
    'theme_advanced_buttons1': 'bold,italic,underline,|,bullist,numlist,|,undo,redo,|,link,unlink,askbot_imageuploader,askbot_attachment',
    'theme_advanced_buttons2': '',
    'theme_advanced_buttons3' : '',
    'theme_advanced_path': False,
    'theme_advanced_resizing': True,
    'theme_advanced_resize_horizontal': False,
    'theme_advanced_statusbar_location': 'bottom',
    'width': '730',
    'height': '250'
}

#delayed notifications, time in seconds, 15 mins by default
NOTIFICATION_DELAY_TIME = 60 * 15

GROUP_MESSAGING = {
    'BASE_URL_GETTER_FUNCTION': 'askbot.models.user_get_profile_url',
    'BASE_URL_PARAMS': {'section': 'messages', 'sort': 'inbox'}
}

ASKBOT_MULTILINGUAL = True

ASKBOT_CSS_DEVEL = False
if 'ASKBOT_CSS_DEVEL' in locals() and ASKBOT_CSS_DEVEL == True:
    COMPRESS_PRECOMPILERS = (
        ('text/less', 'lessc {infile} {outfile}'),
    )

COMPRESS_JS_FILTERS = []
COMPRESS_PARSER = 'compressor.parser.HtmlParser'
JINJA2_EXTENSIONS = ('compressor.contrib.jinja2ext.CompressorExtension',)

# Use syncdb for tests instead of South migrations. Without this, some tests
# fail spuriously in MySQL.
SOUTH_TESTS_MIGRATE = False

VERIFIER_EXPIRE_DAYS = 3
