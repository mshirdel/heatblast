# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

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