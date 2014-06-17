# coding:utf-8
"""
Use this module to write functional tests for the view-functions, only!
"""
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from journalmanager.tests.tests_forms import _makePermission


HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


class LoginForm(WebTest):

    def test_the_user_must_provide_his_credentials(self):
        form = self.app.get(reverse('journalmanager.user_login')).forms[0]
        form['username'] = ''
        form['password'] = ''
        response = form.submit()

        self.assertTrue('not a valid username or password' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_right_username_and_wrong_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        form = self.app.get(reverse('journalmanager.user_login')).forms[0]
        form['username'] = 'foo'
        form['password'] = 'baz'
        response = form.submit()

        self.assertTrue('not a valid username or password' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_wrong_username_and_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        form = self.app.get(reverse('journalmanager.user_login')).forms[0]
        form['username'] = 'fuu'
        form['password'] = '123'
        response = form.submit()

        self.assertTrue('not a valid username or password' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_right_username_and_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.user_login')).forms[0]
        form['username'] = 'foo'
        form['password'] = '123'

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_right_username_and_right_password_for_inactive_user(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.user_login')).forms[0]
        form['username'] = 'foo'
        form['password'] = '123'

        response = form.submit()

        self.assertTrue('not a valid username or password' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_redirect_to_restricted_page_after_successful_login(self):
        user = auth.UserF(is_active=True)
        perm = _makePermission(perm='list_journal', model='journal')
        user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)
        collection.make_default_to_user(user)

        page = self.app.get(reverse('journal.index'), user=user)

        page.mustcontain('no items')


class UserMyAccountTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user)

    def test_logged_user_access_my_account(self):
        response = self.app.get(reverse('journalmanager.my_account'), user=self.user)

        self.assertTemplateUsed(response, 'accounts/my_account.html')

    def test_not_logged_user_access_my_account(self):
        response = self.app.get(reverse('journalmanager.my_account')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logged_user_access_user_configuration(self):
        user = auth.UserF(is_active=True)

        response = self.app.get(reverse('journalmanager.password_change'), user=self.user)

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)
        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms['chg_pwd']
        form['password'] = 123
        form['new_password'] = 321
        form['new_password_again'] = 321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/my_account.html')

    def test_logged_user_change_password_wrong_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)
        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms['chg_pwd']
        form['password'] = 1234
        form['new_password'] = 321
        form['new_password_again'] = 321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_wrong_new_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)
        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms['chg_pwd']
        form['password'] = 123
        form['new_password'] = 321123
        form['new_password_again'] = 321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_wrong_new_password_again(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)
        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms['chg_pwd']
        form['password'] = 123
        form['new_password'] = 321
        form['new_password_again'] = 321321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/password_change.html')
