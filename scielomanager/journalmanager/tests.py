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
