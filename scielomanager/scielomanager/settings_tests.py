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
