# coding:utf-8
"""
`api` app tests

these tests are in a, maybe, wrong app for pragmatic purposes
of the app `api` not being part of the django installed apps.
"""
import json
import datetime
from django_webtest import WebTest
from django_factory_boy import auth

from journalmanager.tests import modelfactories

from api.resources_v1 import (
    IssueResource,
    SectionResource,
    JournalResource,
    )

from scielomanager.utils.modelmanagers.helpers import (
    _makeUserRequestContext,
    _patch_userrequestcontextfinder_settings_setup,
    _patch_userrequestcontextfinder_settings_teardown
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
        response = self.app.get('/api/v1/journals/',
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

        response = self.app.get('/api/v1/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('title' in response.content)

    def test_post_data_index(self):
        response = self.app.post('/api/v1/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_index(self):
        response = self.app.put('/api/v1/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_index(self):
        response = self.app.delete('/api/v1/journals/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_post_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.post('/api/v1/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.put('/api/v1/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        journal = modelfactories.JournalFactory.create()
        response = self.app.delete('/api/v1/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_list_all_by_collection(self):
        collection = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(collection, self.user)
        collection_name = collection.name
        response = self.app.get('/api/v1/journals/?collection=%s' % collection_name,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_datamodel(self):
        col = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)

        response = self.app.get('/api/v1/journals/%s/' % journal.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'editor_address',
            'copyrighter',
            'editor_address_city',
            'editor_address_state',
            'creator',
            'ctrl_vocabulary',
            'national_code',
            'updated',
            'frequency',
            'url_journal',
            'short_title',
            'final_num',
            'logo',
            'publisher_country',
            'publisher_name',
            'eletronic_issn',
            'issues',
            'url_online_submission',
            'init_vol',
            'subject_descriptors',
            'title',
            'pub_status_history',
            'id',
            'final_year',
            'editorial_standard',
            'languages',
            'scielo_issn',
            'collections',
            'index_coverage',
            'secs_code',
            'init_year',
            'sections',
            'is_indexed_aehci',
            'use_license',
            'other_titles',
            'editor_address_country',
            'acronym',
            'publisher_state',
            'is_indexed_scie',
            'sponsors',
            'abstract_keyword_languages',
            'editor_name',
            'other_previous_title',
            'study_areas',
            'subject_categories',
            'medline_code',
            'is_trashed',
            'init_num',
            'publication_city',
            'pub_level',
            'is_indexed_ssci',
            'missions',
            'editor_email',
            'created',
            'medline_title',
            'final_vol',
            'cover',
            'editor_phone2',
            'editor_phone1',
            'print_issn',
            'editor_address_zip',
            'contact',
            'pub_status',
            'pub_status_reason',
            'title_iso',
            'notes',
            'resource_uri',
            'previous_ahead_documents',
            'current_ahead_documents',
            'twitter_user',
            'previous_title',
            'succeeding_title',
        ]

        json_keys = set(response.json.keys())
        expected_keys = set(expected_keys)

        # looks for unexpected fields
        self.assertFalse(json_keys.difference(expected_keys))

        # make sure all expected fields are present
        for key in expected_keys:
            self.assertEqual(True, key in json_keys)

    def test_access_denied_for_unauthorized_users(self):
        response = self.app.get('/api/v1/journals/',
            status=401)

        self.assertEqual(response.status_code, 401)

    def test_filter_by_pubstatus(self):
        col = modelfactories.CollectionFactory()

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.change_status(col, 'current', 'testing', self.user)

        journal2 = modelfactories.JournalFactory.create()
        journal2.join(col, self.user)
        journal2.change_status(col, 'deceased', 'testing', self.user)

        response = self.app.get('/api/v1/journals/?pubstatus=current',
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

        response = self.app.get('/api/v1/journals/?pubstatus=current&pubstatus=deceased',
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

        response = self.app.get('/api/v1/journals/?pubstatus=current&pubstatus=deceased&collection=%s' % col.name,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_filter_print_issn(self):
        col = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create(print_issn='1234-1234')
        journal.join(col, self.user)
        journal2 = modelfactories.JournalFactory.create(print_issn='4321-4321')
        journal2.join(col, self.user)
        response = self.app.get('/api/v1/journals/?print_issn=1234-1234',
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
        response = self.app.get('/api/v1/journals/?eletronic_issn=1234-1234',
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
            '/api/v1/journals/%s/' % journal1.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(
            response['succeeding_title'],
            '/api/v1/journals/%s/' % journal2.pk)

    def test_without_succeding_title(self):
        col = modelfactories.CollectionFactory()

        col.add_user(self.user)

        journal1 = modelfactories.JournalFactory.create(title='Previous Title')
        journal1.join(col, self.user)

        response = self.app.get(
            '/api/v1/journals/%s/' % journal1.pk,
            extra_environ=self.extra_environ).json

        self.assertEqual(
            response['succeeding_title'], None)

    def test_dehydrate_pub_status_with_one_collections(self):
        col = modelfactories.CollectionFactory()

        col.add_user(self.user)

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)

        response = self.app.get('/api/v1/journals/',
                                extra_environ=self.extra_environ).json

        self.assertEqual(response['objects'][0]['pub_status'], 'inprogress')

    def test_dehydrate_pub_status_with_multiple_collections(self):
        col = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        col.add_user(self.user)
        col2.add_user(self.user)

        col.make_default_to_user(self.user)

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.join(col2, self.user, )

        journal.change_status(col, 'current', 'yeah', self.user)

        response = self.app.get('/api/v1/journals/?collection=%s' % col.name_slug,
                                extra_environ=self.extra_environ).json

        self.assertEqual(response['objects'][0]['pub_status'], 'current')

    def test_dehydrate_pub_status_with_multiple_collections_without_collection_param(self):
        col = modelfactories.CollectionFactory()
        col2 = modelfactories.CollectionFactory()

        col.add_user(self.user)
        col2.add_user(self.user)

        col.make_default_to_user(self.user)

        journal = modelfactories.JournalFactory.create()
        journal.join(col, self.user)
        journal.join(col2, self.user, )

        journal.change_status(col, 'current', 'yeah', self.user)

        response = self.app.get('/api/v1/journals/',
                                extra_environ=self.extra_environ, status=400)
        self.assertEqual(response.status_code, 400)


class CollectionRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_index(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v1/collections/',
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_post_data(self):
        response = self.app.post('/api/v1/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        response = self.app.put('/api/v1/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        response = self.app.delete('/api/v1/collections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v1/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('name' in response.content)

    def test_post_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.post('/api/v1/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.put('/api/v1/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.delete('/api/v1/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_api_v1_datamodel(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v1/collections/%s/' % collection.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'city',
            'fax',
            'address_complement',
            'address_number',
            'acronym',
            'country',
            'zip_code',
            'id',
            'phone',
            'state',
            'name_slug',
            'url',
            'address',
            'logo',
            'resource_uri',
            'email',
            'name'
        ]

        self.assertEqual(list(response.json.keys()), expected_keys)

    def test_access_denied_for_unathorized_users(self):
        collection = modelfactories.CollectionFactory.create()
        response = self.app.get('/api/v1/collections/', status=401)
        self.assertEqual(response.status_code, 401)


class IssuesRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username, self.user.api_key.key)

    def test_issue_index(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v1/issues/', extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_issue_filters(self):
        resource_filters = IssueResource().Meta
        mandatory_filters = ['journal', 'is_marked_up']
        for fltr in mandatory_filters:
            self.assertTrue(fltr in resource_filters.filtering)

    def test_post_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.post('/api/v1/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.put('/api/v1/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.delete('/api/v1/issues/', extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_issue_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('number' in response.content)

    def test_post_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.post('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.put('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data_getone(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.delete('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_api_v1_datamodel(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        expected_keys = [
            'is_press_release',
            'ctrl_vocabulary',
            'number',
            'total_documents',
            'label',
            'id',
            'publication_start_month',
            'suppl_number',
            'publication_end_month',
            'editorial_standard',
            'sections',
            'spe_text',
            'updated',
            'suppl_volume',
            'journal',
            'volume',
            'is_trashed',
            'is_marked_up',
            'created',
            'cover',
            'publication_year',
            'order',
            'resource_uri',
            'thematic_titles',
            'suppl_text',
            'type',
            'use_license'
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_access_denied_for_unauthenticated_users(self):
        issue = modelfactories.IssueFactory.create()
        response = self.app.get('/api/v1/issues/', status=401)
        self.assertEqual(response.status_code, 401)

    def test_thematic_titles_must_be_dict(self):
        issue = modelfactories.IssueFactory.create()
        issue_title = modelfactories.IssueTitleFactory.create(issue=issue)

        response = self.app.get('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        content = json.loads(response.content)
        self.assertEqual(content.get('thematic_titles', None), {'pt': 'Bla'})

    def test_thematic_titles_must_be_dict_even_if_empty(self):
        issue = modelfactories.IssueFactory.create()

        response = self.app.get('/api/v1/issues/%s/' % issue.pk, extra_environ=self.extra_environ)

        content = json.loads(response.content)
        self.assertIsInstance(content.get('thematic_titles', None), dict)

    def test_list_all_by_collection(self):
        collection = modelfactories.CollectionFactory()
        journal = modelfactories.JournalFactory.create()
        journal.join(collection, self.user)
        issue = modelfactories.IssueFactory.create(journal=journal)
        collection_name = collection.name

        response = self.app.get('/api/v1/issues/?collection=%s' % collection_name, extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_suppl_number_filter_without_volume(self):
        """
        test that create a supplement issue, with ``number``, ``suppl_text`` and empty ``volume`` fields.
        then request the API, with filter ``suppl_number`` and should return the previous issue, with the correct
        ``suppl_number`` (= ``suppl_text``) and ``suppl_volume`` (empty).
        """
        issue = modelfactories.IssueFactory.create(number='999', suppl_text='2', volume='', type='supplement')
        response = self.app.get('/api/v1/issues/?suppl_number=%s' % issue.number, extra_environ=self.extra_environ)
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
        response = self.app.get('/api/v1/issues/?suppl_number=%s' % issue.number, extra_environ=self.extra_environ)
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
        response = self.app.get('/api/v1/issues/?suppl_volume=%s' % issue.volume, extra_environ=self.extra_environ)
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
        response = self.app.get('/api/v1/issues/?suppl_volume=%s' % issue.volume, extra_environ=self.extra_environ)
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
        response1 = self.app.get('/api/v1/issues/?collection=%s&print_issn=%s' % (collection1.name, journal.print_issn) , extra_environ=self.extra_environ)
        content1 = json.loads(response1.content)

        self.assertEqual(response1.status_code, 200)
        self.assertTrue('objects' in response1.content)

        self.assertEqual(len(content1['objects']), 1)

        #test if return nothing issue from collecion2
        response2 = self.app.get('/api/v1/issues/?collection=%s&print_issn=%s' % (collection2.name, journal.print_issn) , extra_environ=self.extra_environ)
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
        response = self.app.get('/api/v1/issues/?suppl_number=999', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 6)

        #test with param number and suppl_volume
        response = self.app.get('/api/v1/issues/?suppl_volume=2', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 3)

        #test with param number and suppl_number and suppl_volume, must return empty list
        response = self.app.get('/api/v1/issues/?suppl_volume=2&suppl_number=999', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 0)

        #test with param number and suppl_number and suppl_volume, change sequence of params
        response = self.app.get('/api/v1/issues/?suppl_number=999&suppl_volume=2', extra_environ=self.extra_environ)
        content = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

        self.assertEqual(len(content['objects']), 0)


class SectionsRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_section_index(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.get('/api/v1/sections/',
            extra_environ=self.extra_environ)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_section_filters(self):
        resource_filters = SectionResource().Meta
        mandatory_filters = ['journal']
        for fltr in mandatory_filters:
            self.assertTrue(fltr in resource_filters.filtering)

    def test_post_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.post('/api/v1/sections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.put('/api/v1/sections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.delete('/api/v1/sections/',
            extra_environ=self.extra_environ, status=405)
        self.assertEqual(response.status_code, 405)

    def test_api_v1_datamodel(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.get('/api/v1/sections/%s/' % section.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'updated',
            'code',
            'created',
            'journal',
            'titles',
            'is_trashed',
            'id',
            'issues',
            'resource_uri'
        ]

        self.assertEqual(list(response.json.keys()), expected_keys)

    def test_access_denied_for_unauthenticated_users(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.get('/api/v1/sections/', status=401)
        self.assertEqual(response.status_code, 401)


class PressReleaseRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_post_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.post('/api/v1/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.put('/api/v1/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.delete('/api/v1/pressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v1/pressreleases/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_pressrelease_index(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v1/pressreleases/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_datamodel(self):
        pr = modelfactories.RegularPressReleaseFactory.create()
        response = self.app.get('/api/v1/pressreleases/%s/' % pr.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'articles',
            'id',
            'issue_uri',
            'resource_uri',
            'translations',
            'issue_meta',
            'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v1_datamodel(self):
        pr_trans = modelfactories.PressReleaseTranslationFactory.create()
        response = self.app.get('/api/v1/pressreleases/%s/' % pr_trans.press_release.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'content',
            'id',
            'language',
            'resource_uri',
            'title',
        ]

        self.assertEqual(
            sorted(response.json['translations'][0].keys()),
            sorted(expected_keys)
        )

    def test_issue_meta_api_v1_datamodel(self):
        pr_trans = modelfactories.PressReleaseTranslationFactory.create()
        response = self.app.get('/api/v1/pressreleases/%s/' % pr_trans.press_release.pk,
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
            '/api/v1/pressreleases/?article_pid=%s' % pr_articles[0].article_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())

        response = self.app.get(
            '/api/v1/pressreleases/?journal_pid=%s' % prs[0].issue.journal.scielo_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter_for_nonexisting_values_skips_filtering(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())
        response = self.app.get(
            '/api/v1/pressreleases/?journal_pid=5',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)

    def test_article_filter_for_nonexisting_values_skips_filtering(self):
        pr_articles = []
        for pr in range(5):
            pr_articles.append(modelfactories.PressReleaseArticleFactory.create())

        response = self.app.get(
            '/api/v1/pressreleases/?article_pid=EMPTY',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)

    def test_issue_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.RegularPressReleaseFactory.create())

        response = self.app.get(
            '/api/v1/pressreleases/?issue_pid=%s' % prs[0].issue.scielo_pid,
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
        response = self.app.post('/api/v1/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.put('/api/v1/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.delete('/api/v1/apressreleases/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v1/apressreleases/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_pressrelease_index(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v1/apressreleases/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_datamodel(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        response = self.app.get('/api/v1/apressreleases/%s/' % pr.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'articles',
            'id',
            'journal_uri',
            'resource_uri',
            'translations',
            'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v1_datamodel(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        pr_trans = modelfactories.PressReleaseTranslationFactory.create(press_release=pr)
        response = self.app.get('/api/v1/apressreleases/%s/' % pr_trans.press_release.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            'content',
            'id',
            'language',
            'resource_uri',
            'title',
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
            '/api/v1/apressreleases/?article_pid=%s' % pr_articles[0].article_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.AheadPressReleaseFactory.create())

        response = self.app.get(
            '/api/v1/apressreleases/?journal_pid=%s' % prs[0].journal.scielo_pid,
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 1)

    def test_journal_filter_for_nonexisting_values_skips_filtering(self):
        prs = []
        for pr in range(5):
            prs.append(modelfactories.AheadPressReleaseFactory.create())
        response = self.app.get(
            '/api/v1/apressreleases/?journal_pid=5',
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
            '/api/v1/apressreleases/?article_pid=EMPTY',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 0)
