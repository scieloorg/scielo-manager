# coding: utf-8
import datetime
import mocker

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from celery.task.base import Task

from scielomanager.tasks import send_mail
from . import modelfactories
from . import doubles
from articletrack.tasks import process_expirable_checkins, do_expires_checkin
from articletrack.models import Checkin


class CeleryTestCaseBase(TestCase, mocker.MockerTestCase):
    """
    http://stackoverflow.com/a/4559662/1503
    Here's an excerpt from my testing base class that stubs out the apply_async method
    and records to the calls to it (which includes Task.delay.) It's a little gross,
    but it's managed to fit my needs over the past few months I've been using it.
    """
    # @override_settings(TEST_RUNNER=TEST_RUNNER)
    def setUp(self):
        super(CeleryTestCaseBase, self).setUp()
        self.applied_tasks = []

        self.task_apply_async_orig = Task.apply_async

        @classmethod
        def new_apply_async(task_class, args=None, kwargs=None, **options):
            self.handle_apply_async(task_class, args, kwargs, **options)

        # monkey patch the regular apply_sync with our method
        Task.apply_async = new_apply_async

    def tearDown(self):
        super(CeleryTestCaseBase, self).tearDown()

        # Reset the monkey patch to the original method
        Task.apply_async = self.task_apply_async_orig

    def handle_apply_async(self, task_class, args=None, kwargs=None, **options):
        self.applied_tasks.append((task_class, tuple(args), kwargs))

    def assert_task_sent(self, task_class, *args, **kwargs):
        was_sent = any(task_class == task[0] and args == task[1] and kwargs == task[2]
                       for task in self.applied_tasks)
        self.assertTrue(was_sent, 'Task not called w/class %s and args %s' % (task_class, args))

    def assert_task_not_sent(self, task_class):
        was_sent = any(task_class == task[0] for task in self.applied_tasks)
        self.assertFalse(was_sent, 'Task was not expected to be called, but was. Applied tasks: %s' % self.applied_tasks)


class TestCheckinExpirationTask(CeleryTestCaseBase, mocker.MockerTestCase):

    def setUp(self):
        super(TestCheckinExpirationTask, self).setUp()
        self.now = datetime.datetime.now()
        days_delta = datetime.timedelta(days=settings.CHECKIN_EXPIRATION_TIME_SPAN)
        self.next_week_date = self.now + days_delta

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_do_expires_checkin(self):
        """
        create a checkin, that expire today, then call do_expires_checkin()
        """
        checkin = modelfactories.CheckinFactory(expiration_at=self.now)

        # to avoid making a request will replace it with a double
        balaio = self.mocker.replace('articletrack.balaio.BalaioRPC')
        balaio()
        self.mocker.result(doubles.BalaioRPCDouble())
        self.mocker.replay()

        result = do_expires_checkin.delay(checkin)
        self.assertTrue(result.successful())
        self.assertFalse(checkin.is_expirable)
        self.assertEqual('expired', checkin.status)

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_process_expirable_checkins(self):
        """
        create 10 checkins test, that expire today, then call process_expirable_checkins()
        """
        checkins = []

        for x in xrange(0, 10):
            checkin = modelfactories.CheckinFactory(expiration_at=self.now)
            checkins.append(checkin)

        balaio = self.mocker.replace('articletrack.balaio.BalaioRPC')
        for x in xrange(0, 10):
            balaio()
            self.mocker.result(doubles.BalaioRPCDouble())
        self.mocker.replay()

        result = process_expirable_checkins.delay()
        self.assertTrue(result.successful())

        for checkin in Checkin.objects.all():
            self.assertFalse(checkin.is_expirable)
            self.assertEqual('expired', checkin.status)
