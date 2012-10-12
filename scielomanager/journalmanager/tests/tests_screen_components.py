# coding:utf-8
"""
Use this module to write functional tests for the screen components, only!
"""
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from journalmanager.tests.tests import _makePermission


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
        self.assertNotIn('activate-brasil', page)

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