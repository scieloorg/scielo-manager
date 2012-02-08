# coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse

from scielomanager.journalmanager import tests_assets
from scielomanager.journalmanager.models import Collection
from scielomanager.journalmanager.models import UserProfile
from scielomanager.journalmanager.models import Journal
from scielomanager.journalmanager.models import Institution
from scielomanager.journalmanager.models import Issue

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
    Decorator that creates a sample Journal instance
    and destructs it at the end of the execution.
    """
    def decorated(self=None):
        self._create_issue()
        func(self)
        self._destroy_issue()
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
        self.profile = tests_assets.get_sample_userprofile(self.user, self.collection)
        self.profile.save()

        self.client = Client()
        self.client.login(username='dummyuser', password='123')

    def _create_journal(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_institution = tests_assets.get_sample_institution()
        sample_institution.collection = self.collection
        sample_institution.save()

        sample_journal.institution = sample_institution
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

    def _destroy_journal(self):
        Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xe3o Paulo)').delete()

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
        self._destroy_journal

    def test_add_journal(self):
        #empty form
        response = self.client.get(reverse('journal.add'))
        self.assertEqual(response.status_code, 200)

        sample_institution = tests_assets.get_sample_institution()
        sample_institution.collection = self.collection
        sample_institution.save()

        sample_uselicense = tests_assets.get_sample_uselicense()
        sample_uselicense.save()

        #add journal - missing required
        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform())

        self.assertTrue('field required' in response.content.lower())

        #add journal - must be added
        sample_indexing_coverage = tests_assets.get_sample_indexing_coverage()
        sample_indexing_coverage.save()

        response = self.client.post(reverse('journal.add'),
            tests_assets.get_sample_journal_dataform(institution=sample_institution.pk,
                                                     use_license=sample_uselicense.pk,
                                                     collections=[self.collection.pk],
                                                     indexing_coverage=[sample_indexing_coverage.pk]))

        self.assertRedirects(response, reverse('journal.index'))

        #edit journal - must be changed
        testing_journal = Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)')
        response = self.client.post(reverse('journal.edit', args = (testing_journal.pk,)),
            tests_assets.get_sample_journal_dataform(title = 'Modified Title',
                                                     institution = sample_institution.pk,
                                                     use_license = sample_uselicense.pk,
                                                     collections = [self.collection.pk],
                                                     indexing_coverage = [sample_indexing_coverage.pk]))

        self.assertRedirects(response, reverse('journal.index'))
        modified_testing_journal = Journal.objects.get(title = 'Modified Title')
        self.assertEqual(testing_journal, modified_testing_journal)

    def test_add_institution(self):
        #empty form
        response = self.client.get(reverse('institution.add'))
        self.assertEqual(response.status_code, 200)

        #add institution - must be added
        response = self.client.post(reverse('institution.add'),
            tests_assets.get_sample_institution_dataform(collections=[self.collection.pk]))

        self.assertRedirects(response, reverse('institution.index'))

        #edit institution - must be changed
        testing_institution = Institution.objects.get(name = u'Associação Nacional de História - ANPUH')
        response = self.client.post(reverse('institution.edit', args = (testing_institution.pk,)),
            tests_assets.get_sample_institution_dataform(name = 'Modified Title',
                                                         collections = [self.collection.pk]))

        self.assertRedirects(response, reverse('institution.index'))
        modified_testing_institution = Institution.objects.get(name = 'Modified Title')
        self.assertEqual(testing_institution, modified_testing_institution)

    @with_sample_journal
    def test_journal_index(self):
        """
        View: journal_index

        Tests url dispatch and values returned by the view to the template
        """

        response = self.client.get('/journal/')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('journals' in response.context)
        self.assertTrue('collection' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
            unicode(response.context['journals'].object_list[0].title))
        self.assertTrue(1, len(response.context['journals'].object_list))

    @with_sample_journal
    def test_institution_index(self):
        """
        View: institution_index

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/institution/')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('institutions' in response.context)
        self.assertTrue('collection' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH',
            unicode(response.context['institutions'].object_list[0].name))
        self.assertTrue(1, len(response.context['institutions'].object_list))

    @with_sample_journal
    def test_search_journal(self):
        """
        View: search_journal

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/search/?q=Arquivos')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('journals' in response.context)
        self.assertTrue('collection' in response.context)

        #testing content
        self.assertEqual(u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)', unicode(response.context['journals'].object_list[0].title))
        self.assertTrue(1, len(response.context['journals'].object_list))

    @with_sample_journal
    def test_search_institution(self):
        """
        View: search_institution

        Tests url dispatch and values returned by the view to the template
        """
        response = self.client.get('/journal/institution/search/?q=Nacional')

        #url dispatcher
        self.assertEqual(response.status_code, 200)

        #values passed to template
        self.assertTrue('institutions' in response.context)
        self.assertTrue('collection' in response.context)

        #testing content
        self.assertEqual(u'Associação Nacional de História - ANPUH', unicode(response.context['institutions'].object_list[0].name))
        self.assertTrue(1, len(response.context['institutions'].object_list))

    @with_sample_journal
    def test_toggle_journal_availability(self):
        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.toggle_availability', args=[pre_journal.pk]))
        pos_journal = Journal.objects.all()[0]

        self.assertEqual(pre_journal, pos_journal)
        self.assertRedirects(response, reverse('journal.index'))
        self.assertTrue(pre_journal.is_available is not pos_journal.is_available)

        response = self.client.get(reverse('journal.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_journal
    def test_toggle_institution_availability(self):
        pre_institution = Institution.objects.all()[0]
        response = self.client.get(reverse('institution.toggle_availability', args=[pre_institution.pk]))
        pos_institution = Institution.objects.all()[0]

        self.assertEqual(pre_institution, pos_institution)
        self.assertRedirects(response, reverse('institution.index'))
        self.assertTrue(pre_institution.is_available is not pos_institution.is_available)

        response = self.client.get(reverse('institution.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_issue
    def test_toggle_issue_availability(self):
        pre_issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.toggle_availability', args=[pre_issue.pk]))
        pos_issue = Issue.objects.all()[0]

        self.assertEqual(pre_issue, pos_issue)
        self.assertRedirects(response, reverse('issue.index', args=[pre_issue.journal.pk]))
        self.assertTrue(pre_issue.is_available is not pos_issue.is_available)

        response = self.client.get(reverse('issue.toggle_availability', args=[9999999]))
        self.assertEqual(response.status_code, 404)

    @with_sample_journal
    def test_journal_availability_list(self):

        pre_journal = Journal.objects.all()[0]
        response = self.client.get(reverse('journal.index') + '?is_available=1')
        self.assertEqual(response.context['journals'].object_list[0].is_available, True)

        #change object atribute is_available
        pre_journal.is_available = False
        pre_journal.save()

        response = self.client.get(reverse('journal.index') + '?is_available=0')
        self.assertEqual(response.context['journals'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['journals'].object_list), 1)


    @with_sample_journal
    def test_institution_availability_list(self):

        institution = Institution.objects.all()[0]
        response = self.client.get(reverse('institution.index'))
        self.assertEqual(response.context['institutions'].object_list[0].is_available, True)

        #change atribute is_available
        institution.is_available = False
        institution.save()

        response = self.client.get(reverse('institution.index') + '?is_available=0')
        self.assertEqual(response.context['institutions'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['institutions'].object_list), 1)


    @with_sample_issue
    def test_issue_availability_list(self):

        issue = Issue.objects.all()[0]
        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]))
        self.assertEqual(response.context['issues'].object_list[0].is_available, True)

        #change atribute is_available
        issue.is_available = False
        issue.save()

        response = self.client.get(reverse('issue.index', args=[issue.journal.pk]) + '?is_available=0')
        self.assertEqual(response.context['issues'].object_list[0].is_available, False)
        self.assertEqual(len(response.context['issues'].object_list), 1)

# class LoggedOutViewsTest(TestCase):

#     def test_page_index(self):
#         """
#         View: journal_index (Not Logged)

