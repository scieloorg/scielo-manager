# coding:utf-8
"""
Use this module to write functional tests for the pages and
screen components, only!
"""
import unittest

from django.conf import settings
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth
from waffle import Flag

from journalmanager.tests import modelfactories
from journalmanager.tests.tests_forms import _makePermission
from scielomanager.utils.modelmanagers.helpers import (
    _patch_userrequestcontextfinder_settings_setup,
    _patch_userrequestcontextfinder_settings_teardown,
    _makeUserProfile,
    )


class UserCollectionsSelectorTests(WebTest):

    def test_auto_define_a_collection_as_default_when_it_is_the_unique(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_collection', model='collection')
        user.user_permissions.add(perm)

        _makeUserProfile(user)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        page = self.app.get(reverse('index'), user=user)
        self.assertTrue(collection.name in page)
        # TODO: Test if the collection if marked as active

    def test_active_collection_for_user_with_a_single_collection(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_collection', model='collection')
        user.user_permissions.add(perm)
        _makeUserProfile(user)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)

        page = self.app.get(reverse('index'), user=user)
        self.assertIn('data-active-collection="%s"' % collection.name, page)

    def test_link_to_activate_collection_available_for_users_with_many_collections(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_collection', model='collection')
        user.user_permissions.add(perm)

        _makeUserProfile(user)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.make_default_to_user(user)
        collection2 = modelfactories.CollectionFactory.create(name='Chile')
        collection2.add_user(user)

        page = self.app.get(reverse('index'), user=user)
        self.assertIn('/toggle_active_collection/%s' % collection2.pk, page)


class UserAreasSelectorTests(WebTest):

    def test_logout_button(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_journal', model='journal')
        user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)
        collection.make_default_to_user(user)

        page = self.app.get(reverse('journal.index'), user=user)

        response = page.click(href=u'/accounts/logout/').follow()

        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertNotIn('_auth_user_id', self.client.session)


class RecentActivitiesTests(WebTest):

    def test_mailto_the_user_responsible_for_the_activity(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_journal', model='journal')
        user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)

        journal = modelfactories.JournalFactory(creator=user)
        journal.join(collection, user)

        page = self.app.get(reverse('index'), user=user)
        page.mustcontain('href="mailto:%s"' % user.email)

    def test_expected_table_row(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_journal', model='journal')
        user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)

        journal = modelfactories.JournalFactory(creator=user)
        journal.join(collection, user)

        page = self.app.get(reverse('index'), user=user)

        elem = page.lxml.xpath('//table[@id="activities"]/tbody/tr[2]/*')

        self.assertIn(collection.name, elem[0].text)
        self.assertIn(user.username, elem[1].xpath('a')[0].text)
        self.assertIn(journal.short_title, elem[2].xpath('a')[0].text)
        self.assertIn(journal.updated.strftime('%X'), elem[3].text)


class SectionsListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_sections_list_without_itens(self):
        """
        Asserts the message ``'There are no items.`` is shown
        when the sections list is empty.
        """
        perm_sponsor_list = _makePermission(perm='list_section',
                                            model='section',
                                            app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_list)

        journal = modelfactories.JournalFactory()
        journal.join(self.collection, self.user)

        page = self.app.get(reverse('section.index', args=[journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in page.body)


class JournalsListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_journals_list_without_itens(self):
        """
        Asserts the message ``'There are no items.`` is shown
        when the journals list is empty.
        """
        perm_journal_list = _makePermission(
            perm='list_journal',
            model='journal',
            app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_list)

        response = self.app.get(reverse('journal.index'), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_list_journal_permission_is_required(self):
        response = self.app.get(
            reverse('journal.index'), user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')


class PressReleasesListTests(WebTest):

    @_patch_userrequestcontextfinder_settings_setup
    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    @_patch_userrequestcontextfinder_settings_teardown
    def tearDown(self):
        """
        Restore the default values.
        """

    def test_pressrelease_list_without_itens(self):
        """
        Asserts the message ``'There are no items.`` is shown
        when the pressrelease list is empty.
        """
        journal = modelfactories.JournalFactory()
        journal.join(self.collection, self.user)

        perm_pressrelease_list = _makePermission(perm='list_pressrelease',
                                                 model='pressrelease',
                                                 app_label='journalmanager')
        self.user.user_permissions.add(perm_pressrelease_list)

        response = self.app.get(reverse('prelease.index', args=[journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_pressrelease_list_with_itens(self):
        """
        Asserts that threre is itens on press release list
        """
        journal = modelfactories.JournalFactory()
        journal.join(self.collection, self.user)

        issue = modelfactories.IssueFactory(journal=journal)
        perm_journal_list = _makePermission(perm='list_pressrelease',
                                            model='pressrelease',
                                            app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_list)

        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')

        pr = modelfactories.RegularPressReleaseFactory.create(issue=issue)
        pr.add_translation('The new york times Journal',
                           'Biggest rock entered the land was in 1969',
                           language)

        response = self.app.get(reverse('prelease.index',
                                args=[journal.pk]),
                                user=self.user)

        self.assertTrue('The new york times Journal' in response.body)

    def test_aheadpressrelease_list_with_itens(self):
        """
        Asserts that threre is itens on ahead press release list
        """
        journal = modelfactories.JournalFactory()
        journal.join(self.collection, self.user)

        perm_journal_list = _makePermission(perm='list_pressrelease',
                                            model='pressrelease',
                                            app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_list)

        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')

        pr = modelfactories.AheadPressReleaseFactory.create(journal=journal)
        pr.add_translation('Ahead Press Release on new york times',
                           'Biggest rock entered the land was in 1969',
                           language)

        response = self.app.get(reverse('prelease.index',
                                args=[journal.pk]) + '?tab=ahead',
                                user=self.user)
        self.assertTrue('Ahead Press Release on new york times' in response.body)


class IndexPageTests(WebTest):

    @_patch_userrequestcontextfinder_settings_setup
    def setUp(self):
        self.user = auth.UserF()

    @_patch_userrequestcontextfinder_settings_teardown
    def tearDown(self):
        """
        Restore the default values.
        """

    def test_logged_user_access_to_index(self):

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user)

        response = self.app.get(reverse('index'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_logged_editor_user_access_to_list_journal(self):
        Flag.objects.create(name='editorialmanager', everyone=True)
        editors_group = modelfactories.GroupFactory.create(name='Editors')
        perm = _makePermission(perm='list_editor_journal', model='journal', app_label='journalmanager')
        editors_group.permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user)

        self.user.groups.add(editors_group)

        response = self.app.get(reverse('index'), user=self.user)
        response = response.follow()

        self.assertTemplateUsed(response, 'journal/journal_list.html')

    def test_not_logged_user_access_to_index(self):
        response = self.app.get(reverse('index')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')


class UserIndexPageTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_logged_user_access(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        response = self.app.get(reverse('user.index'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/user_list.html')

    def test_remove_user_from_collection(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        other_user = auth.UserF(is_active=True)
        self.collection.add_user(other_user)

        response = self.app.get(reverse('user.index'), user=self.user)

        self.assertTrue(other_user.username in response.body)

        response = self.app.get(reverse('user.exclude_user_from_collection', args=[other_user.pk]), user=self.user)

        self.assertFalse(other_user.username in response.body)

    def test_logged_user_access_users_not_being_manager_of_the_collection(self):
        user = auth.UserF(is_active=True)
        response = self.app.get(reverse('user.index'), user=user).follow()

        self.assertTemplateUsed(response, 'accounts/unauthorized.html')
        response.mustcontain('not authorized to access')


class SponsorsListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_user_access_journals_list_without_itens(self):
        perm_sponsor_list = _makePermission(
            perm='list_sponsor',
            model='sponsor',
            app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_list)

        response = self.app.get(reverse('sponsor.index'), user=self.user)

        self.assertTrue('There are no items.' in response.body)


class IssuesListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory()
        self.journal.join(self.collection, self.user)

    def test_user_access_issue_list_without_itens(self):
        perm_issue_list = _makePermission(
            perm='list_issue',
            model='issue',
            app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_list)

        response = self.app.get(reverse('issue.index', args=[self.journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_user_reordering_issues_without_permissions(self):
        """
        Asserts that unpriviledged users can't reorder Issues
        """
        perm_issue_list = _makePermission(
            perm='list_issue',
            model='issue',
            app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_list)

        response = self.app.get(reverse('issue.reorder.ajax', args=[self.journal.pk]), user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_user_reordering_unknown_issues(self):
        """
        The server must respond a http 500 error code when
        it is requested to reorder issues that do not match
        the journal.
        """
        perm1 = _makePermission(
            perm='list_issue',
            model='issue',
            app_label='journalmanager')
        perm2 = _makePermission(
            perm='reorder_issue',
            model='issue',
            app_label='journalmanager')
        self.user.user_permissions.add(perm1)
        self.user.user_permissions.add(perm2)

        params = 'numbers=num%5B%5D%3D8036%26num%5B%5D%3D8035&issues_set=numbers-2005%7CNone'

        response = self.app.get(
            reverse('issue.reorder.ajax', args=[self.journal.pk]) + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        self.assertEqual(response.status_code, 500)

    def test_user_reordering_without_passing_params(self):
        """
        The server must respond a http 500 code and do nothing.
        """
        perm1 = _makePermission(
            perm='list_issue',
            model='issue',
            app_label='journalmanager')
        perm2 = _makePermission(
            perm='reorder_issue',
            model='issue',
            app_label='journalmanager')
        self.user.user_permissions.add(perm1)
        self.user.user_permissions.add(perm2)

        response = self.app.get(
            reverse('issue.reorder.ajax', args=[self.journal.pk]),
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        self.assertEqual(response.status_code, 500)


class SectionLookupForTranslationsTests(WebTest):
    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory()
        self.journal.join(self.collection, self.user)

    def test_existing_section(self):
        section = modelfactories.SectionFactory(journal=self.journal)
        section_title = modelfactories.SectionTitleFactory(section=section)

        params = 'j=%s&t=%s' % (self.journal.pk, section_title.title)
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=False
        )

        import json
        response_py = json.loads(response.content)
        self.assertEqual(response_py['exists'], True)
        self.assertEqual(response_py['message'], 'The section already exists.')

        title, code = response_py['sections'][0]
        self.assertEqual(title, unicode(section))
        self.assertEqual(code, section.actual_code)

    def test_new_section(self):

        params = 'j=%s&t=%s' % (self.journal.pk, 'newsection')
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=False
        )

        import json
        response_py = json.loads(response.content)
        self.assertEqual(response_py['exists'], False)
        self.assertEqual(response_py['message'], 'This is a new section.')

    def test_missing_journal_returns_400_status_code(self):
        params = '?t=%s' % ('newsection')
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_title_returns_400_status_code(self):
        params = '?j=%s' % (self.journal.pk)
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=True
        )

        self.assertEqual(response.status_code, 400)

    def test_non_xhr_request_returns_400_status_code(self):
        params = '?j=%s&t=%s' % (self.journal.pk, 'newsection')
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            user=self.user,
            expect_errors=True
        )

        self.assertEqual(response.status_code, 400)

    def test_sections_can_be_excluded_from_the_search(self):
        section = modelfactories.SectionFactory(journal=self.journal)
        section_title = modelfactories.SectionTitleFactory(section=section)

        params = 'j=%s&t=%s&exc=%s' % (self.journal.pk, section_title.title, section.pk)
        response = self.app.get(
            reverse('ajx.lookup_for_section_translation') + '?' + params,
            headers={'x-requested-with': 'XMLHttpRequest'},
            user=self.user,
            expect_errors=False
        )

        import json
        response_py = json.loads(response.content)
        self.assertEqual(response_py['exists'], False)
        self.assertEqual(response_py['message'], 'This is a new section.')
