#coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from scielomanager.journalmanager.models import Collection, UserProfile

class LoggedInViewsTest(TestCase):

    """
    Set fixture
    """
    fixtures = ['test_data']

    def setUp(self):
        """
        Creates an authenticated session using user from fixture
        """

        self.client.login(username='admin', password='123')

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
        self.assertEqual(u'Periódico SciELO', unicode(response.context['journals'].object_list[0].title))
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
        self.assertEqual(u'SciELO Publisher', unicode(response.context['institutions'][0].name))
        self.assertTrue(1, len(response.context['institutions']))


class LoggedOutViewsTest(TestCase):

    def test_page_index(self):
        """
        View: journal_index (Not Logged)

        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    # def test_password_reset(self):
    #     """
    #     View: password_reset (Not Logged)

    #     """

    #     response = self.client.get('/accounts/password/reset/')
    #     self.assertEqual(response.status_code, 200)

    # def test_account_register(self):
    #     """
    #     View: account_register (Not Logged)

    #     """

    #     response = self.client.get('/accounts/register/')
    #     self.assertEqual(response.status_code, 200)

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