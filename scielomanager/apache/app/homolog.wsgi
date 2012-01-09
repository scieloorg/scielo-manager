import os, sys
sys.path.append('/var/www/jmanager_scielo_org/')
sys.path.append('/var/www/jmanager_scielo_org/scielomanager/')
os.environ['DJANGO_SETTINGS_MODULE'] = 'scielomanager.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