#         """
#         response = self.client.get('/')
#         self.assertEqual(response.status_code, 200)

#     def test_password_reset(self):
#         """
#         View: password_reset (Not Logged)

#         """

#         response = self.client.get('/accounts/password/reset/')
#         self.assertEqual(response.status_code, 200)

#     def test_account_register(self):
#         """
#         View: account_register (Not Logged)

#         """

#         response = self.client.get('/accounts/register/')
#         self.assertEqual(response.status_code, 200)

class ToolsTest(TestCase):
    def test_paginator_factory(self):
        """
        Function: scielomanager.tools.get_paginated
        """
        from scielomanager.tools import get_paginated

        items_list = [chr(i) for i in range(97, 123)]
        page_num = 1
        items_per_page = 5

        paginated = get_paginated(items_list, page_num, items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # When requiring a non-existing page, the last one is retrieved
        paginated = get_paginated(items_list, 10, items_per_page=items_per_page)
        self.assertEqual(paginated.number, paginated.paginator.num_pages)

        del(paginated)

        # Testing if page parameter is integer
        paginated = get_paginated(items_list, str(1), items_per_page=items_per_page)

        self.assertEqual(paginated.paginator.count, 26)
        self.assertEqual(paginated.paginator.num_pages, 6)
        self.assertTrue(hasattr(paginated, 'object_list'))
        self.assertEqual(len(paginated.object_list), 5)

        del(paginated)

        # Testing if page parameter is a "string"
        self.assertRaises(TypeError, get_paginated, items_list, 'foo', items_per_page=items_per_page)

# class JournalImportTest(TestCase):
#     import json
#     import os

#     fixtures = ['test_import_data']

#     json_parsed=json.loads(open('utils/test_journal.json','r').read())

#     #def setUp(self):
#         #import pdb; pdb.set_trace()

#     def test_get_collection(self):
#         """
#         Function: scielomanger.utils.get_collection
#         Testando recuperar dados da coleção que receberá o import
#         """

#         from scielomanager.utils.journalimport import JournalImport

#         ji = JournalImport()
#         collection = ji.get_collection('Brasil')
#         self.assertEqual(collection.id, 1)
#         self.assertEqual(collection.name, u'Brasil')
#         self.assertEqual(collection.url, u'http://www.scielo.br/')

#     #def test_charge_summary(self):
#         #from scielomanager.utils.journalimport import JournalImport

#         #ji = JournalImport()

#         #ji.run_import(self.json_parsed, 'Brasil')

#         #self.assertEqual(len(Institution.objects.all()),2)
#         #self.assertEqual(len(Journal.objects.all()),3)

