# coding: utf-8

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.conf import settings
from journalmanager.tests import modelfactories


class AccessPageReportTests(WebTest):

    def setUp(self):
        # create a group 'Librarian'
        self.group = modelfactories.GroupFactory(name="Librarian")
        # create a user and set group 'Librarian'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(self.group)
        self.user.save()

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

    def test_non_authenticated_users_access_to_report_area(self):
        response = self.app.get(reverse('report.index')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')

    def test_authenticated_users_with_access_to_report_area(self):
        response = self.app.get(reverse('report.index'), user=self.user)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'report/report_list.html')

    def test_authenticated_users_without_access_to_report_area(self):
        # create a group 'Trainee'
        group = modelfactories.GroupFactory(name="Trainee")
        # create a user and set group 'Trainee'
        user = modelfactories.UserFactory(is_active=True)
        user.groups.add(group)
        user.save()

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user, is_manager=False)
        collection.make_default_to_user(user)

        response = self.app.get(reverse('report.index'), user=user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_authenticated_users_with_access_to_see_report_link(self):
        response = self.app.get('/', user=self.user)

        response.mustcontain('Reports')
        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_authenticated_users_without_access_to_see_report_link(self):
        # create a group 'Trainee'
        group = modelfactories.GroupFactory(name="Trainee")
        # create a user and set group 'Trainee'
        user = modelfactories.UserFactory(is_active=True)
        user.groups.add(group)
        user.save()

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user, is_manager=False)
        collection.make_default_to_user(user)

        response = self.app.get('/', user=user)

        self.assertTrue('Reports' not in response.content)
        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')
