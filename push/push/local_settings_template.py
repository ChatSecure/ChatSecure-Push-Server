# Local settings go here!

DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '',                      # Or path to database file if using sqlite3.
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = ''

BROKER_URL = 'amqp://guest:guest@localhost:5672/'

CHATSECURE_PUSH = {
    # Set this to false when debugging to not use Celery
    'USE_MESSAGE_QUEUE': False,
    'DEFAULT_TOKEN_EXPIRY_TIME_S': 60 * 60 * 24 * 60  # 60 days
}

PUSH_NOTIFICATIONS_SETTINGS = {
    # See README.md for instructions for obtaining the APNS Certificate, and GCM API Key

    # Note the value of APNS_CERTIFICATE should depend on DEBUG
    #'APNS_CERTIFICATE' : '/Path/To/Certificate.pem'

    #'GCM_API_KEY' : 'Your API Key'
}
