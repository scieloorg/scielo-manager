# -*- encoding: utf-8 -*-
# Django settings for scielomanager project.
import os

from django.contrib.messages import constants as messages

DEBUG = False

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

MONGO_URI = r'mongodb://localhost:27017/journalmanager'

DOCUMENTATION_BASE_URL = r'http://docs.scielo.org/projects/scielo-manager/en/latest/'
GRAVATAR_BASE_URL = 'https://secure.gravatar.com'

# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

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
MEDIA_ROOT  = os.path.join(PROJECT_PATH, 'static/media/')
#STATIC_ROOT = os.path.join(PROJECT_PATH, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
MEDIA_URL  = '/static/media/'

# Webassets
ASSETS_ROOT = os.path.join(PROJECT_PATH, 'static/')
ASSETS_URL = '/static/'
ASSETS_DEBUG = False

#Third-party URLS
DOCUMENTATION_BASE_URL = r'http://docs.scielo.org/projects/scielo-manager/en/latest'

AVAILABLE_IN_TEMPLATES = {
    'docs_url': DOCUMENTATION_BASE_URL,
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
    'django.middleware.gzip.GZipMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'scielomanager.utils.middlewares.threadlocal.ThreadLocalMiddleware',
    'scielomanager.maintenancewindow.middleware.MaintenanceMiddleware',
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
    'export',
    'accounts',
    'maintenancewindow',
    'south',
    'scielo_extensions',
    'widget_tweaks',
    'tastypie',
    'django_assets',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.csrf',
    'django.core.context_processors.media',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
    'journalmanager.context_processors.dynamic_template_inheritance',
    'journalmanager.context_processors.access_to_settings',
    'journalmanager.context_processors.show_user_collections',
    'journalmanager.context_processors.add_default_collection',
    'journalmanager.context_processors.show_system_notes',
    'journalmanager.context_processors.show_system_notes_blocking_users',
    'journalmanager.context_processors.on_maintenance',
    'scielo_extensions.context_processors.from_settings',
)

# Messages framework
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'
MESSAGE_TAGS = {
    messages.INFO: 'alert-heading',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-error',
}

FIXTURE_DIRS = (os.path.join(PROJECT_PATH, 'fixtures'),)

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

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = ('journalmanager.backends.ModelBackend',)

MANAGED_LANGUAGES_CHOICES = (
    (u'en', u'English'),
    (u'es', u'Español'),
    (u'pt-BR', u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:]

PAGINATION__ITEMS_PER_PAGE = 20

SECTION_CODE_TOTAL_RANDOM_CHARS = 4

CACHE_PREFIX = 'scielomanager:'

#One day (seconds)
CACHE_COUNT_TIMEOUT = 84600

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

CACHES = {
    'default': {
        #'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        'LOCATION': '',
    }
}

IMAGE_CONTENT_TYPE = ['image/jpg', 'image/jpeg', 'image/gif', 'image/png']
IMAGE_DIMENSIONS = {
    'height_logo': 100,
    'width_logo': 200,
    'height_cover': 100,
    'width_cover': 150,
}

IMAGE_SIZE = 300 * 1014

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5Mb

BASE_PATH = PROJECT_PATH
TEST_DISCOVERY_ROOT = BASE_PATH
TEST_RUNNER = 'utils.runner.DiscoveryRunner'

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

# Always minify the HTML when the DEBUG mode is False
HTML_MINIFY = not DEBUG
