# coding: utf-8
import datetime
from django.test import TestCase
from django_factory_boy import auth
from django.conf import settings
from articletrack import models
from . import modelfactories


class CommentTests(TestCase):

    def test_comment_ordering(self):
        ordering = models.Comment._meta.ordering
        self.assertEqual(ordering, ['created_at'])


class TicketTests(TestCase):

    def test_ticket_ordering(self):
        ordering = models.Ticket._meta.ordering
        self.assertEqual(ordering, ['started_at'])


class CheckinTests(TestCase):

    def test_new_checkin_is_pending_and_clear(self):

        checkin = modelfactories.CheckinFactory()
        # rejected_* is clear
        self.assertIsNone(checkin.rejected_by)
        self.assertIsNone(checkin.rejected_at)
        self.assertIsNone(checkin.rejected_cause)
        # reviewd_* is clear
        self.assertIsNone(checkin.reviewed_by)
        self.assertIsNone(checkin.reviewed_at)
        # accepted_* is clear
        self.assertIsNone(checkin.accepted_by)
        self.assertIsNone(checkin.accepted_at)
        # default status is pending
        self.assertEqual(checkin.status, 'pending')

    def test_reject_workflow_simple(self):

        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory()
        rejection_text = 'your checkin is bad, and you should feel bad!'  # http://www.quickmeme.com/Zoidberg-you-should-feel-bad/?upcoming

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user)

        # can be reviewed and can be rejected, then reject
        self.assertTrue(checkin.can_be_reviewed())
        self.assertTrue(checkin.can_be_rejected())
        checkin.do_reject(user, rejection_text)

        # check status and Integrity
        self.assertEqual(checkin.status, 'rejected')
        self.assertEqual(checkin.rejected_by, user)
        self.assertIsNotNone(checkin.rejected_at)

        # fields related with review and accept, must be clear
        self.assertIsNone(checkin.reviewed_by)
        self.assertIsNone(checkin.reviewed_at)
        self.assertIsNone(checkin.accepted_by)
        self.assertIsNone(checkin.accepted_at)

        # the checkin is not pending, reviewed, or accepted
        self.assertFalse(checkin.is_reviewed())
        self.assertFalse(checkin.is_accepted())
        self.assertFalse(checkin.can_be_accepted())
        self.assertFalse(checkin.can_be_reviewed())

        # checkin must be able to be sent to pending
        self.assertTrue(checkin.can_be_send_to_pending())
        self.assertEqual(checkin.rejected_cause, rejection_text)

    def test_accept_workflow_simple(self):
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory()

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(user)

        # do accept
        self.assertTrue(checkin.can_be_accepted())
        checkin.accept(user)

        # fields related with review and accept, must be clear
        self.assertEqual(checkin.accepted_by, user)
        self.assertIsNotNone(checkin.accepted_at)
        self.assertEqual(checkin.reviewed_by, user)
        self.assertIsNotNone(checkin.reviewed_at)

        # checkin must be accepted
        self.assertTrue(checkin.is_accepted())

    def test_accept_raises_ValueError_when_already_accepted(self):
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory()

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(user)

        # do accept
        self.assertTrue(checkin.can_be_accepted())
        checkin.accept(user)

        self.assertRaises(ValueError, lambda: checkin.accept(user))

    def test_accept_raises_ValueError_when_user_is_inactive(self):
        active_user = auth.UserF.build()
        inactive_user = auth.UserF.build(is_active=False)
        checkin = modelfactories.CheckinFactory()

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(active_user)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(active_user)

        # do accept
        self.assertTrue(checkin.can_be_accepted())
        self.assertRaises(ValueError, lambda: checkin.accept(inactive_user))

    def test_is_accepted_method_with_accepted_checkin(self):
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory()

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(user)

        # do accept
        self.assertTrue(checkin.can_be_accepted())
        checkin.accept(user)
        self.assertTrue(checkin.is_accepted())

    def test_is_accepted_method_without_accepted_checkin(self):
        checkin = modelfactories.CheckinFactory()
        self.assertFalse(checkin.is_accepted())

    def test_get_newest_checkin(self):
        user = auth.UserF(is_active=True)
        checkin1 = modelfactories.CheckinFactory(uploaded_at=datetime.datetime.now())

        self.assertEqual(checkin1.get_newest_checkin,
                         checkin1.article.checkins.order_by('uploaded_at')[0])

        checkin2 = modelfactories.CheckinFactory(accepted_by=user,
                                                 accepted_at=datetime.datetime.now(),
                                                 uploaded_at=datetime.datetime.now(),
                                                 status='accepted')
        self.assertEqual(checkin2.get_newest_checkin,
                         checkin2.article.checkins.order_by('uploaded_at')[0])

    def test_is_newest_checkin(self):
        user = auth.UserF(is_active=True)
        checkin1 = modelfactories.CheckinFactory()
        article = checkin1.article

        self.assertTrue(checkin1.is_newest_checkin)
        checkin2 = modelfactories.CheckinFactory(accepted_by=user,
                                                 accepted_at=datetime.datetime.now(),
                                                 status='accepted',
                                                 article=article,
                                                 uploaded_at=datetime.datetime.now())

        self.assertTrue(checkin2.is_newest_checkin)
        self.assertFalse(checkin1.is_newest_checkin)

    def test_new_checkin_has_correct_expiration_date_and_is_not_expirable(self):
        checkin = modelfactories.CheckinFactory()

        now = datetime.datetime.now()
        days_delta = datetime.timedelta(days=settings.CHECKIN_EXPIRATION_TIME_SPAN)
        next_week_date = now + days_delta

        self.assertEqual(checkin.expiration_at.date(), next_week_date.date())
        self.assertFalse(checkin.is_expirable)

    def test_if_expiration_date_is_today_then_checkin_is_expirable(self):
        now = datetime.datetime.now()

        checkin = modelfactories.CheckinFactory(expiration_at=now)

        self.assertEqual(checkin.expiration_at.date(), now.date())
        self.assertTrue(checkin.is_expirable)


