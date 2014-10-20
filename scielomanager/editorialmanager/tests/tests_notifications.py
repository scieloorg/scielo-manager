# coding: utf-8

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from editorialmanager import notifications
from . import modelfactories as editorial_modelfactories


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
        self.expected_subject_sufix_by_action = {
            'issue_add_no_replicated_board': "Issue Board can't be replicated",
            'issue_add_replicated_board': "Issue has a new replicated board",
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
            # with
            expected_subject = self._make_subject(action)
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


class BoardMembersMessageTests(TestCase):
    ACTIONS =  [
        'board_add_member',
        'board_edit_member',
        'board_delete_member',
    ]

    def setUp(self):
        # create librarian group and those members
        self.librarian_group = modelfactories.GroupFactory(name="Librarian")
        self.librarian1 = auth.UserF(is_active=True)
        self.librarian2 = auth.UserF(is_active=True)

        self.librarian1.groups.add(self.librarian_group)
        self.librarian1.save()

        self.librarian2.groups.add(self.librarian_group)
        self.librarian2.save()

        self.editor = auth.UserF(is_active=True)
        self.journal = modelfactories.JournalFactory.create(editor=self.editor)
        self.issue = modelfactories.IssueFactory(journal=self.journal)
        self.board = editorial_modelfactories.EditorialBoardFactory.create(issue=self.issue)
        self.member = editorial_modelfactories.EditorialMemberFactory.create(board=self.board)

        self.expected_recipients = [self.librarian1, self.librarian2, ]
        self.expected_subject_sufix_by_action = {
            'board_add_member': "Member of the journal board, was added",
            'board_edit_member': "Member of the journal board, was edited",
            'board_delete_member': "Member of the journal board, was deleted",
        }

    def _make_subject(self, action, subject=''):
        subject_prefix = settings.EMAIL_SUBJECT_PREFIX
        subject_suffix = self.expected_subject_sufix_by_action[action]
        return ' '.join([subject_prefix, subject, subject_suffix])

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action(self):
        email_count = 0
        for action in self.ACTIONS:
            # with
            expected_subject = self._make_subject(action)
            message = ''
            email_count += 1
            # when
            result = notifications.board_members_send_email_by_action(self.member, self.editor, message, action)
            # then
            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)
