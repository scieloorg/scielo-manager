# -*- encoding: utf-8 -*-

# Because Django deletes related objects by default,
# deleting the ContentType objects will also remove the
# related django.contrib.auth.models.Permission objects
# (and the many-to-many associations with users and groups).
import subprocess
import sys
import os


# Adding scielomanager package to the python path.
here = os.path.abspath(os.path.dirname(__file__))
if here not in sys.path:
    sys.path.insert(0, here)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "scielomanager.settings")


from django.conf import settings
from django.contrib.contenttypes.models import ContentType


try:
    ContentType.objects.filter(app_label='articletrack').delete()
except Exception as exc:
    sys.exit(exc.message)


with open(os.path.join(here, 'drop_articletrack_tables.sql')) as fhandle:
    returncode = subprocess.call(['psql', settings.DATABASES['default']['NAME'],
         '-U' + settings.DATABASES['default']['USER'],], stdin=fhandle)
    sys.exit(returncode)

