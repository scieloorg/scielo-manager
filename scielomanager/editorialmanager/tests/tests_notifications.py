# coding: utf-8

from django.core import mail
from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings
from django_factory_boy import auth
from journalmanager import models as jmodels
from journalmanager.tests import modelfactories
from editorialmanager import notifications
from . import modelfactories as editorial_modelfactories


class IssueBoardMessageTests(TestCase):
    ACTIONS = [
        'issue_add_no_replicated_board',
        'issue_add_replicated_board',
    ]

    def setUp(self):
        self.editor = auth.UserF(is_active=True)
        self.journal = modelfactories.JournalFactory.create(editor=self.editor)
        self.issue = modelfactories.IssueFactory(journal=self.journal)
        self.expected_recipients = [self.editor.email, ]
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

    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action_with_disable_notifications_for_editor(self):
        """
        for each action, test notifications are sent, but editor will have disable notifications
        """
        editor_profile = self.editor.get_profile()
        editor_profile.email_notifications = False
        editor_profile.save()
        # update self.expected_recipients
        self.expected_recipients.remove(editor_profile.user.email)

        for action in self.ACTIONS:
            # with
            expected_subject = self._make_subject(action)
            # when
            result = notifications.issue_board_replica(issue=self.issue, action=action)
            # then
            # no mail sent, since the only recipient: editor, "choose" to not receive emails
            self.assertIsNone(result)


class BoardMembersMessageTests(TestCase):
    ACTIONS = [
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

        self.collection = modelfactories.CollectionFactory.create()
        self.editor = auth.UserF(is_active=True)
        self.journal = modelfactories.JournalFactory.create(editor=self.editor)
        self.issue = modelfactories.IssueFactory(journal=self.journal)
        self.board = editorial_modelfactories.EditorialBoardFactory.create(issue=self.issue)
        self.member = editorial_modelfactories.EditorialMemberFactory.create(board=self.board)

        # link journal to collection
        jmodels.Membership.objects.create(journal=self.journal, collection=self.collection, created_by=auth.UserF(is_active=True))

        # link librarians and collection
        self.collection.add_user(self.librarian1)
        self.collection.add_user(self.librarian2)

        self.expected_recipients = []
        self.expected_bcc_recipients = [self.librarian1.email, self.librarian2.email, ]
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
            message = 'Audit Log change message goes here!'
            email_count += 1
            # when
            result = notifications.board_members_send_email_by_action(self.member, self.editor, message, action)
            # then
            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            self.assertEqual(len(self.expected_bcc_recipients), len(new_email.bcc))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)
            for recipient in self.expected_bcc_recipients:
                self.assertIn(recipient, new_email.bcc)


    @override_settings(CELERY_EAGER_PROPAGATES_EXCEPTIONS=True, CELERY_ALWAYS_EAGER=True, BROKER_BACKEND='memory')
    def test_each_action_with_disable_notifications_for_one_librarian(self):
        """
        for each action, test notifications are sent, but librarian2 will have disable notifications
        """
        librarian2_profile = self.librarian2.get_profile()
        librarian2_profile.email_notifications = False
        librarian2_profile.save()
        # remove it from expected_bcc_recipients
        self.expected_bcc_recipients.remove(librarian2_profile.user.email)

        email_count = 0
        for action in self.ACTIONS:
            # with
            expected_subject = self._make_subject(action)
            message = 'Audit Log change message goes here!'
            email_count += 1
            # when
            result = notifications.board_members_send_email_by_action(self.member, self.editor, message, action)
            # then
            self.assertTrue(result)
            self.assertEqual(len(mail.outbox), email_count)
            new_email = mail.outbox[-1]
            self.assertEqual(new_email.subject, expected_subject)
            self.assertEqual(len(self.expected_recipients), len(new_email.to))
            self.assertEqual(len(self.expected_bcc_recipients), len(new_email.bcc))
            for recipient in self.expected_recipients:
                self.assertIn(recipient, new_email.to)
            for recipient in self.expected_bcc_recipients:
                self.assertIn(recipient, new_email.bcc)
