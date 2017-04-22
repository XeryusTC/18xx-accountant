# -*- coding: utf-8 -*-
from django.core.exceptions import ImproperlyConfigured
import os
from .base import *

def get_env_setting(setting):
    try:
        return os.environ[setting]
    except KeyError:
        raise ImproperlyConfigured(
            "Could not find setting '{}' in the environment".format(setting))

DEBUG = False
DOMAIN = get_env_setting('ACCOUNTANT_DOMAIN')
ALLOWED_HOSTS = [
    DOMAIN,
    'www.' + DOMAIN,
]

SECRET_KEY = get_env_setting('ACCOUNTANT_SECRET_KEY')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': get_env_setting('ACCOUNTANT_DB_NAME'),
        'USER': get_env_setting('ACCOUNTANT_DB_USER'),
        'PASSWORD': get_env_setting('ACCOUNTANT_DB_PASSWORD'),
        'HOST': 'localhost',
        'port': '',
    },
}

INSTALLED_APPS += ('gunicorn',)

# sECURITY SETTINGS
X_FRAME_OPTIONS = 'DENY'
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
