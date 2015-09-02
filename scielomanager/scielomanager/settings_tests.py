# coding: utf-8
"""
This module is used by the test runner.
"""
import os

PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))

execfile(os.path.join(PROJECT_PATH, 'settings.py'))


INSTALLED_APPS += (
    'api',
)

ALLOWED_HOSTS = ['*']
API_BALAIO_DEFAULT_TIMEOUT = 0  # in seconds

JOURNAL_COVER_MAX_SIZE = 30 * 1024
JOURNAL_LOGO_MAX_SIZE = 13 * 1024

# Use this command to start a little SMTP server
# python -m smtpd -n -c DebuggingServer localhost:1025

EMAIL_HOST = 'localhost'
EMAIL_USE_TLS = False
EMAIL_PORT = 1025
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

# Desabilitar logging na execução dos test para um determinado nível.
# Issue relacionado: https://github.com/scieloorg/scielo-manager/issues/1188
# Valores aceitaveis:
# - False: não desabilita o logging.
# - 'CRITICAL' ou 'DEBUG' ou 'ERROR', etc. : desabilita loggings abaixo do nivel especificado.

DISABLE_LOGGING_BELOW_LEVEL = 'CRITICAL'  # set to False to enable loggings
