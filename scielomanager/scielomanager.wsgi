import os, sys

for pwd in ['..', '.']:
    here = os.path.join(os.path.abspath(os.path.dirname(__file__)), pwd)
    if here not in sys.path:
        sys.path.insert(0, here)

os.environ['DJANGO_SETTINGS_MODULE'] = 'scielomanager.settings'
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()