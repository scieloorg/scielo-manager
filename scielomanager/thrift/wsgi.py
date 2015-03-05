#coding: utf-8
import os
import sys


# Adding scielomanager package to the python path.
parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if parent not in sys.path:
    sys.path.insert(0, parent)


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scielomanager.settings")


# DJANGO_SETTINGS_MODULE must be set before any project package
# is loaded.
from server import make_wsgi_app
app = make_wsgi_app()

