# -*- encoding:utf-8 -*-
import os

from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission
from django.core.urlresolvers import reverse
from django.core import mail

from journalmanager.tests import tests_assets
from journalmanager.models import Collection
from journalmanager.models import Journal
from journalmanager.models import Sponsor
from journalmanager.models import Issue
from journalmanager.models import UserCollections
from journalmanager.models import Section

from journalmanager.forms import JournalForm


def with_sample_journal(func):
    """
    Decorator that creates a sample Journal instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_journal()
        func(self)
        self._destroy_journal()
    return decorated


def with_sample_issue(func):
    """
    Decorator that creates a sample Issue instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_issue()
        func(self)
        self._destroy_issue()
    return decorated


def with_sample_sponsor(func):
    """
    Decorator that creates a sample Sponsor instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_sponsor()
        func(self)
        self._destroy_sponsor()
    return decorated


class LoggedInViewsTest(TestCase):
    """
    Tests views that need logged in users.

    The setUp method creates a new user and authenticates with it. If you want
    a journal to be created at the beginning and then be destructed after each
    testcase, decorate your testcase methods with ``with_sample_journal``.
    """

    def setUp(self):
        """
        Creates an authenticated session using a dummy user.
        """

        #add a dummy user
        self.user = tests_assets.get_sample_creator()
        self.collection = tests_assets.get_sample_collection()
        self.user.save()
        self.collection.save()
        self.usercollections = tests_assets.get_sample_usercollections(self.user, self.collection)
        self.usercollections.save()

        self.client = Client()
        self.client.login(username='dummyuser', password='123')

    def tearDown(self):
        """
        Destroying the data
        """
        for m in [Journal, Sponsor, Issue, UserCollections, User, Section, Collection]:
            m.objects.all().delete()

    def _create_journal(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection, ]
        sample_sponsor.save()

        sample_use_license = tests_assets.get_sample_uselicense()
        sample_use_license.save()

        sample_journal.use_license = sample_use_license
        sample_journal.pub_status_changed_by = self.user
        sample_journal.collection = self.collection
        sample_journal.save()
        sample_journal.sponsor = [sample_sponsor, ]
        sample_journal.save()

        sample_journal.save()

    def _destroy_journal(self):
        pass

    def _create_issue(self):
        self._create_journal()
        sample_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xe3o Paulo)')
        sample_issue = tests_assets.get_sample_issue()

        sample_issue.journal = sample_journal
        sample_issue.save()

        sample_section = tests_assets.get_sample_section()
        sample_section.journal = sample_journal
        sample_section.save()

    def _destroy_issue(self):
        pass

    def _create_sponsor(self):
        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.save()
        sample_sponsor.collections = [self.collection]
        sample_sponsor.save()

    def _destroy_sponsor(self):
        pass

    def test_add_journal_with_cover(self):
        """
        Covered cases:
        * Accessing the form
        * Submission with missing data
        * Submission with all required data
        * Send with image cover
        """
        #empty form
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.collection = self.collection
        sample_sponsor.save()

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        #get the image test
        image_test_cover = open(os.path.dirname(__file__) + '/image_test/image_test_cover.jpg')

        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-sponsor': [sample_sponsor.pk],
                                         'journal-use_license': sample_uselicense.pk,
                                         'journal-collection': self.usercollections.pk,
                                         'journal-languages': [sample_language.pk],
                                         'journal-abstract_keyword_languages': [sample_language.pk],
                                         'mission-0-language': sample_language.pk,
                                         'journal-cover': image_test_cover}))

        self.assertRedirects(response, reverse('journal.index'))

    def test_add_journal_with_logo(self):
        """
        Covered cases:
        * Accessing the form
        * Submission with missing data
        * Submission with all required data
        * Send with image logo
        """
        #empty form
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        sample_sponsor = tests_assets.get_sample_sponsor()
        sample_sponsor.collection = self.collection
        sample_sponsor.save()

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        #get the image test
        image_test_logo = open(os.path.dirname(__file__) + '/image_test/image_test_logo.jpg')

        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform({'journal-sponsor': [sample_sponsor.pk],
                                         'journal-use_license': sample_uselicense.pk,
                                         'journal-collection': self.usercollections.pk,
                                         'journal-languages': [sample_language.pk],
                                         'journal-abstract_keyword_languages': [sample_language.pk],
                                         'mission-0-language': sample_language.pk,
                                         'journal-logo': image_test_logo}))

        self.assertRedirects(response, reverse('journal.index'))

    @with_sample_journal
    def test_toggle_sponsor_availability(self):
        pre_sponsor = Sponsor.objects.all()[0]
        response = self.client.get(reverse('sponsor.toggle_availability', args=[pre_sponsor.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_sponsor = Sponsor.objects.all()[0]

        self.assertEqual(pre_sponsor, pos_sponsor)
        self.assertTrue(pre_sponsor.is_trashed is not pos_sponsor.is_trashed)

        response = self.client.get(reverse('sponsor.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_issue
    def test_toggle_issue_availability(self):
        pre_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.toggle_availability', args=[pre_issue.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_issue = Issue.objects.all()[0]

        self.assertEqual(pre_issue, pos_issue)
        self.assertTrue(pre_issue.is_trashed is not pos_issue.is_trashed)

        response = self.client.get(reverse('issue.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    def test_toggle_user_availability(self):
        pre_user = User.objects.all()[0]
        response = self.client.get(reverse('user.toggle_availability', args=[pre_user.pk]), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        pos_user = User.objects.all()[0]

        self.assertEqual(pre_user, pos_user)
        self.assertTrue(pre_user.is_active is not pos_user.is_active)

        response = self.client.get(reverse('user.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 400)

    @with_sample_sponsor
    def test_sponsor_availability_list(self):
        sponsor = Sponsor.objects.all()[0]
        response = self.client.get(reverse('sponsor.index'))
        for spr in response.context['objects_sponsor'].object_list:
            self.assertEqual(spr.is_trashed, False)

        #change atribute is_available
        sponsor.is_trashed = True
        sponsor.save()

        response = self.client.get(reverse('sponsor.index') + '?is_available=0')
        self.assertEqual(len(response.context['objects_sponsor'].object_list), 0)

    @with_sample_issue
    def test_issue_availability_list(self):

        first_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.index', args=[first_issue.journal.pk]))

        for year, volumes in response.context['issue_grid'].items():
            for volume, issues in volumes.items():
                for issue in issues['numbers']:
                    self.assertEqual(issue.is_trashed, False)

        #change atribute is_available
        first_issue.is_trashed = True
        first_issue.save()

        response = self.client.get(reverse('issue.index', args=[first_issue.journal.pk]) + '?is_available=0')

        for year, volumes in response.context['issue_grid'].items():
            for volume, issues in volumes.items():
                for issue in issues['numbers']:
                    self.assertEqual(issue.is_trashed, True)

    def test_contextualized_collection_field_on_add_journal(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Journal, he can only bind that Journal to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.models import get_user_collections
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collection'].queryset:
            self.assertTrue(qset_item in user_collections)

    def test_contextualized_collection_field_on_add_sponsor(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Sponsor, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.models import get_user_collections
        response = self.client.get(reverse('sponsor.add'))
        self.assertEqual(response.status_code, 200)

        user_collections = [collection.collection for collection in get_user_collections(self.user.pk)]

        for qset_item in response.context['add_form'].fields['collections'].queryset:
            self.assertTrue(qset_item in user_collections)

    @with_sample_journal
    def test_contextualized_language_field_on_add_section(self):
        """
        A user has a manytomany relation to Collection entities. So, when a
        user is registering a new Section, he can only bind it to
        the Collections he relates to.

        Covered cases:
        * Check if all collections presented on the form are related to the
          user.
        """
        from journalmanager.models import Journal
        journal = Journal.objects.all()[0]

        sample_language = tests_assets.get_sample_language()
        sample_language.save()

        journal.languages.add(sample_language)

        response = self.client.get(reverse('section.add', args=[journal.pk]))
        self.assertEqual(response.status_code, 200)

        for qset_item in response.context['section_title_formset'].forms[0].fields['language'].queryset:
            self.assertTrue(qset_item in journal.languages.all())

    @with_sample_journal
    def test_journal_trash(self):
        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['trashed_docs'].object_list), 0)

        journal = Journal.objects.all()[0]
        journal.is_trashed = True
        journal.save()

        response = self.client.get(reverse('trash.listing'))
        self.assertEqual(len(response.context['trashed_docs'].object_list), 1)



class ComponentsTest(TestCase):
    def test_ISSNField_validation(self):

        valid_issns = ['1678-5320','0044-5967','0102-8650','2179-975X','1413-7852','0103-2100',]
        invalid_issns = ['A123-4532','1t23-8979','0900-090900','9827-u982','8992-8u77','1111-111Y',]

        for issn in valid_issns:
            form = JournalForm({'print_issn': issn,})
            self.assertTrue(form.errors.get('print_issn') is None)
            del(form)

        for issn in invalid_issns:
            form = JournalForm({'print_issn': issn,})
            self.assertEqual(form.errors.get('print_issn')[0], u'Enter a valid ISSN.')
            del(form)

class ModelBackendTest(TestCase):
    """
    Testa as especializações de metodos de backend ModelBackend
    """

    def setUp(self):
        #add a dummy user
        self.user = tests_assets.get_sample_creator()
        self.user.save()
        self.profile = tests_assets.get_sample_userprofile(user=self.user)
        self.profile.save()

    def test_authenticate(self):
        """
        test_authentication

        Covered Tests
        1. authenticating user with true username and password
        2. authenticating user with true username and wrong password
        3. authenticating user with true email and password
        4. authenticating user with true email and wrong password
        5. authenticating user with wrong username/email and password
        """
        from scielomanager.journalmanager.backends import ModelBackend

        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('dummyuser', '123')
        self.assertEqual(auth_response, self.user)

        auth_response = mbkend.authenticate('dummyuser', 'fakepasswd')
        self.assertEqual(auth_response, None)

        auth_response = mbkend.authenticate('dev@scielo.org', '123')
        self.assertEqual(auth_response, self.user)

        auth_response = mbkend.authenticate('dev@scielo.org', 'fakepasswd')
        self.assertEqual(auth_response, None)

        auth_response = mbkend.authenticate('fakeuser', 'fakepasswd')
        self.assertEqual(auth_response, None)
