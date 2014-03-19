# coding:utf-8
import json

from django_webtest import WebTest
from django.core.urlresolvers import reverse

from journalmanager.tests import modelfactories


class DownloadMarkupFilesTests(WebTest):
    def setUp(self):
        self.user = modelfactories.UserFactory(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()

        self.collection.add_user(self.user, is_manager=False)
        self.journal = self._makeJournal()

    def _makeJournal(self):

        journal = modelfactories.JournalFactory.create()

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=self.collection,
            journal=journal,
            publication_status=status
        )

        return journal


    def test_non_authenticated_users_are_redirected_to_login_page(self):
        response = self.app.get(
            reverse('export.markupfiles'),
            status=302
        ).follow()

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_authenticated_users_can_access(self):
        response = self.app.get(
            reverse('export.markupfiles'),
            user=self.user
        )

        self.assertTemplateUsed(response, 'export/markup_files.html')


class ListIssuesForMarkupFilesTests(WebTest):
    """
    Tests ajax interactions
    """
    def setUp(self):
        self.user = modelfactories.UserFactory(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()

        self.collection.add_user(self.user, is_manager=False)
        self.journal = self._makeJournal()

    def _makeJournal(self):

        journal = modelfactories.JournalFactory.create()

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=self.collection,
            journal=journal,
            publication_status=status
        )

        return journal

    def test_get_issues_pending_for_markup(self):
        """
        This interaction is performed by ajax requests, while
        querying for the list of issues waiting to be marked-up.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)
        issue2 = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=True)

        params = 'j={0}&all=0'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_get_all_issues(self):
        """
        This interaction is performed by ajax requests, while
        querying for the list of issues of a given journal.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)
        issue2 = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=True)

        params = 'j={0}&all=1'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)

    def test_get_all_issues_passing_true_as_the_boolean_value(self):
        """
        The recommended values to be used as boolean params are 0 and 1.
        But we are already prepared to handle: True, true, yes, Yes, on,
        On, y, Y. Anything else is handled as False.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)
        issue2 = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=True)

        params = 'j={0}&all=true'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)

    def test_get_all_issues_passing_On_as_the_boolean_value(self):
        """
        The recommended values to be used as boolean params are 0 and 1.
        But we are already prepared to handle: True, true, yes, Yes, on,
        On, y, Y. Anything else is handled as False.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)
        issue2 = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=True)

        params = 'j={0}&all=on'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 2)

    def test_unknown_values_passed_to_All_are_treated_as_false(self):
        """
        The recommended values to be used as boolean params are 0 and 1.
        But we are already prepared to handle: True, true, yes, Yes, on,
        On, y, Y. Anything else is handled as False.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)
        issue2 = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=True)

        params = 'j={0}&all=Bzz'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        response_data = json.loads(response.content)
        self.assertEqual(len(response_data), 1)

    def test_non_ajax_requests_gets_a_400_error(self):
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)

        params = 'j={0}&all=0'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            user=self.user,
            status=400
        )

        self.assertEqual(response.status_code, 400)

    def test_only_authenticated_users_can_query_issues(self):
        """
        Access to the Ajax that returns a list of issues for a
        given Journal.
        """
        issue = modelfactories.IssueFactory(
            journal=self.journal, is_marked_up=False)

        params = 'j={0}&all=0'.format(self.journal.pk)

        response = self.app.get(
            reverse('ajx.list_issues_for_markup_files') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            status=302
        ).follow()

        self.assertTemplateUsed(response, 'registration/login.html')
