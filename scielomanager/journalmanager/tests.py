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

    def test_title_index(self):
        response = self.client.get('/journal/')
        self.assertEqual(response.status_code, 200)


class LoggedOutViewsTest(TestCase):
    pass

