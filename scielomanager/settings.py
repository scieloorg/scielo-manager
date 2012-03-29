# -*- encoding: utf-8 -*-
# Django settings for scielomanager project.
import os

from django.contrib.messages import constants as messages

DEBUG = True
TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.dirname(__file__))
SITE_ROOT = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    ('Admin SciELO', 'dev@scielo.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'journalmanager',         # Or path to database file if using sqlite3.
        'USER': 'postgres',               # Not used with sqlite3.
        'PASSWORD': '',                   # Not used with sqlite3.
        'HOST': '',                       # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                       # Set to empty string for default. Not used with sqlite3.
    }
}

DOCUMENTATION_BASE_URL = r'http://docs.scielo.org/projects/scielo-manager/en/latest/'

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Sao_Paulo'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
#MEDIA_ROOT  = os.path.join(PROJECT_PATH, 'static/media/')
#STATIC_ROOT = os.path.join(PROJECT_PATH, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
MEDIA_URL  = '/static/media/'

#Third-party URLS
DOCUMENTATION_BASE_URL = r'http://docs.scielo.org/projects/scielo-manager/en/latest/'

AVAILABLE_IN_TEMPLATES = {
    'docs_url': DOCUMENTATION_BASE_URL,
    'jquery_url': r'https://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js',
    'jquery_ui_url': r'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.16/jquery-ui.min.js',
    'jquery_ui_css_url': r'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.17/themes/base/jquery-ui.css',
}

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')gowbe964a_$7&gj5mt%fz5asd&9!8d^_-+2wjacn4sm6e$!cw'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'scielomanager.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(PROJECT_PATH, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    #'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'journalmanager',
    'south',
    'scielo_extensions',
)

TEMPLATE_CONTEXT_PROCESSORS =(
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'scielo_extensions.context_processors.from_settings',
)

# Messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.INFO: 'alert-heading',
    messages.SUCCESS: 'alert-heading',
    messages.WARNING: 'alert-error',
    messages.ERROR: 'alert-error',
}

FIXTURE_DIRS = ('fixtures',)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

AUTH_PROFILE_MODULE = 'journalmanager.UserProfile'

AUTHENTICATION_BACKENDS = ('journalmanager.backends.ModelBackend',)

MANAGED_LANGUAGES_CHOICES = (
    (u'en',u'English'),
    (u'es',u'Español'),
    (u'pt-BR',u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:] # exlude source language

PAGINATION__ITEMS_PER_PAGE = 20

### END App customization settings
#################################################################

# Local deployment settings: there *must* be an unversioned
# 'settings_local.include' file in the current directory.
# See sample file at settings_local-SAMPLE.include.
# NOTE: in the next line we do not use a simple...
# try: from settings_local import * except ImportError: pass
# ...because (1) we want to be able to add to settings in this file, and
# not only overwrite them, and (2) we do not want the app to launch if the
# 'settings_local.include' file is not provided
execfile(os.path.join(PROJECT_PATH,'settings_local.include'))
