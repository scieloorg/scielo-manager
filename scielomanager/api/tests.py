# coding:utf-8
"""
`api` app tests

these tests are in a, maybe, wrong app for pragmatic purposes
of the app `api` not being part of the django installed apps.
"""
from django.test import TestCase

from journalmanager.tests import modelfactories


class JournalRestAPITest(TestCase):

    def test_journal_index(self):
        response = self.client.get('/api/v1/journals/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_journal_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.client.get('/api/v1/journals/%s/' % journal.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.content)

    def test_post_data_index(self):
        response = self.client.post('/api/v1/journals/')
        self.assertEqual(response.status_code, 405)

    def test_put_data_index(self):
        response = self.client.put('/api/v1/journals/')
        self.assertEqual(response.status_code, 405)

    def test_del_data_index(self):
        response = self.client.delete('/api/v1/journals/')
        self.assertEqual(response.status_code, 405)

    def test_post_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.client.post('/api/v1/journals/%s/' % journal.pk)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.client.put('/api/v1/journals/%s/' % journal.pk)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.client.delete('/api/v1/journals/%s/' % journal.pk)
        self.assertEqual(response.status_code, 405)

    def test_list_all_by_collection(self):
        journal = modelfactories.JournalFactory.create()
        collection_name = journal.collection.name
        response = self.client.get('/api/v1/journals/?collection=%s' % collection_name)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)


class CollectionRestAPITest(TestCase):

    def test_index(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.client.get('/api/v1/collections/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_post_data(self):
        response = self.client.post('/api/v1/collections/')
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        response = self.client.put('/api/v1/collections/')
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        response = self.client.delete('/api/v1/collections/')
        self.assertEqual(response.status_code, 405)

    def test_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.client.get('/api/v1/collections/%s/' % collection.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.content)

    def test_post_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.client.post('/api/v1/collections/%s/' % collection.pk)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.client.put('/api/v1/collections/%s/' % collection.pk)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.client.delete('/api/v1/collections/%s/' % collection.pk)
        self.assertEqual(response.status_code, 405)


class IssuesRestAPITest(TestCase):

    def test_issue_index(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.get('/api/v1/issues/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_post_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.post('/api/v1/issues/')
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.put('/api/v1/issues/')
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.delete('/api/v1/issues/')
        self.assertEqual(response.status_code, 405)

    def test_issue_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.get('/api/v1/issues/%s/' % issue.pk)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('number' in response.content)

    def test_post_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.post('/api/v1/issues/%s/' % issue.pk)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.put('/api/v1/issues/%s/' % issue.pk)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.client.delete('/api/v1/issues/%s/' % issue.pk)
        self.assertEqual(response.status_code, 405)


class SectionsRestAPITest(TestCase):

    def test_section_index(self):
        section = modelfactories.SectionFactory.create()
        response = self.client.get('/api/v1/sections/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_post_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.client.post('/api/v1/sections/')
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.client.put('/api/v1/sections/')
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.client.delete('/api/v1/sections/')
        self.assertEqual(response.status_code, 405)
