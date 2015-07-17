# coding: utf-8

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.conf import settings
from journalmanager.tests import modelfactories
from editorialmanager.models import EditorialMember, EditorialBoard
from editorialmanager.tests import modelfactories as editorial_modelfactories


class AccessReportMemberListTests(WebTest):

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

        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

    def test_non_authenticated_users_access_to_member_list_report(self):
        response = self.app.get(reverse('report.member_list'))

        self.assertEqual(response.status_code, 302)

    def test_authenticated_users_access_to_member_list_report(self):
        response = self.app.get(reverse('report.member_list'), user=self.user)

        response.mustcontain('Editorial Member Report')
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list'), user=self.user)

        response.mustcontain(member.first_name)
        response.mustcontain(member.last_name)
        response.mustcontain(member.institution)
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_collection(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?collection=' + str(self.collection.id), user=self.user)

        response.mustcontain(member.first_name)
        response.mustcontain(member.last_name)
        response.mustcontain(member.institution)
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_invalid_collection(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?collection=9999', user=self.user)

        response.mustcontain('No result found')
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_country(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?country=' + str(member.country), user=self.user)

        response.mustcontain(member.first_name)
        response.mustcontain(member.last_name)
        response.mustcontain(member.country.name)
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_invalid_country(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?country=OKII', user=self.user)

        response.mustcontain('No result found')
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_invalid_study_area(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?study_area=Primeira Guerra Mundial', user=self.user)

        response.mustcontain('No result found')
        self.assertEqual(response.status_code, 200)

    def test_content_in_member_list_report_with_filter_by_invalid_subject_area(self):

        member = editorial_modelfactories.EditorialMemberFactory.create()
        member.board = EditorialBoard.objects.create(issue=self.issue)
        member.save()

        response = self.app.get(reverse('report.member_list') + '?subject_category=9', user=self.user)

        response.mustcontain('No result found')
        self.assertEqual(response.status_code, 200)


class DownloadReportMemberCSVFileTests(WebTest):

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

        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

    def test_non_authenticated_users_are_redirected_to_login_page(self):
        response = self.app.get(
            reverse('report.export_csv', args=[self.journal.id]),
            status=302
        ).follow()

        self.assertTemplateUsed(response, 'registration/login.html')
