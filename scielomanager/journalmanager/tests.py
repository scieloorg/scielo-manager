#coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from scielomanager.journalmanager.models import Collection, UserProfile, Journal, Institution
from scielomanager.journalmanager import tests_assets

class LoggedInViewsTest(TestCase):

    """
    Set fixture
    """
    # fixtures = ['test_data']

    def setUp(self):
        """
        Creates an authenticated session using user from fixture
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

        self.__create_journal()

    def tearDown(self):
        self.__destroy_journal()

    def __create_journal(self):
        sample_journal = tests_assets.get_sample_journal()
        sample_journal.creator = self.user

        sample_institution = tests_assets.get_sample_institution()
        sample_institution.collection = self.collection
        sample_institution.save()

        sample_journal.institution = sample_institution
        sample_journal.save()
        sample_journal.collections = [self.collection,]

        sample_journal.save()

    def __destroy_journal(self):
        Journal.objects.get(title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xe3o Paulo)').delete()

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

