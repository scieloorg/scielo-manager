# -*- coding: utf-8 -*-
from __future__ import absolute_import
from scielomanager.celery import app


@app.task(bind=True)
def debug_task(self):
    """
    Dummy task just for test.
    """
    try:
        print('Request user: %s' % self.request.user)
    except AttributeError:
        print('Request has not attribute: user')
    except Exception as e:
        print('Ooops! Exception:', e)