class ArticleTests(TestCase):

    def test_is_accepted_method_with_accepted_checkins(self):

        user = auth.UserF(is_active=True)

        article = modelfactories.ArticleFactory()
        modelfactories.CheckinFactory(accepted_by=user,
                                      accepted_at=datetime.datetime.now(),
                                      status='accepted',
                                      article=article)

        self.assertTrue(article.is_accepted())

    def test_is_accepted_method_without_accepted_checkins(self):
        article = modelfactories.ArticleFactory()

        modelfactories.CheckinFactory(article=article)
        modelfactories.CheckinFactory(article=article)

        self.assertFalse(article.is_accepted())


class CheckinWorkflowLogTests(TestCase):
    """
    Every change of Checkin's status will generate a record with info about the current status of the checkin
    This way is possible to audit the actions made with the related checkin
    """

    def test_checkinworkflowlog_ordering(self):
        ordering = models.CheckinWorkflowLog._meta.ordering
        self.assertEqual(ordering, ['created_at'])

    def test_new_checkin_no_log(self):
        """
        generate a new checkin, must not generate any log
        """
        checkin = modelfactories.CheckinFactory()
        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin)
        self.assertEqual(logs.count(), 0)

    def test_checkin_send_to_review_log(self):
        checkin = modelfactories.CheckinFactory()
        user = auth.UserF(is_active=True)

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user)

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status, user=user)

        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].user, user)
        self.assertEqual(logs[0].description, models.MSG_WORKFLOW_SENT_TO_REVIEW)

    def test_checkin_do_review_log(self):
        checkin = modelfactories.CheckinFactory()
        user_send_to_review = auth.UserF(is_active=True)
        user_review = auth.UserF(is_active=True)

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user_send_to_review)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(user_review)

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status, user=user_review)

        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].user, user_review)
        self.assertEqual(logs[0].description, models.MSG_WORKFLOW_REVIEWED)

    def test_checkin_do_accept_log(self):
        checkin = modelfactories.CheckinFactory()
        user_send_to_review = auth.UserF(is_active=True)
        user_review = auth.UserF(is_active=True)
        user_accept = auth.UserF(is_active=True)

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user_send_to_review)

        # do review
        self.assertTrue(checkin.can_be_reviewed())
        checkin.do_review(user_review)

        # do accept
        self.assertTrue(checkin.can_be_accepted())
        checkin.accept(user_accept)

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status, user=user_accept)

        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].user, user_accept)
        self.assertEqual(logs[0].description, models.MSG_WORKFLOW_ACCEPTED)

    def test_checkin_do_reject_log(self):
        checkin = modelfactories.CheckinFactory()
        user_send_to_review = auth.UserF(is_active=True)
        user_reject = auth.UserF(is_active=True)
        rejection_text = 'your checkin is bad, and you should feel bad!'  # http://www.quickmeme.com/Zoidberg-you-should-feel-bad/?upcoming

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user_send_to_review)

        # do reject
        self.assertTrue(checkin.can_be_rejected())
        checkin.do_reject(user_reject, rejection_text)

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status, user=user_reject)

        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].user, user_reject)
        expected_description = "%s - Reason: %s" % (models.MSG_WORKFLOW_REJECTED, checkin.rejected_cause)
        self.assertEqual(logs[0].description, expected_description)

    def test_checkin_send_to_pending_log(self):
        checkin = modelfactories.CheckinFactory()
        user1_send_to_review = auth.UserF(is_active=True)
        user_reject = auth.UserF(is_active=True)
        user2_send_to_review = auth.UserF(is_active=True)
        rejection_text = 'your checkin is bad, and you should feel bad!'  # http://www.quickmeme.com/Zoidberg-you-should-feel-bad/?upcoming

        # send to review
        self.assertTrue(checkin.can_be_send_to_review())
        checkin.send_to_review(user1_send_to_review)

        # do reject
        self.assertTrue(checkin.can_be_rejected())
        checkin.do_reject(user_reject, rejection_text)

        # send to pending
        self.assertTrue(checkin.can_be_send_to_pending())
        checkin.send_to_pending(user2_send_to_review)

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status, user=user2_send_to_review)

        self.assertEqual(logs.count(), 1)
        self.assertEqual(logs[0].user, user2_send_to_review)
        self.assertEqual(logs[0].description, models.MSG_WORKFLOW_SENT_TO_PENDING)

    def test_do_expires_generate_log_entry(self):
        checkin = modelfactories.CheckinFactory()

        # do_expires
        checkin.do_expires()

        logs = models.CheckinWorkflowLog.objects.filter(checkin=checkin, status=checkin.status)

        self.assertEqual(logs.count(), 1)
        self.assertIsNone(logs[0].user)
        self.assertEqual(logs[0].status, 'expired')
        self.assertEqual(logs[0].description, models.MSG_WORKFLOW_EXPIRED)
