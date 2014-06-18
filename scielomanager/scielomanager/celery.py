# -*- coding: utf-8 -*-
from __future__ import absolute_import

import os

from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'scielomanager.settings')

app = Celery('scielomanager', broker='django://')

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Schedule:
# http://celery.readthedocs.org/en/latest/userguide/periodic-tasks.html#crontab-schedules
from celery.schedules import crontab
CELERYBEAT_SCHEDULE = {
    'checkin-expire-daily': {
        'task': 'articletrack.tasks.process_expirable_checkins',
        'schedule': crontab(minute=0, hour=0),
        'args': ()
    },
}
app.conf.update(
    CELERYBEAT_SCHEDULE=CELERYBEAT_SCHEDULE,
)

if __name__ == '__main__':
    app.start()
