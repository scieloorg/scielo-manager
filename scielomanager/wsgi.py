"""
WSGI config for scielomanager project.

This module contains the WSGI application used by Django's development server
and any production WSGI deployments. It should expose a module-level variable
named ``application``. Django's ``runserver`` and ``runfcgi`` commands discover
this application via the ``WSGI_APPLICATION`` setting.

Usually you will have the standard Django WSGI application here, but it also
might make sense to replace the whole Django WSGI application with a custom one
that later delegates to the Django one. For example, you could introduce WSGI
middleware here, or combine a Django application with an application of another
framework.

"""
import os
import sys

# Adding scielomanager package to the python path.
here = os.path.abspath(os.path.dirname(__file__))
if here not in sys.path:
    sys.path.insert(0, here)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scielomanager.settings")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)

try:
    import newrelic.agent
    newrelic.agent.initialize(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'newrelic.ini'), 'production')
except (IOError, ImportError):
    pass
else:
    application = newrelic.agent.wsgi_application()(application)
