# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
from .base import *


DEBUG = True
ALLOWED_HOSTS = []

INTERNAL_IPS = ['127.0.0.1']

INSTALLED_APPS += [
    'django_extensions',
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'socialnews',
        'USER': 'postgres',
        'PASSWORD': 'pg123',
        'HOST': '',
        'PORT': '5432',
    }
}

PAGE_SIZE = 10

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'helermiles@gmail.com'
try:
    EMAIL_HOST_PASSWORD = os.environ['HEATBLAST_EMAIL_PASSWORD']
except KeyError:
    EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
