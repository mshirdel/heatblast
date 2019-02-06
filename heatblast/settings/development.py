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
