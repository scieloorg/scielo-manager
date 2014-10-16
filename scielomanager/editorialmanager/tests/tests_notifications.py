# coding: utf-8

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings

from django_factory_boy import auth

from journalmanager.tests import modelfactories

from scielomanager import notifications


def generate_subject(action, subject=''):
    subject_prefix = settings.EMAIL_SUBJECT_PREFIX
    subject_suffix = notifications.EMAIL_DATA_BY_ACTION[action]['subject_sufix']
    return ' '.join([subject_prefix, subject, subject_suffix])


class IssueBoardMessageTests(TestCase):
    ACTIONS =  [
        'issue_add_no_replicated_board',
        'issue_add_replicated_board',
    ]

    def setUp(self):
        self.editor = auth.UserF(is_active=True)
        self.journal = modelfactories.JournalFactory.create(editor=self.editor)
        self.issue = modelfactories.IssueFactory(journal=self.journal)
        self.expected_recipients = [self.editor, ]

    def tearDown(self):
        """
        Restore the default values.
        """

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action(self):
        email_count = 0
        for action in self.ACTIONS:
            # with
            expected_subject = generate_subject(action=action, subject='')
            email_count += 1
            # when
            result = notifications.issue_board_replica(issue=self.issue, action=action)
            # then
            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)
