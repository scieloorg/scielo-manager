# coding: utf-8
import datetime
import logging
# from celery.utils.log import get_task_logger
from .balaio import BalaioRPC
from xmlrpclib import Fault, ProtocolError
from .models import Checkin
from scielomanager.celery import app

logger = logging.getLogger(__name__)


@app.task(bind=True)
def do_expirate_checkin(self, checkin):
    """
    For this checkin:
    - call do_expirate() that change status and create workflow logs.
    - call BalaioRPC.expire_attempt API method to trigger action on Balaio's side.
    if API is down or RPC call raise exception -> task will be retried
    """
    rpc_client = BalaioRPC()
    logger.debug('[do_expirate_single_checkin] START process to expirate checkin (pk=%s) at %s' % (checkin.pk, datetime.datetime.now()))
    checkin.do_expirate()
    logger.info('[do_expirate_single_checkin] EXPIRED checkin pk: %s' % checkin.pk)
    if rpc_client.is_up():
        try:
            rpc_response = rpc_client.call('expire_attempt', [checkin.attempt_ref, ])
        except (Fault, ProtocolError, ValuerError) as e:
            logger.debug('[do_expirate_single_checkin] FAIL, retrying: exception' % e)
            raise self.retry(exc=e)
        logger.info('[do_expirate_single_checkin] BALAIO RPC method call success!.')
    else:
        raise self.retry(exc=Exception("Balaio is down!"))
        logger.error('[do_expirate_single_checkin] BALAIO RPC is Down. Could not call "expire_attempt" method.')
    logger.debug('[do_expirate_single_checkin] FINISH process at %s' % datetime.datetime.now())


@app.task(bind=True)
def process_expirable_checkins(self):
    """
    RUN: daily!
    For each checkin that is "expirable":
        call the method: checkin.do_expirate to change the checkins as expired
    """
    logger.debug('[do_expirate_checkins] START process at %s' % datetime.datetime.now())
    checkins = Checkin.objects.filter(status='pending', expiration_at__isnull=False)
    logger.info('[do_expirate_checkins] Found %s checkins matching conditions' % checkins.count())
    for checkin in checkins:
        logger.info('[do_expirate_checkins] Processing checkin (pk=%s)' % checkin.pk)
        if checkin.is_expirable:
            do_expirate_checkin.apply_async(args=[checkin, ])

    logger.debug('[do_expirate_checkins] FINISH process at %s' % datetime.datetime.now())
