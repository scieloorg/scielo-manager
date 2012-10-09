# coding:utf-8
"""
Use this module to write functional tests for the view-functions, only!
"""
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core import mail
from django_factory_boy import auth

from journalmanager.tests import modelfactories


HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


def _makePermission(perm, model, app_label='journalmanager'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


class SectionFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user)

    def test_basic_structure(self):
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user)

        self.assertTemplateUsed(form, 'journalmanager/add_section.html')
        form.mustcontain('section-form',
                         'csrfmiddlewaretoken',
                         'titles-TOTAL_FORMS',
                         'titles-INITIAL_FORMS',
                         'titles-MAX_NUM_FORMS',
                        )

    def test_POST_workflow_with_valid_formdata(self):
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        form['titles-0-title'] = 'Original Article'
        form.set('titles-0-language', language.pk)

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/section_dashboard.html')
        response.mustcontain('Original Article')

    def test_POST_workflow_with_invalid_formdata(self):
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')


class UserFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_basic_structure(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('user.add'), user=self.user)

        self.assertTemplateUsed(page, 'journalmanager/add_user.html')
        page.mustcontain('user-form',
                         'csrfmiddlewaretoken',
                         'usercollections-TOTAL_FORMS',
                         'usercollections-INITIAL_FORMS',
                         'usercollections-MAX_NUM_FORMS',
                        )

    def test_POST_workflow_with_valid_formdata(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'), user=self.user).forms['user-form']

        form['user-username'] = 'bazz'
        form['user-first_name'] = 'foo'
        form['user-last_name'] = 'bar'
        form['userprofile-0-email'] = 'bazz@spam.org'
        # form.set('asmSelect0', '1')  # groups
        form.set('usercollections-0-collection', self.collection.pk)  # collections

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/user_dashboard.html')
        response.mustcontain('bazz', 'bazz@spam.org')

        # check if an email has been sent to the new user
        self.assertTrue(len(mail.outbox), 1)
        self.assertIn('bazz@spam.org', mail.outbox[0].recipients())

        # check if basic state has been set
        self.assertTrue(response.context['user'].user_collection.get(
            pk=self.collection.pk))

    def test_POST_workflow_with_invalid_formdata(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'), user=self.user).forms['user-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')


class UserMyAccount(WebTest):

    def test_logged_user_access_my_account(self):
        user = auth.UserF(is_active=True)

        response = self.app.get(reverse('journalmanager.my_account'), user=user)

        self.assertTemplateUsed(response, 'accounts/my_account.html')

    def test_not_logged_user_acess_my_account(self):

        response = self.app.get(reverse('journalmanager.my_account')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_logged_user_access_user_configuration(self):
        user = auth.UserF(is_active=True)

        response = self.app.get(reverse('journalmanager.password_change'), user=user)

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_right_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms[1]
        form['password'] = 123
        form['new_password'] = 321
        form['new_password_again'] = 321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/my_account.html')

    def test_logged_user_change_password_wrong_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms[1]
        form['password'] = 1234
        form['new_password'] = 321
        form['new_password_again'] = 321

        response = form.submit().follow()
           
        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_wrong_new_password(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms[1]
        form['password'] = 123
        form['new_password'] = 321123
        form['new_password_again'] = 321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_logged_user_change_password_wrong_new_password_again(self):
        user = auth.UserF(username='foo',
                          password=HASH_FOR_123,
                          is_active=False)

        form = self.app.get(reverse('journalmanager.password_change'), user=user).forms[1]
        form['password'] = 123
        form['new_password'] = 321
        form['new_password_again'] = 321321

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'accounts/password_change.html')


class IndexPage(WebTest):

    def test_logged_user_access_to_index(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('index'), user=user)

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_not_logged_user_access_to_index(self):
        response = self.app.get(reverse('index')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')


class UserIndexPage(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_logged_user_access(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user, is_manager=True)

        response = self.app.get(reverse('user.index'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/user_dashboard.html')

    def test_logged_user_access_users_not_being_manager_of_the_collection(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('user.index'), user=user).follow()

        self.assertTemplateUsed(response, 'registration/login.html')


class FormJournal(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_logged_user_access_journal(self):
        perm = _makePermission(perm='change_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user)

        response = self.app.get(reverse('journal.add'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/add_journal.html')
