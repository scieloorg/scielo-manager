#coding: utf-8

import json
import datetime
from django_webtest import WebTest
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from editorialmanager.tests import modelfactories as editorial_modelfactories
from api.resources_v2 import (
    JournalResource,
    IssueResource,
    )


def _make_auth_environ(username, token):
    return {'HTTP_AUTHORIZATION': 'ApiKey {0}:{1}'.format(username, token)}


def _makePermission(perm, model, app_label='journalmanager'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)

    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


def _makeUseLicense():
    from journalmanager.models import UseLicense
    ul = UseLicense(license_code='TEST')
    ul.save()


class JournalRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)
        _makeUseLicense()

    def test_journal_index(self):
        response = self.app.get('/api/v2/journals/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_journal_filters(self):
        resource_filters = JournalResource().Meta
        mandatory_filters = ['is_trashed']
        for fltr in mandatory_filters:
            self.assertTrue(fltr in resource_filters.filtering)

    def test_journal_getone(self):
        col = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.content)

    def test_post_data_index(self):
        response = self.app.post('/api/v2/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_index(self):
        response = self.app.put('/api/v2/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_index(self):
        response = self.app.delete('/api/v2/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_post_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.post('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.put('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.delete('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthorized_users(self):
        response = self.app.get('/api/v2/journals/',
            status=401)

        self.assertEqual(response.status_code, 401)

    def test_list_all_journals_by_collection(self):
        collection = modelfactories.CollectionFactory()

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()
        journal1.join(collection, self.user)
        journal2.join(collection, self.user)

        response = self.app.get('/api/v2/journals/?collection=%s' % collection.name,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_datamodel(self):
        col = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'editor_address',
            u'copyrighter',
            u'editor_address_city',
            u'editor_address_state',
            u'creator',
            u'ctrl_vocabulary',
            u'national_code',
            u'updated',
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
            u'resource_uri',
            u'previous_ahead_documents',
            u'current_ahead_documents',
            u'twitter_user',
            u'previous_title',
            u'succeeding_title',
            u'subject_categories'
        ]

        json_keys = set(response.json.keys())
        expected_keys = set(expected_keys)

        # looks for unexpected fields
        self.assertFalse(json_keys.difference(expected_keys))

        # make sure all expected fields are present
        for key in expected_keys:
            self.assertEqual(True, key in json_keys)

    def test_api_collections_data(self):
        col1 = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()

        journal.join(col1, self.user)
        journal.join(col2, self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ)

        expected_collections = [col1.name, col2.name]

        self.assertEqual(response.json['collections'], expected_collections)

    def test_filter_by_pubstatus(self):
        col = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.change_status(col, 'current', 'testing', self.user)

        journal2 = modelfactories.JournalFactory.create()
        journal2.join(col, self.user)
        journal2.change_status(col, 'deceased', 'testing', self.user)

        response = self.app.get('/api/v2/journals/?pubstatus=current',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_filter_by_pubstatus_many_values(self):
        col = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.change_status(col, 'current', 'testing', self.user)

        journal2 = modelfactories.JournalFactory.create()
        journal2.join(col, self.user)
        journal2.change_status(col, 'deceased', 'testing', self.user)

        response = self.app.get('/api/v2/journals/?pubstatus=current&pubstatus=deceased',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 2)

    def test_filter_by_pubstatus_many_values_filtering_by_collection(self):
        col = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.change_status(col, 'current', 'testing', self.user)

        journal2 = modelfactories.JournalFactory.create()
        journal2.join(col2, self.user)
        journal2.change_status(col2, 'deceased', 'testing', self.user)

        response = self.app.get('/api/v2/journals/?pubstatus=current&pubstatus=deceased&collection=%s' % col.name,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_filter_print_issn(self):
        col = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create(print_issn='1234-1234')
        journal.join(col, self.user)
        journal2 = modelfactories.JournalFactory.create(print_issn='4321-4321')
        journal2.join(col, self.user)

        response = self.app.get('/api/v2/journals/?print_issn=1234-1234',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)
        self.assertEqual(json.loads(response.content)['objects'][0]['print_issn'], '1234-1234')

    def test_filter_eletronic_issn(self):
        col = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create(eletronic_issn='1234-1234')
        journal.join(col, self.user)
        journal2 = modelfactories.JournalFactory.create(eletronic_issn='4321-4321')
        journal2.join(col, self.user)
        response = self.app.get('/api/v2/journals/?eletronic_issn=1234-1234',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)
        self.assertEqual(json.loads(response.content)['objects'][0]['eletronic_issn'], '1234-1234')

    def test_succeding_title(self):
        col = modelfactories.CollectionFactory()

        col.add_user(self.user)

        journal1 = modelfactories.JournalFactory.create(title='Previous Title')
        journal1.join(col, self.user)

        journal2 = modelfactories.JournalFactory.create(title='Succeeding Title', previous_title=journal1)
        journal2.join(col, self.user)

        response = self.app.get(
            '/api/v2/journals/%s/' % journal1.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(
            response['succeeding_title'],
            '/api/v2/journals/%s/' % journal2.pk)

    def test_without_succeding_title(self):
        col = modelfactories.CollectionFactory()

        col.add_user(self.user)

        journal1 = modelfactories.JournalFactory.create(title='Previous Title')
        journal1.join(col, self.user)

        response = self.app.get(
            '/api/v2/journals/%s/' % journal1.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(
            response['succeeding_title'], None)

    def test_api_pub_status_data(self):
        col = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(response['pub_status'], {col.name:
                journal.membership_info(collection=col, attribute='status')})

    def test_api_pub_status_data_with_multiple_collection(self):
        col1 = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col1, self.user)
        journal.join(col2, self.user)

        #Change status of journal on collection 1
        journal.change_status(col1, 'current',
            'The journal passed on SciELO evaluation', self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(response['pub_status'],
            {col.name:journal.membership_info(collection=col, attribute='status')
            for col in journal.collections.all()})

    def test_api_pub_status_history_data(self):
        col1 = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col1, self.user)
        journal.join(col2, self.user)

        response = self.app.get('/api/v2/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ).json

        expected_history = []

        for history in journal.statuses.order_by('-since').all():
            expected_history.append({'date': history.since.strftime('%Y-%m-%dT%H:%M:%S.%f'), 'status': history.status})

        self.assertEqual(response['pub_status_history'],
            expected_history)


class CollectionRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_index(self):
        modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v2/collections/',
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_post_data(self):
        response = self.app.post('/api/v2/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        response = self.app.put('/api/v2/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        response = self.app.delete('/api/v2/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v2/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.content)

    def test_post_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.post('/api/v2/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.put('/api/v2/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.delete('/api/v2/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_api_v2_datamodel(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v2/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ)

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

    def test_access_denied_for_unathorized_users(self):
        modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v2/collections/', status=401)
        self.assertEqual(response.status_code, 401)


class IssuesRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)

    def test_issue_index(self):
        modelfactories.IssueFactory.create()
        response = self.app.get('/api/v2/issues/', extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_issue_filters(self):
        resource_filters = IssueResource().Meta
        mandatory_filters = ['journal', 'is_marked_up']
        for fltr in mandatory_filters:
            self.assertTrue(fltr in resource_filters.filtering)

    def test_post_data(self):
        modelfactories.IssueFactory.create()
        response = self.app.post('/api/v2/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        modelfactories.IssueFactory.create()
        response = self.app.put('/api/v2/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        modelfactories.IssueFactory.create()
        response = self.app.delete('/api/v2/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_issue_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('number' in response.content)

    def test_post_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.post('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.put('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.delete('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_api_v2_datamodel(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        expected_keys = [
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
            u'spe_text',
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
            u'resource_uri',
            u'thematic_titles',
            u'suppl_text',
            u'type',
            u'use_license'
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_access_denied_for_unauthenticated_users(self):
        modelfactories.IssueFactory.create()
        response = self.app.get('/api/v2/issues/', status=401)
        self.assertEqual(response.status_code, 401)

    def test_thematic_titles_must_be_dict(self):
        issue = modelfactories.IssueFactory.create()
        modelfactories.IssueTitleFactory.create(issue=issue)

        response = self.app.get('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        content = json.loads(response.content)
        self.assertEqual(content.get('thematic_titles', None), {'pt': 'Bla'})

    def test_thematic_titles_must_be_dict_even_if_empty(self):
        issue = modelfactories.IssueFactory.create()

        response = self.app.get('/api/v2/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        content = json.loads(response.content)
        self.assertIsInstance(content.get('thematic_titles', None), dict)

    def test_list_all_by_collection(self):
        collection = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(collection, self.user)
        modelfactories.IssueFactory.create(journal=journal)
        collection_name = collection.name

        response = self.app.get('/api/v2/issues/?collection=%s' % collection_name, extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_suppl_number_filter_without_volume(self):
        """
        test that create a supplement issue, with ``number``, ``suppl_text`` and empty ``volume`` fields.
        then request the API, with filter ``suppl_number`` and should return the previous issue, with the correct
        ``suppl_number`` (= ``suppl_text``) and ``suppl_volume`` (empty).
        """
        issue = modelfactories.IssueFactory.create(number='999', suppl_text='2', volume='', type='supplement')
        response = self.app.get('/api/v2/issues/?suppl_number=%s' % issue.number, extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        content = content['objects'][0]
        self.assertEqual(content.get('suppl_number', None), issue.suppl_text)
        self.assertEqual(content.get('suppl_volume', None), '')
        self.assertEqual(content.get('number', None), issue.number)
        self.assertEqual(content.get('volume', None), issue.volume)

    def test_suppl_number_filter_with_volume(self):
        """
        test that create a supplement issue, with ``number``, ``suppl_text`` and *NON* empty ``volume`` fields.
        then request the API, with filter ``suppl_number`` and should return the previous issue, with the correct
        ``suppl_number`` (= ``suppl_text``) and ``suppl_volume`` (= ``suppl_text``).
        """
        issue = modelfactories.IssueFactory.create(number='999', suppl_text='2', volume='1', type='supplement')
        response = self.app.get('/api/v2/issues/?suppl_number=%s' % issue.number, extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(content['objects']), 1)
        content = content['objects'][0]
        self.assertEqual(content.get('suppl_number', None), issue.suppl_text)
        self.assertEqual(content.get('suppl_volume', None), issue.suppl_text)
        self.assertEqual(content.get('number', None), issue.number)
        self.assertEqual(content.get('volume', None), issue.volume)

    def test_suppl_volume_filter_without_number(self):
        """
        test that create a supplement issue, with ``volume``, ``suppl_text`` and empty ``number`` fields.
        then request the API, with filter ``suppl_number`` and should return the previous issue, with the correct
        ``suppl_volume`` (= ``suppl_text``) and ``suppl_number`` (empty).
        """
        issue = modelfactories.IssueFactory.create(volume='999', suppl_text='2', number='', type='supplement')
        response = self.app.get('/api/v2/issues/?suppl_volume=%s' % issue.volume, extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(content['objects']), 1)
        content = content['objects'][0]
        self.assertEqual(content.get('suppl_volume', None), issue.suppl_text)
        self.assertEqual(content.get('suppl_number', None), '')
        self.assertEqual(content.get('number', None), issue.number)
        self.assertEqual(content.get('volume', None), issue.volume)

    def test_suppl_volume_filter_with_number(self):
        """
        test that create a supplement issue, with ``volume``, ``suppl_text`` and *NON* empty ``number`` fields.
        then request the API, with filter ``suppl_volume`` and should return an empty list.
        Because, the ``suppl_volume`` filter will apply always with ``number=''`` condition.
        """
        issue = modelfactories.IssueFactory.create(number='999', suppl_text='2', volume='777', type='supplement')
        response = self.app.get('/api/v2/issues/?suppl_volume=%s' % issue.volume, extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 0)

    def test_if_the_returned_list_are_from_correct_collection(self):
        """
        test if the API is considering the colletion on filter
        """
        collection1 = modelfactories.CollectionFactory()
        collection2 = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(collection1, self.user)

        modelfactories.IssueFactory.create(journal=journal)

        #test if return one issue from collecion1
        response1 = self.app.get('/api/v2/issues/?collection=%s&print_issn=%s' % (collection1.name, journal.print_issn) , extra_environ=self.extra_environ)
        content1 = json.loads(response1.content)

        self.assertEqual(response1.status_code, 200)
        self.assertTrue('objects' in response1.content)

        self.assertEqual(len(content1['objects']), 1)

        #test if return nothing issue from collecion2
        response2 = self.app.get('/api/v2/issues/?collection=%s&print_issn=%s' % (collection2.name, journal.print_issn) , extra_environ=self.extra_environ)
        content2 = json.loads(response2.content)

        self.assertEqual(response2.status_code, 200)
        self.assertTrue('objects' in response2.content)

        self.assertEqual(len(content2['objects']), 0)


    def test_number_of_itens_when_change_filters(self):
        """
        test if number of itens changes when change params
        """
        collection = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(collection, self.user)

        modelfactories.IssueFactory.create(journal=journal)
        modelfactories.IssueFactory.create(journal=journal, number='999', type='supplement',)
        modelfactories.IssueFactory.create(journal=journal, number='999', type='supplement',)
        modelfactories.IssueFactory.create(journal=journal, number='999', type='supplement',)
        modelfactories.IssueFactory.create(journal=journal, number='999', volume='2', type='supplement', )
        modelfactories.IssueFactory.create(journal=journal, number='999', volume='3', type='supplement', )
        modelfactories.IssueFactory.create(journal=journal, number='999', volume='5', type='supplement', )
        modelfactories.IssueFactory.create(journal=journal, number='', volume='2', type='supplement', )
        modelfactories.IssueFactory.create(journal=journal, number='', volume='2', type='supplement', )
        modelfactories.IssueFactory.create(journal=journal, number='', volume='2', type='supplement', )

        #test with param number
        response = self.app.get('/api/v2/issues/?suppl_number=999', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 6)

        #test with param number and suppl_volume
        response = self.app.get('/api/v2/issues/?suppl_volume=2', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 3)

        #test with param number and suppl_number and suppl_volume, must return empty list
        response = self.app.get('/api/v2/issues/?suppl_volume=2&suppl_number=999', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 0)

        #test with param number and suppl_number and suppl_volume, change sequence of params
        response = self.app.get('/api/v2/issues/?suppl_number=999&suppl_volume=2', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 0)


class PressReleaseRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_post_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.post('/api/v2/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.put('/api/v2/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.delete('/api/v2/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v2/pressreleases/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_pressrelease_index(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v2/pressreleases/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_datamodel(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v2/pressreleases/%s/' % pr.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'articles',
            u'id',
            u'issue_uri',
            u'resource_uri',
            u'translations',
            u'issue_meta',
            u'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v2_datamodel(self):
        pr_trans = modelfactories.PressReleaseTranslationFactory.create()
        response = self.app.get('/api/v2/pressreleases/%s/' % pr_trans.press_release.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'content',
            u'id',
            u'language',
            u'resource_uri',
            u'title',
        ]

        self.assertEqual(
            sorted(response.json['translations'][0].keys()),
            sorted(expected_keys)
        )

    def test_issue_meta_api_v2_datamodel(self):
        pr_trans = modelfactories.PressReleaseTranslationFactory.create()
        response = self.app.get('/api/v2/pressreleases/%s/' % pr_trans.press_release.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'short_title',
            'volume',
            'number',
            'suppl_volume',
            'suppl_number',
            'publication_start_month',
            'publication_end_month',
            'publication_city',
            'publication_year',
            'scielo_pid',
        ]

        self.assertEqual(
            sorted(response.json['issue_meta'].keys()),
            sorted(expected_keys)
        )

    def test_article_filter(self):
        pr_articles = []
        for pr in range(5):
            pr_articles.append(modelfactories.PressReleaseArticleFactory.create())

        response = self.app.get(
            '/api/v2/pressreleases/?article_pid=%s' % pr_articles[0].article_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())

        response = self.app.get(
            '/api/v2/pressreleases/?journal_pid=%s' % prs[0].issue.journal.scielo_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter_for_nonexisting_values_skips_filtering(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())
        response = self.app.get(
            '/api/v2/pressreleases/?journal_pid=5',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)

    def test_article_filter_for_nonexisting_values_skips_filtering(self):
        pr_articles = []
        for pr in range(5):
            pr_articles.append(modelfactories.PressReleaseArticleFactory.create())

        response = self.app.get(
            '/api/v2/pressreleases/?article_pid=EMPTY',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)

    def test_issue_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())

        response = self.app.get(
            '/api/v2/pressreleases/?issue_pid=%s' % prs[0].issue.scielo_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)


class AheadPressReleaseRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_post_data(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.post('/api/v2/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.put('/api/v2/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.delete('/api/v2/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v2/apressreleases/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_pressrelease_index(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v2/apressreleases/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_datamodel(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v2/apressreleases/%s/' % pr.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'articles',
            u'id',
            u'journal_uri',
            u'resource_uri',
            u'translations',
            u'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v2_datamodel(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        pr_trans = modelfactories.PressReleaseTranslationFactory.create(press_release=pr)
        response = self.app.get('/api/v2/apressreleases/%s/' % pr_trans.press_release.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'content',
            u'id',
            u'language',
            u'resource_uri',
            u'title',
        ]

        self.assertEqual(
            sorted(response.json['translations'][0].keys()),
            sorted(expected_keys)
        )

    def test_article_filter(self):
        prelease = modelfactories.AheadPressReleaseFactory.create()
        pr_articles = []
        for pr in range(5):
            pr_articles.append(modelfactories.PressReleaseArticleFactory.create(press_release=prelease))

        response = self.app.get(
            '/api/v2/apressreleases/?article_pid=%s' % pr_articles[0].article_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.AheadPressReleaseFactory.create())

        response = self.app.get(
            '/api/v2/apressreleases/?journal_pid=%s' % prs[0].journal.scielo_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter_for_nonexisting_values_skips_filtering(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.AheadPressReleaseFactory.create())
        response = self.app.get(
            '/api/v2/apressreleases/?journal_pid=5',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)

    def test_article_filter_for_nonexisting_values_skips_filtering(self):
        prelease = modelfactories.AheadPressReleaseFactory.create()
        pr_articles = []
        for pr in range(5):
            pr_articles.append(modelfactories.PressReleaseArticleFactory.create(press_release=prelease))

        response = self.app.get(
            '/api/v2/apressreleases/?article_pid=EMPTY',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)


class EditorialBoardRestAPITest(WebTest):

    def setUp(self):
        self.api_path = '/api/v2/editorialboard/'
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)
        # setup collection
        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)
        # journal
        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)
        #set the user as editor of the journal
        self.journal.editor = self.user
        self.journal.save()
        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

    def tearDown(self):
        pass

    def test_post_data(self):
        """ method POST not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        """ method PUT not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        """ method DELETE not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get(self.api_path, status=401)
        self.assertEqual(response.status_code, 401)

    def test_editorialboard_index(self):
        # with
        board = editorial_modelfactories.EditorialBoardFactory.create(issue=self.issue)
        # when
        response = self.app.get(self.api_path, extra_environ=self.extra_environ)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_data_editorialboard(self):
        # with
        board = editorial_modelfactories.EditorialBoardFactory.create(issue=self.issue)
        target_url = "%s%s/" % (self.api_path, board.pk)
        # when
        response = self.app.get(target_url, extra_environ=self.extra_environ)
        # then
        expected_keys = [
            u'id',
            u'issue',
            u'resource_uri',
        ]
        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class RoleTypeRestAPITest(WebTest):

    def setUp(self):
        self.api_path = '/api/v2/roletype/'
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)

    def tearDown(self):
        pass

    def test_post_data(self):
        """ method POST not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        """ method PUT not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        """ method DELETE not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get(self.api_path, status=401)
        self.assertEqual(response.status_code, 401)

    def test_roletype_index(self):
        # with
        role = editorial_modelfactories.RoleTypeFactory.create()
        # when
        response = self.app.get(self.api_path, extra_environ=self.extra_environ)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_data_roletype(self):
        # with
        role = editorial_modelfactories.RoleTypeFactory.create()
        target_url = "%s%s/" % (self.api_path, role.pk)
        # when
        response = self.app.get(target_url, extra_environ=self.extra_environ)
        # then
        expected_keys = [
            u'id',
            u'name',
            u'resource_uri',
        ]
        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class RoleTypeTranslationRestAPITest(WebTest):

    def setUp(self):
        self.api_path = '/api/v2/roletypetranslation/'
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)

    def tearDown(self):
        pass

    def test_post_data(self):
        """ method POST not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        """ method PUT not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        """ method DELETE not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get(self.api_path, status=401)
        self.assertEqual(response.status_code, 401)

    def test_roletypetranslation_index(self):
        # with
        role_i18n = editorial_modelfactories.RoleTypeTranslationFactory.create()
        # when
        response = self.app.get(self.api_path, extra_environ=self.extra_environ)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_data_roletypetranslation(self):
        # with
        role_i18n = editorial_modelfactories.RoleTypeTranslationFactory.create()
        target_url = "%s%s/" % (self.api_path, role_i18n.pk)
        # when
        response = self.app.get(target_url, extra_environ=self.extra_environ)
        # then
        expected_keys = [
            u'id',
            u'language',
            u'name',
            u'resource_uri',
            u'role',
        ]
        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class EditorialMemberRestAPITest(WebTest):

    def setUp(self):
        self.api_path = '/api/v2/editorialmember/'
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)
        # setup collection
        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)
        # journal
        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)
        #set the user as editor of the journal
        self.journal.editor = self.user
        self.journal.save()
        # create an issue
        self.issue = modelfactories.IssueFactory.create()
        self.issue.journal = self.journal
        self.journal.save()
        self.issue.save()

    def tearDown(self):
        pass

    def test_post_data(self):
        """ method POST not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        """ method PUT not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        """ method DELETE not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get(self.api_path, status=401)
        self.assertEqual(response.status_code, 401)

    def test_editorialmember_index(self):
        # with
        member = editorial_modelfactories.EditorialMemberFactory.create()
        # when
        response = self.app.get(self.api_path, extra_environ=self.extra_environ)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_data_editorialmember(self):
        # with
        board = editorial_modelfactories.EditorialBoardFactory.create(issue=self.issue)
        role = editorial_modelfactories.RoleTypeFactory.create()
        member = editorial_modelfactories.EditorialMemberFactory.create(board=board, role=role, order=1)
        target_url = "%s%s/" % (self.api_path, member.pk)
        # when
        response = self.app.get(target_url, extra_environ=self.extra_environ)
        # then
        expected_keys = [
            u'board',
            u'city',
            u'country',
            u'email',
            u'first_name',
            u'id',
            u'institution',
            u'last_name',
            u'link_cv',
            u'orcid',
            u'order',
            u'research_id',
            u'resource_uri',
            u'role',
            u'state'
        ]
        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class LanguageRestAPITest(WebTest):

    def setUp(self):
        self.api_path = '/api/v2/language/'
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)

    def tearDown(self):
        pass

    def test_post_data(self):
        """ method POST not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        """ method PUT not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        """ method DELETE not allowed """
        response = self.app.delete(self.api_path, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get(self.api_path, status=401)
        self.assertEqual(response.status_code, 401)

    def test_language_index(self):
        # with
        language = modelfactories.LanguageFactory.create()
        # when
        response = self.app.get(self.api_path, extra_environ=self.extra_environ)
        # then
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v2_data_language(self):
        # with
        language = modelfactories.LanguageFactory.create()
        target_url = "%s%s/" % (self.api_path, language.pk)
        # when
        response = self.app.get(target_url, extra_environ=self.extra_environ)
        # then
        expected_keys = [
            u'id',
            u'iso_code',
            u'name',
            u'resource_uri',
        ]
        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))
