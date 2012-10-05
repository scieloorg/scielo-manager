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

        response = page.click(href=u'/accounts/logout/').follow().follow()

        self.assertTemplateUsed(response, 'registration/login.html')
        self.assertNotIn('_auth_user_id', self.client.session)
