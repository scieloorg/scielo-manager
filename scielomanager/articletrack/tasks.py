# coding: utf-8
import datetime
import logging

from .balaio import BalaioRPC
from .models import Checkin
from scielomanager.celery import app
from articletrack.notifications import checkin_send_email_by_action
logger = logging.getLogger(__name__)


# ################## #
# CHECKIN EXPIRATION #
# ################## #


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


# ########################### #
# CHECKIN PROCEED TO CHECKOUT #
# ########################### #


@app.task(bind=True)
def do_proceed_to_checkout(self, checkin_id):
    """
    Call balaio to process checkin and proceed to checkout, if checkin comply with requirements
    """
    logger.debug('[do_proceed_to_checkout] START process to proceed with checkout of Checkin (pk=%s) at %s' % (checkin_id, datetime.datetime.now()))
    rpc_client = BalaioRPC()

    try:
        checkin = Checkin.objects.get(pk=checkin_id)
    except Checkin.DoesNotExist as e:
        logger.error('[do_proceed_to_checkout] FAIL while retrieving checkin (pk: %s), Checkin does not exist' % e)

    if checkin.is_scheduled_to_checkout:
        try:
            rpc_response = rpc_client.call('proceed_to_checkout', [checkin.attempt_ref, ])
        except Exception as e:
            logger.error('[do_proceed_to_checkout] FAIL, retrying. Exception: %s' % e)
            raise self.retry(exc=e)
        else:
            if rpc_response:
                checkin.do_confirm_checkout()
                logger.info('[do_proceed_to_checkout] Checkin (pk: %s) proceed to checkout successfully' % checkin_id)
                # notify users:
                checkin_send_email_by_action(checkin, 'checkout_confirmed')
            else:
                logger.error('BalaioRPC API method: "proceed_to_checkout" FAIL for checkin: %s. Response: %s' % (checkin.pk, rpc_response))
    else:
        logger.info('[do_proceed_to_checkout] Checkin does not comply the requirements to proceed to checkout')

    logger.debug('[do_proceed_to_checkout] FINISH process at %s' % datetime.datetime.now())


@app.task(bind=True)
def process_checkins_scheduled_to_checkout(self):
    logger.debug("[process_checkins_scheduled_to_checkout] START process at %s" % datetime.datetime.now())

    checkins = Checkin.objects.filter(status='checkout_scheduled')
    logger.info('[process_checkins_scheduled_to_checkout] Found %s checkins matching conditions' % checkins.count())

    for checkin in checkins:
        logger.info('[process_checkins_scheduled_to_checkout] Processing checkin (pk=%s)' % checkin.pk)
        do_proceed_to_checkout.apply_async(args=[checkin.pk, ])

    logger.debug('[process_checkins_scheduled_to_checkout] FINISH process at %s' % datetime.datetime.now())
