import os
# Django settings for push project.

DEBUG = False
DEBUG_PROPAGATE_EXCEPTIONS = True

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

AUTH_USER_MODEL = 'accounts.PushUser'

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = 'staticfiles'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'static'),

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '')

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'push.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'push.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # 3rd Party
    'rest_framework',
    'rest_framework.authtoken',
    'push_notifications',

    # ChatSecure Push
    'accounts',
    'api',
    'tokens',
    'devices',
    'messages.apps.PushMessagesConfig' # To avoid label conflict with 'django.contrib.messages'
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticatedOrReadOnly',),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
    'PAGINATE_BY': 10
}

CHATSECURE_PUSH = {
    # Whether to dispatch push messages on an asynchronous queue (currently Celery)
    'USE_MESSAGE_QUEUE': True,
    # Push Whitelist Tokens older than this expiry time will be deleted
    'DEFAULT_TOKEN_EXPIRY_TIME_S': 60 * 60 * 24 * 60,  # 60 days
    # Address of the 'XMPP Push Service' which adapts XEP-0357 traffic to this app's HTTP API
    # This value is issued to clients who in turn deliver it to their XMPP Server
    'XMPP_PUSH_SERVICE': os.environ.get("XMPP_PUSH_SERVICE", '')
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
        }
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Heroku
# Parse database configuration from $DATABASE_URL
import dj_database_url

DATABASES['default'] = dj_database_url.config()

# The APNS cert should be located at /ProjectRoot/private_keys/apns_cert.pem (../../../private_keys/apns_cert.pem)
APNS_CERTIFICATE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'private_keys/apns_cert.pem')

# For reference, these are APNS Host and Feedback Host addresses
APNS_HOST_DEV = "gateway.sandbox.push.apple.com"
APNS_FEEDBACK_HOST_DEV = "feedback.sandbox.push.apple.com"
APNS_HOST_PROD = "gateway.push.apple.com"
APNS_FEEDBACK_HOST_PROD = "feedback.push.apple.com"

APNS_USE_SANDBOX = os.environ.get("APNS_USE_SANDBOX", 'true').lower()
APNS_USE_SANDBOX = True if APNS_USE_SANDBOX == 'true' else False

PUSH_NOTIFICATIONS_SETTINGS = {
    'APNS_CERTIFICATE' : APNS_CERTIFICATE_PATH,
    'APNS_HOST' : APNS_HOST_DEV if APNS_USE_SANDBOX else APNS_HOST_PROD,
    'APNS_FEEDBACK_HOST' : APNS_FEEDBACK_HOST_DEV if APNS_USE_SANDBOX else APNS_FEEDBACK_HOST_PROD,
    'APNS_ERROR_TIMEOUT': .5,  # Seconds

    'GCM_API_KEY' : os.environ.get('GCM_API_KEY', ''),
}

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Heroku CloudAMQP.
# https://www.cloudamqp.com/docs/celery.html
BROKER_POOL_LIMIT = 1
BROKER_URL = os.environ.get('CLOUDAMQP_URL', '')
BROKER_HEARTBEAT = None  # We're using TCP keep-alive instead
BROKER_CONNECTION_TIMEOUT = 30  # May require a long timeout due to Linux DNS timeouts etc
CELERY_RESULT_BACKEND = None  # AMQP is not recommended as result backend as it creates thousands of queues
CELERY_SEND_EVENTS = False # Will not create celeryev.* queues
CELERY_EVENT_QUEUE_EXPIRES = 60  # Will delete all celeryev. queues without consumers after 1 minute.

# Celery
CELERY_IMPORTS = ('messages.messenger',)

try:
    from push.local_settings import *
except:
    pass
