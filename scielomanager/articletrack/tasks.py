# coding: utf-8
import datetime
import logging

from .balaio import BalaioRPC
from .models import Checkin
from scielomanager.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def do_expires_checkin(self, checkin):
    """
    For this checkin:
    - call BalaioRPC.expire_attempt API method to trigger action on Balaio's side.
    - call do_expires() that change status and create workflow logs.
    if API is down or RPC call raise exception -> task will be retried
    """
    rpc_client = BalaioRPC()
    logger.debug('[do_expires_checkin] START process to expire checkin (pk=%s) at %s' % (checkin.pk, datetime.datetime.now()))

    try:
        rpc_client.call('expire_attempt', [checkin.attempt_ref, ])
    except Exception as e:
        logger.debug('[do_expires_checkin] FAIL, retrying exception: %s' % e)
        raise self.retry(exc=e)
    else:
        checkin.do_expires()
        logger.info('[do_expires_checkin] EXPIRED checkin pk: %s' % checkin.pk)

    logger.debug('[do_expires_checkin] FINISH process at %s' % datetime.datetime.now())


@app.task(bind=True)
def process_expirable_checkins(self):
    """
    RUN: daily!
    For each checkin that is "expirable":
        call the task: do_expires_checkin to change the checkins as expired
    """
    logger.debug('[process_expirable_checkins] START process at %s' % datetime.datetime.now())
    checkins = Checkin.objects.filter(status='pending', expiration_at__isnull=False)
    logger.info('[process_expirable_checkins] Found %s checkins matching conditions' % checkins.count())
    for checkin in checkins:
        logger.info('[process_expirable_checkins] Processing checkin (pk=%s)' % checkin.pk)
        if checkin.is_expirable:
            do_expires_checkin.apply_async(args=[checkin, ])

    logger.debug('[process_expirable_checkins] FINISH process at %s' % datetime.datetime.now())
