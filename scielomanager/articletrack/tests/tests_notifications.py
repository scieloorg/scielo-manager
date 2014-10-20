# coding: utf-8

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from django_factory_boy import auth

from articletrack.tests import modelfactories
from articletrack import models, notifications


class CheckinMessageTests(TestCase):
    ACTIONS =  [
        'checkin_reject',
        'checkin_review',
        'checkin_accept',
        'checkin_send_to_pending',
        'checkin_send_to_review',
        'checkin_send_to_checkout',
        'checkout_confirmed',
    ]

    def setUp(self):
        self.submitter = auth.UserF(is_active=True)
        self.checkin = modelfactories.CheckinFactory.create(submitted_by=self.submitter)
        member1 = auth.UserF(is_active=True)
        member2 = auth.UserF(is_active=True)
        member3 = auth.UserF(is_active=True)
        self.team = modelfactories.TeamFactory(name='test team')
        self.team.join(member1)
        self.team.join(member2)
        self.team.join(member3)
        self.team.join(self.submitter)
        self.expected_recipients = [user.email for user in [member1, member2, member3, self.submitter, ]]
        self.expected_recipients = list(set(self.expected_recipients))
        self.expected_subject_sufix_by_action = {
            'checkin_reject': 'Package rejected',
            'checkin_review': 'Package reviewed',
            'checkin_accept': 'Package accepted',
            'checkin_send_to_pending': 'Package send to pending',
            'checkin_send_to_review': 'Package sent to review',
            'checkin_send_to_checkout': 'Package sent to checkout',
            'checkout_confirmed': 'Package checkout confirmed',
        }

    def tearDown(self):
        """
        Restore the default values.
        """

    def _make_subject(self, action, subject=''):
        subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        subject_suffix = self.expected_subject_sufix_by_action[action]
        return ' '.join([subject_prefix, subject, subject_suffix])

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action(self):
        email_count = 0
        for action in self.ACTIONS:
            email_count += 1
            # when
            result = notifications.checkin_send_email_by_action(checkin=self.checkin, action=action)
            # then
            expected_subject = self._make_subject(action, subject=self.checkin.package_name)

            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)


class TicketMessageTests(TestCase):
    ACTIONS = [
        'ticket_add',
        'ticket_edit',
        'ticket_close',
    ]

    def setUp(self):
        self.submitter = auth.UserF(is_active=True)
        self.checkin = modelfactories.CheckinFactory.create(submitted_by=self.submitter)
        self.ticket = modelfactories.TicketFactory.create(article=self.checkin.article)
        member1 = auth.UserF(is_active=True)
        member2 = auth.UserF(is_active=True)
        member3 = auth.UserF(is_active=True)
        self.team = modelfactories.TeamFactory(name='test team')
        self.team.join(member1)
        self.team.join(member2)
        self.team.join(member3)
        self.team.join(self.submitter)
        self.expected_recipients = [user.email for user in [member1, member2, member3, self.submitter, self.ticket.author]]
        self.expected_recipients = list(set(self.expected_recipients))
        self.expected_subject_sufix_by_action = {
            'ticket_add': 'Ticket created',
            'ticket_edit': 'Ticket edited',
            'ticket_close': 'Ticket closed',
        }

    def _make_subject(self, action, subject=''):
        subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        subject_suffix = self.expected_subject_sufix_by_action[action]
        return ' '.join([subject_prefix, subject, subject_suffix])

    def tearDown(self):
        """
        Restore the default values.
        """

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action(self):
        email_count = 0
        for action in self.ACTIONS:
            email_count += 1
            # when
            result = notifications.ticket_send_mail_by_action(ticket=self.ticket, action=action)
            # then
            expected_subject = self._make_subject(action)

            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)


class CommentMessageTests(TestCase):
    ACTIONS = [
        'comment_created',
        'comment_edit',
    ]

    def setUp(self):
        self.submitter = auth.UserF(is_active=True)
        self.checkin = modelfactories.CheckinFactory.create(submitted_by=self.submitter)
        self.ticket = modelfactories.TicketFactory.create(article=self.checkin.article)
        self.comment = modelfactories.CommentFactory.create(ticket=self.ticket)
        member1 = auth.UserF(is_active=True)
        member2 = auth.UserF(is_active=True)
        member3 = auth.UserF(is_active=True)
        self.team = modelfactories.TeamFactory(name='test team')
        self.team.join(member1)
        self.team.join(member2)
        self.team.join(member3)
        self.team.join(self.submitter)
        self.expected_recipients = [user.email for user in [member1, member2, member3, self.submitter, self.ticket.author]]
        self.expected_recipients = list(set(self.expected_recipients))
        self.expected_subject_sufix_by_action = {
            'comment_created': 'New comment',
            'comment_edit': 'Comment edited',
        }

    def tearDown(self):
        """
        Restore the default values.
        """

    def _make_subject(self, action, subject=''):
        subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        subject_suffix = self.expected_subject_sufix_by_action[action]
        return ' '.join([subject_prefix, subject, subject_suffix])

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action(self):
        email_count = 0
        message_class = notifications.TicketMessage
        for action in self.ACTIONS:
            email_count += 1
            # when
            result = notifications.comment_send_mail_by_action(comment=self.comment, action=action)
            # then
            expected_subject = self._make_subject(action)

            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)
