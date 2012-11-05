# coding:utf-8
"""
Use this module to write functional tests for the pages and
screen components, only!
"""
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from journalmanager.tests.tests_forms import _makePermission


class UserCollectionsSelectorTests(WebTest):

    def test_auto_define_a_collection_as_default_when_it_is_the_unique(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        page = self.app.get(reverse('index'), user=user)
        self.assertTrue(collection.name in page)
        # TODO: Test if the collection if marked as active

    def test_toggle_active_collection_unavailable_for_users_with_a_single_collection(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)

        page = self.app.get(reverse('index'), user=user)
        self.assertIn('<li class="disabled" id="edit-brasil">', page)

    def test_toggle_active_collection_available_for_users_with_many_collections(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.make_default_to_user(user)
        collection2 = modelfactories.CollectionFactory.create(name='Chile')
        collection2.add_user(user)

        page = self.app.get(reverse('index'), user=user)

        self.assertIn('activate-chile', page)


class UserAreasSelectorTests(WebTest):

    def test_logout_button(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_journal', model='journal')
        user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        page = self.app.get(reverse('journal.index'), user=user)

        response = page.click(href=u'/accounts/logout/').follow()

        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertNotIn('_auth_user_id', self.client.session)


class RecentActivitiesTests(WebTest):

    def test_mailto_the_user_responsible_for_the_activity(self):
        user = auth.UserF(is_active=True)
        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)
        journal = modelfactories.JournalFactory(collection=collection,
            creator=user)

        page = self.app.get(reverse('index'), user=user)
        page.mustcontain('href="mailto:%s"' % user.email)

    def test_expected_table_row(self):
        user = auth.UserF(is_active=True)
        collection = modelfactories.CollectionFactory.create(name='Brasil')
        collection.add_user(user)

        journal = modelfactories.JournalFactory(collection=collection,
            creator=user)

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

        journal = modelfactories.JournalFactory(collection=self.collection)

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
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_list)

        response = self.app.get(reverse('journal.index'), user=self.user)

        self.assertTrue('There are no items.' in response.body)


class IndexPageTests(WebTest):

    def test_logged_user_access_to_index(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('index'), user=user)

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_not_logged_user_access_to_index(self):
        response = self.app.get(reverse('index')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')


class UserIndexPageTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_logged_user_access(self):
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user, is_manager=True)

        response = self.app.get(reverse('user.index'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/user_dashboard.html')

    def test_logged_user_access_users_not_being_manager_of_the_collection(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('user.index'),
            user=user).follow()

        self.assertTemplateUsed(response, 'accounts/unauthorized.html')
        response.mustcontain('not authorized to access')


class SponsorsListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_user_access_journals_list_without_itens(self):
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_list)

        response = self.app.get(reverse('sponsor.index'),
            user=self.user)

        self.assertTrue('There are no items.' in response.body)


class IssuesListTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory(collection=self.collection)

    def test_user_access_issue_list_without_itens(self):
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_list)

        response = self.app.get(reverse('issue.index',
            args=[self.journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_user_reordering_issues_without_permissions(self):
        """
        Asserts that unpriviledged users can't reorder Issues
        """
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_list)

        response = self.app.get(reverse('issue.reorder.ajax',
            args=[self.journal.pk]), user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_user_reordering_unknown_issues(self):
        """
        The server must respond a http 500 error code when
        it is requested to reorder issues that do not match
        the journal.
        """
        perm1 = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        perm2 = _makePermission(perm='reorder_issue',
            model='issue', app_label='journalmanager')
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
        The server must respond a http 200 code and do nothing.
        """
        perm1 = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        perm2 = _makePermission(perm='reorder_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm1)
        self.user.user_permissions.add(perm2)

        response = self.app.get(
            reverse('issue.reorder.ajax', args=[self.journal.pk]),
            user=self.user,
        )

        self.assertEqual(response.body, '')
