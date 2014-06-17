# coding: utf-8
"""
This module is used by the test runner.
"""
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

execfile(os.path.join(PROJECT_PATH, 'settings.py'))


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '',
    }
}

INSTALLED_APPS += (
    'api',
)

ALLOWED_HOSTS = ['*']
API_BALAIO_DEFAULT_TIMEOUT = 0  # in seconds

JOURNAL_COVER_MAX_SIZE = 30 * 1024
JOURNAL_LOGO_MAX_SIZE = 13 * 1024

#Use this command to start a little SMTP server
#python -m smtpd -n -c DebuggingServer localhost:1025

EMAIL_HOST = 'localhost'
EMAIL_USE_TLS = False
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
