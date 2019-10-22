from .base import *

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('db_name', 'socialnews'),
        'USER': os.environ.get('db_user', 'postgres'),
        'PASSWORD': os.environ.get('db_pass', 'password'),
        'HOST': os.environ.get('db_host',''),
        'PORT': os.environ.get('db_port', '5432'),
    }
}

PAGE_SIZE = 10

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'helermiles@gmail.com'
try:
    EMAIL_HOST_PASSWORD = os.environ.get['HEATBLAST_EMAIL_PASSWORD']
except KeyError:
    EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587
EMAIL_USE_TLS = True
