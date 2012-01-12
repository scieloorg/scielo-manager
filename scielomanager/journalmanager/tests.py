#coding: utf-8
from django.test import TestCase
from django.test.client import Client
from django.contrib.auth.models import User
from scielomanager.journalmanager.models import Collection, UserProfile


class LoggedInViewsTest(TestCase):
    def setUp(self):
        """
        Creates an authenticated session
        """
        self.client = Client()
        user = User.objects.create_user('dummyuser', 'dummyuser@scielo.org', '123456')
        collection = Collection(name='scielobr', manager=user, url='http://www.scielo.br')

        user.save()
        collection.save()

        user_profile = UserProfile(user=user, collection=collection)
        user_profile.save()

        self.client.login(username='dummyuser', password='123456')

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

class LoggedOutViewsTest(TestCase):
    pass

