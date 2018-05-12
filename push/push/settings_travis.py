# Local settings go here!

DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'travisci',
        'USER':     'postgres',
        'PASSWORD': '',
        'HOST':     'localhost',
        'PORT':     '',
    }
}


# Make this unique, and don't share it with anybody.
SECRET_KEY = 'travisci'

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
    'APNS_TOPIC': 'your.bundle.Identifier'
}
