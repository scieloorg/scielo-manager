# coding:utf-8
"""
Use this module to write functional tests for the view-functions, only!
"""
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django_factory_boy import auth

from journalmanager.tests import modelfactories


HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


class LoginForm(WebTest):

    def test_the_user_must_provide_his_credentials(self):
        form = self.app.get(reverse('index')).forms[0]
        form['username'] = ''
        form['password'] = ''
        response = form.submit()

        self.assertTrue('alert' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_right_username_and_wrong_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        form = self.app.get(reverse('index')).forms[0]
        form['username'] = 'foo'
        form['password'] = 'baz'
        response = form.submit()

        self.assertTrue('alert' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_wrong_username_and_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        form = self.app.get(reverse('index')).forms[0]
        form['username'] = 'fuu'
        form['password'] = '123'
        response = form.submit()

        self.assertTrue('alert' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_right_username_and_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('index')).forms[0]
        form['username'] = 'foo'
        form['password'] = '123'
        # there are 2 redirects =O
        response = form.submit().follow().follow()

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_right_username_and_right_password_for_inactive_user(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        form = self.app.get(reverse('index')).forms[0]
        form['username'] = 'foo'
        form['password'] = '123'

        response = form.submit()

        self.assertTrue('alert' in response.body)
        self.assertTemplateUsed(response, 'registration/login.html')
