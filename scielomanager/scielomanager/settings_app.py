# coding: utf-8
"""
This file contains permanent settings, specific to the
scielomanager project.
"""
import os

from django.contrib.messages import constants as messages


# Absolute path to this module (not used by django itself)
HERE_ABSPATH = os.path.abspath(os.path.dirname(__file__))

# URLs referenced somewhere in the project
DOCUMENTATION_BASE_URL = r'http://docs.scielo.org/projects/scielo-manager/en/latest/'
GRAVATAR_BASE_URL = 'https://secure.gravatar.com'

# Settings that are meant to be visible in templates
AVAILABLE_IN_TEMPLATES = {
    'docs_url': DOCUMENTATION_BASE_URL,
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ['*']

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(HERE_ABSPATH, 'static/media/')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = '/static/media/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE_ABSPATH, 'static/'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
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

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(HERE_ABSPATH, 'templates'),
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

# Put strings here, targeting the directory that hosts fixture files.
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
FIXTURE_DIRS = (os.path.join(HERE_ABSPATH, 'fixtures'),)

# Authentication and authorization
AUTH_PROFILE_MODULE = 'journalmanager.UserProfile'
AUTHENTICATION_BACKENDS = ('journalmanager.backends.ModelBackend',)
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/'

# App supported languages
MANAGED_LANGUAGES_CHOICES = (
    (u'en', u'English'),
    (u'es', u'Español'),
    (u'pt-BR', u'Português'),
)
TARGET_LANGUAGES = MANAGED_LANGUAGES_CHOICES[1:]

# The total items per page on paginated objects
PAGINATION__ITEMS_PER_PAGE = 20

# The total number of characters used to form the section code.
# Section codes are formed by <Journal.acronym>-<base28_chars>
SECTION_CODE_TOTAL_RANDOM_CHARS = 4

# Session
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Image files constraints
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

# Custom test runner
BASE_PATH = HERE_ABSPATH
TEST_DISCOVERY_ROOT = BASE_PATH
TEST_RUNNER = 'utils.runner.DiscoveryRunner'

# Class responsible for retrieving the current user's context,
# according to the application rules. This class is used by
# , for example, the ``userobjects`` managers.
USERREQUESTCONTEXT_FINDER = 'utils.middlewares.threadlocal.UserRequestContextFinder'


####################################################
# This must be the last piece of code of this module
####################################################
try:
    execfile(os.path.join(HERE_ABSPATH, 'settings_local.include'))
except IOError:
    exit('Missing configuration file: "settings_local.include"')
