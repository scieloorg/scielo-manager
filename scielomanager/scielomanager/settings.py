# -*- encoding: utf-8 -*-
# Django settings for scielomanager project.
import os
from datetime import timedelta
from django.contrib.messages import constants as messages

# XML Catalog env-var is required for sps-stylechecking
from packtools.catalogs import XML_CATALOG
os.environ['XML_CATALOG_FILES'] = XML_CATALOG

DEBUG = False

TEMPLATE_DEBUG = DEBUG
PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
HERE = os.path.dirname(os.path.abspath(__file__))

ADMINS = (
    ('Admin SciELO', 'dev@scielo.org'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
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
MEDIA_ROOT = os.path.join(HERE, 'static/media/')
# STATIC_ROOT = os.path.join(PROJECT_PATH, 'static/')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'
MEDIA_URL = '/static/media/'

# Webassets
ASSETS_ROOT = os.path.join(HERE, 'static/')
ASSETS_URL = '/static/'
ASSETS_DEBUG = False

# Third-party URLS
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
    os.path.join(HERE, 'static/'),
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
    # 'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'scielomanager.utils.middlewares.threadlocal.ThreadLocalMiddleware',
    'maintenancewindow.middleware.MaintenanceMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'scielomanager.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',

    # Third-party apps
    'django_assets',
    'kombu.transport.django',
    'widget_tweaks',
    'djcelery',
    'tastypie',
    'south',

    # SciELO shared apps
    'scielo_extensions',

    # SciELO Manager apps
    'maintenancewindow',
    'journalmanager',
    'editorialmanager',
    'audit_log',
    'validator',
    'accounts',
    'export',
    'health',
    'thrift',
    'scielomanager',  # apenas para management commands
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
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

FIXTURE_DIRS = (os.path.join(HERE, 'fixtures'),)

# Reconfiguração total do sistema de logs do projeto.
# http://stackoverflow.com/a/22336174
LOGGING_CONFIG = None
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(name)s[%(process)d] [%(levelname)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'NOTSET',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'ERROR',
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'thrift': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'health': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        'packtools': {
            'handlers': ['console', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}
import logging.config
logging.config.dictConfig(LOGGING)


AUTH_PROFILE_MODULE = 'journalmanager.UserProfile'

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'
AUTHZ_REDIRECT_URL = '/accounts/unauthorized/'

AUTHENTICATION_BACKENDS = ('journalmanager.backends.ModelBackend',)

MANAGED_LANGUAGES_CHOICES = (
    (u'en', u'English'),
    (u'es', u'Español'),
    (u'pt-BR', u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:]

PAGINATION__ITEMS_PER_PAGE = 20

SECTION_CODE_TOTAL_RANDOM_CHARS = 4

SESSION_EXPIRE_AT_BROWSER_CLOSE = True


IMAGE_CONTENT_TYPE = ['image/jpg', 'image/jpeg', 'image/gif', 'image/png']
IMAGE_DIMENSIONS = {
    'height_logo': 100,
    'width_logo': 200,
    'height_cover': 100,
    'width_cover': 150,
}

IMAGE_SIZE = 300 * 1024
IMAGE_MAX_UPLOAD_SIZE = 5242880  # must be an integer of bytes allowed, see comment on custom_fields.ContentTypeRestrictedFileField for reference
JOURNAL_COVER_MAX_SIZE = IMAGE_MAX_UPLOAD_SIZE
JOURNAL_LOGO_MAX_SIZE = IMAGE_MAX_UPLOAD_SIZE
VALIDATOR_MAX_UPLOAD_SIZE = 512 * 1024  # max size in byte to upload xml to validator

FILE_UPLOAD_HANDLERS = (
    "django.core.files.uploadhandler.MemoryFileUploadHandler",
    "django.core.files.uploadhandler.TemporaryFileUploadHandler",
)

FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # 2.5Mb

BASE_PATH = PROJECT_PATH
TEST_DISCOVERY_ROOT = BASE_PATH
TEST_RUNNER = 'scielomanager.utils.runner.DiscoveryRunner'

LOCALE_PATHS = (
    os.path.join(HERE, 'locale'),
)

if 'djcelery' in INSTALLED_APPS:
    CELERY_TIMEZONE = TIME_ZONE
    BROKER_URL = 'django://'
    CELERY_ACCEPT_CONTENT = ['pickle', 'json', 'msgpack', 'yaml']
    CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
    CELERY_IMPORTS = ('scielomanager.tasks')
    CELERYD_MAX_TASKS_PER_CHILD = 100
    CELERY_SEND_TASK_ERROR_EMAILS = True

if 'thrift' in INSTALLED_APPS:
    THRIFT_CONFIG = {
        'HOST': '0.0.0.0',
        'PORT': '6000',
    }


# ----------------------------------------------------
# Endereços de enlace para comunicação inter-processos
#
# Todos os endereços de IPC devem ser prefixados com
# `IPC_`, para sinalizar que é um endpoint da aplicação.
# ----------------------------------------------------
IPC_HEALTHD_BIND_ADDR = 'tcp://0.0.0.0:11711'


ELASTICSEARCH_NODES = (
    'localhost:0',
    # 'esa.scielo.org:9200',
    # 'esb.scielo.org:9200',
    # 'esc.scielo.org:9200',
)

ES_ARTICLE_INDEX_NAME = 'icatman'
ES_ARTICLE_DOC_TYPE = 'article'

# URL wayta
WAYTA_URL = "http://wayta.scielo.org"
WAYTA_PATH = "/api/v1/"

# Checkin expiration time span (in days)
CHECKIN_EXPIRATION_TIME_SPAN = 7  # days

# ## END App customization settings
#################################################################

# Local deployment settings: there *must* be an unversioned
# 'scielomanager.conf' file in /etc/scieloapps/.
# See sample file at settings_local-SAMPLE.include.
# NOTE: in the next line we do not use a simple...
# try: from settings_local import * except ImportError: pass
# ...because (1) we want to be able to add to settings in this file, and
# not only overwrite them, and (2) we do not want the app to launch if the
# config file cannot be loaded.
SCIELOMANAGER_SETTINGS_FILE = os.environ.get('SCIELOMANAGER_SETTINGS_FILE')
if SCIELOMANAGER_SETTINGS_FILE:
    execfile(SCIELOMANAGER_SETTINGS_FILE)
else:
    raise RuntimeError('Missing settings file. Make sure SCIELOMANAGER_SETTINGS_FILE is configured.')

# Always minify the HTML when the DEBUG mode is False
HTML_MINIFY = not DEBUG
EXCLUDE_FROM_MINIFYING = ('^admin/', )

# Versão mais antiga suportada do SPS, na qual o usuario do
# StyleChecker deve ser notficado do Deprecation Warning.
# A versão deve respeitar o formato do atributo @specific-use: 'sps-1.1' ou 'sps-1.2'.
PACKTOOLS_DEPRECATION_WARNING_VERSION = 'sps-1.1'
