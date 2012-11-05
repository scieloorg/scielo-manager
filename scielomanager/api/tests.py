# coding:utf-8
"""
`api` app tests

these tests are in a, maybe, wrong app for pragmatic purposes
of the app `api` not being part of the django installed apps.
"""
from django_webtest import WebTest

from journalmanager.tests import modelfactories


class JournalRestAPITest(WebTest):

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

    def test_api_v1_datamodel(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.get('/api/v1/journals/%s/' % journal.pk)

        expected_keys = [
            u'editor_address',
            u'copyrighter',
            u'editor_address_city',
            u'editor_address_state',
            u'creator',
            u'ctrl_vocabulary',
            u'national_code',
            u'frequency',
            u'url_journal',
            u'short_title',
            u'final_num',
            u'logo',
            u'publisher_country',
            u'publisher_name',
            u'eletronic_issn',
            u'issues',
            u'url_online_submission',
            u'init_vol',
            u'subject_descriptors',
            u'title',
            u'pub_status_history',
            u'id',
            u'final_year',
            u'editorial_standard',
            u'languages',
            u'scielo_issn',
            u'collections',
            u'index_coverage',
            u'secs_code',
            u'init_year',
            u'sections',
            u'is_indexed_aehci',
            u'use_license',
            u'other_titles',
            u'updated',
            u'editor_address_country',
            u'acronym',
            u'publisher_state',
            u'is_indexed_scie',
            u'sponsors',
            u'abstract_keyword_languages',
            u'editor_name',
            u'other_previous_title',
            u'study_areas',
            u'medline_code',
            u'is_trashed',
            u'init_num',
            u'publication_city',
            u'pub_level',
            u'is_indexed_ssci',
            u'missions',
            u'editor_email',
            u'created',
            u'medline_title',
            u'final_vol',
            u'cover',
            u'editor_phone2',
            u'editor_phone1',
            u'print_issn',
            u'editor_address_zip',
            u'contact',
            u'pub_status',
            u'pub_status_reason',
            u'title_iso',
            u'notes',
            u'resource_uri'
        ]

        self.assertEqual(response.json.keys(), expected_keys)


class CollectionRestAPITest(WebTest):

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

    def test_api_v1_datamodel(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v1/collections/%s/' % collection.pk)

        expected_keys = [
            u'city',
            u'fax',
            u'address_complement',
            u'address_number',
            u'acronym',
            u'country',
            u'zip_code',
            u'id',
            u'phone',
            u'state',
            u'name_slug',
            u'url',
            u'address',
            u'logo',
            u'resource_uri',
            u'email',
            u'name'
        ]

        self.assertEqual(response.json.keys(), expected_keys)


class IssuesRestAPITest(WebTest):

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

    def test_api_v1_datamodel(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v1/issues/%s/' % issue.pk)

        expected_keys = [
            u'is_press_release',
            u'ctrl_vocabulary',
            u'number',
            u'total_documents',
            u'label',
            u'id',
            u'publication_start_month',
            u'suppl_number',
            u'publication_end_month',
            u'editorial_standard',
            u'sections',
            u'updated',
            u'suppl_volume',
            u'journal',
            u'volume',
            u'is_trashed',
            u'is_marked_up',
            u'created',
            u'cover',
            u'publication_year',
            u'order',
            u'resource_uri'
        ]

        self.assertEqual(response.json.keys(), expected_keys)


class SectionsRestAPITest(WebTest):

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

    def test_api_v1_datamodel(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.get('/api/v1/sections/%s/' % section.pk)

        expected_keys = [
            u'updated',
            u'code',
            u'created',
            u'journal',
            u'titles',
            u'is_trashed',
            u'id',
            u'issues',
            u'resource_uri'
        ]

        self.assertEqual(response.json.keys(), expected_keys)
