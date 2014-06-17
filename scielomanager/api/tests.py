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
from articletrack.tests import modelfactories as articletrack_modelfactories

from api.resources import (
    IssueResource,
    SectionResource,
    JournalResource,
    CheckinResource,
    CheckinNoticeResource,
    CheckinArticleResource,
    TicketResource,
    CommentResource,
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

    def test_access_denied_for_unauthenticated_users(self):
        section = modelfactories.SectionFactory.create()
        response = self.app.get('/api/v1/sections/', status=401)
        self.assertEqual(response.status_code, 401)


class ChangesRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
            self.user.api_key.key)

    def test_changes_index(self):
        event = modelfactories.DataChangeEventFactory.create()
        response = self.app.get('/api/v1/changes/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_since_filter(self):
        seqs = []
        for i in range(5):
            event = modelfactories.DataChangeEventFactory.create()
            seqs.append(event.pk)

        response = self.app.get('/api/v1/changes/?since=%s' % seqs[1],
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)
        self.assertEqual(len(json.loads(response.content)['objects']), 4)

    def test_post_data(self):
        event = modelfactories.DataChangeEventFactory.create()
        response = self.app.post('/api/v1/changes/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_put_data(self):
        event = modelfactories.DataChangeEventFactory.create()
        response = self.app.put('/api/v1/changes/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_del_data(self):
        event = modelfactories.DataChangeEventFactory.create()
        response = self.app.delete('/api/v1/changes/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        event = modelfactories.DataChangeEventFactory.create()
        response = self.app.get('/api/v1/changes/', status=401)

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
            u'articles',
            u'id',
            u'issue_uri',
            u'resource_uri',
            u'translations',
            u'issue_meta',
            u'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v1_datamodel(self):
        pr_trans = modelfactories.PressReleaseTranslationFactory.create()
        response = self.app.get('/api/v1/pressreleases/%s/' % pr_trans.press_release.pk,
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
            u'articles',
            u'id',
            u'journal_uri',
            u'resource_uri',
            u'translations',
            u'doi',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))

    def test_translations_api_v1_datamodel(self):
        pr = modelfactories.AheadPressReleaseFactory.create()
        pr_trans = modelfactories.PressReleaseTranslationFactory.create(press_release=pr)
        response = self.app.get('/api/v1/apressreleases/%s/' % pr_trans.press_release.pk,
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


class CheckinRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
                                                self.user.api_key.key)
        self.article = articletrack_modelfactories.ArticleFactory.create()

    def tearDown(self):
        pass

    def test_post_data(self):

        perm = _makePermission(perm='add_checkin', model='checkin', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {
            u'attempt_ref': 1,
            u'package_name': u'20132404.zip',
            u'uploaded_at': u'2013-11-13 15:23:12.286068-02',
            u'created_at': u'2013-11-13 15:23:18.286068-02',
            u'article': u'/api/v1/checkins_articles/%s/' % self.article.pk,
        }

        response = self.app.post_json('/api/v1/checkins/',
                                      att,
                                      extra_environ=self.extra_environ,
                                      status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        from articletrack import models

        perm = _makePermission(perm='add_checkin', model='checkin', app_label='articletrack')
        self.user.user_permissions.add(perm)
        perm = _makePermission(perm='change_checkin', model='checkin', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'attempt_ref': 2}

        checkin = articletrack_modelfactories.CheckinFactory.create()

        response = self.app.put_json('/api/v1/checkins/%s/' % checkin.pk,
                                att,
                                extra_environ=self.extra_environ,
                                status=204)

        self.assertEqual(response.status_code, 204)
        checkin_check = models.Checkin.objects.get(pk=checkin.pk)
        self.assertEqual(checkin_check.attempt_ref, u'2')

    def test_del_data(self):
        response = self.app.delete('/api/v1/checkins/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get('/api/v1/checkins/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_checkin_index(self):
        articletrack_modelfactories.CheckinFactory.create()
        response = self.app.get('/api/v1/checkins/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_data_checkin(self):
        check = articletrack_modelfactories.CheckinFactory.create()
        response = self.app.get('/api/v1/checkins/%s/' % check.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
                u'accepted_at',
                u'article',
                u'attempt_ref',
                u'created_at',
                u'expiration_at',
                u'id',
                u'package_name',
                u'rejected_at',
                u'rejected_cause',
                u'reviewed_at',
                u'resource_uri',
                u'status',
                u'uploaded_at'
            ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class NoticeRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
                                                self.user.api_key.key)
        self.collection = modelfactories.CollectionFactory.create()

    def tearDown(self):
        pass

    def test_post_data(self):

        checkin = articletrack_modelfactories.CheckinFactory.create()

        perm = _makePermission(perm='add_notice', model='notice', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'checkin': u'/api/v1/checkins/%s/' % checkin.pk,
               u'checkpoint': u'Validation',
               u'uploaded_at': u'2013-11-14T15:10:20.345520',
               u'message': u'The reference of xyz is not OK',
               u'stage': u'Reference',
               u'status': u'warning'
               }

        response = self.app.post_json('/api/v1/notices/',
                                      att,
                                      extra_environ=self.extra_environ,
                                      status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        from articletrack import models

        perm = _makePermission(perm='add_notice', model='notice', app_label='articletrack')
        self.user.user_permissions.add(perm)
        perm = _makePermission(perm='change_notice', model='notice', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'stage': u'DOI'}
        notice = articletrack_modelfactories.NoticeFactory.create(stage='References')

        response = self.app.put_json(
            '/api/v1/notices/%s/' % notice.pk,
            att,
            extra_environ=self.extra_environ,
            status=204)

        self.assertEqual(response.status_code, 204)
        notice_check = models.Notice.objects.get(pk=notice.pk)
        self.assertEqual(notice_check.stage, 'DOI')

    def test_del_data(self):
        response = self.app.delete(
            '/api/v1/notices/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get('/api/v1/notices/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_notice_index(self):
        articletrack_modelfactories.NoticeFactory.create()

        response = self.app.get(
            '/api/v1/notices/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_model_notice(self):
        check = articletrack_modelfactories.NoticeFactory.create()
        response = self.app.get(
            '/api/v1/notices/%s/' % check.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'checkin',
            u'checkpoint',
            u'created_at',
            u'id',
            u'resource_uri',
            u'message',
            u'stage',
            u'status'
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class CheckinArticleRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
                                                self.user.api_key.key)

    def tearDown(self):
        pass

    def test_post_data(self):
        perm = _makePermission(perm='add_article', model='article', app_label='articletrack')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory.create()

        att = {
            u'articlepkg_ref': 1,
            u'article_title': u'An azafluorenone alkaloid and a megastigmane from Unonopsis lindmanii (Annonaceae)',
            u'journal_title': u'Journal of the Brazilian Chemical Society',
            u'issue_label': u'2013 v.24 n.4',
            u'eissn': u'',
            u'pissn': u'1234-0002',  # matching with JournalFactory.print_issn
        }
        response = self.app.post_json('/api/v1/checkins_articles/',
                                      att,
                                      extra_environ=self.extra_environ,
                                      status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

        # assert the related journal was found and bound.
        from articletrack import models
        article_id = response.location.rsplit('/', 2)[-2]
        self.assertTrue(journal in models.Article.objects.get(pk=article_id).journals.all())

    def test_post_data_invalid_journal(self):
        perm = _makePermission(perm='add_article', model='article', app_label='articletrack')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory.create()

        att = {
            u'articlepkg_ref': 1,
            u'article_title': u'An azafluorenone alkaloid and a megastigmane from Unonopsis lindmanii (Annonaceae)',
            u'journal_title': u'Journal of the Brazilian Chemical Society',
            u'issue_label': u'2013 v.24 n.4',
            u'eissn': u'',
            u'pissn': u'xxx',  # matching with JournalFactory.print_issn
        }
        response = self.app.post_json('/api/v1/checkins_articles/',
                                      att,
                                      extra_environ=self.extra_environ,
                                      status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        from articletrack import models

        perm = _makePermission(perm='add_article', model='article', app_label='articletrack')
        self.user.user_permissions.add(perm)
        perm = _makePermission(perm='change_article', model='article', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'issue_label': u'2013 v.24 n.5'}

        article = articletrack_modelfactories.ArticleFactory.create()

        response = self.app.put_json(
            '/api/v1/checkins_articles/%s/' % article.pk,
            att,
            extra_environ=self.extra_environ,
            status=204)

        self.assertEqual(response.status_code, 204)
        article_check = models.Article.objects.get(pk=article.pk)
        self.assertEqual(article_check.issue_label, u'2013 v.24 n.5')

    def test_del_data(self):
        response = self.app.delete(
            '/api/v1/checkins_articles/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get('/api/v1/checkins_articles/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_checkin_index(self):
        articletrack_modelfactories.ArticleFactory.create()
        response = self.app.get(
            '/api/v1/checkins_articles/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_data_checkin(self):
        article = articletrack_modelfactories.ArticleFactory.create()
        response = self.app.get(
            '/api/v1/checkins_articles/%s/' % article.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'article_title',
            u'articlepkg_ref',
            u'eissn',
            u'id',
            u'issue_label',
            u'journal_title',
            u'journals',
            u'pissn',
            u'resource_uri',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class TicketRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
                                                self.user.api_key.key)
        self.article = articletrack_modelfactories.ArticleFactory.create()
        self.author = modelfactories.UserFactory(is_active=True)

    def tearDown(self):
        pass

    def test_post_data(self):

        perm = _makePermission(perm='add_ticket', model='ticket', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {
            u'started_at': '2013-11-17 15:23:18',
            u'author': u'/api/v1/users/%s/' % self.author.pk,
            u'title': u'title of the ticket',
            u'message': u'message of the ticket',
            u'article': u'/api/v1/checkins_articles/%s/' % self.article.pk,
        }

        response = self.app.post_json(
            '/api/v1/tickets/',
            att,
            extra_environ=self.extra_environ,
            status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        from articletrack import models

        perm = _makePermission(perm='add_ticket', model='ticket', app_label='articletrack')
        self.user.user_permissions.add(perm)
        perm = _makePermission(perm='change_ticket', model='ticket', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'finished_at': '2013-11-18 15:23:12', }
        ticket = articletrack_modelfactories.TicketFactory.create(author=self.author, article=self.article)

        response = self.app.put_json(
            '/api/v1/tickets/%s/' % ticket.pk,
            att,
            extra_environ=self.extra_environ,
            status=204)

        self.assertEqual(response.status_code, 204)
        ticket_check = models.Ticket.objects.get(pk=ticket.pk)
        self.assertEqual(ticket_check.finished_at, datetime.datetime(2013, 11, 18, 15, 23, 12))
        self.assertFalse(ticket_check.is_open)

    def test_del_data(self):
        response = self.app.delete(
            '/api/v1/tickets/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get('/api/v1/tickets/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_checkin_index(self):
        articletrack_modelfactories.TicketFactory.create(author=self.author, article=self.article)
        response = self.app.get(
            '/api/v1/tickets/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_data_checkin(self):
        ticket = articletrack_modelfactories.TicketFactory.create(author=self.author, article=self.article)
        response = self.app.get(
            '/api/v1/tickets/%s/' % ticket.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'article',
            u'author',
            u'finished_at',
            u'id',
            u'message',
            u'started_at',
            u'title',
            u'resource_uri',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))


class CommentRestAPITest(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)
        self.extra_environ = _make_auth_environ(self.user.username,
                                                self.user.api_key.key)
        self.ticket = articletrack_modelfactories.TicketFactory.create()
        self.author = modelfactories.UserFactory(is_active=True)

    def tearDown(self):
        pass

    def test_post_data(self):

        perm = _makePermission(perm='add_comment', model='comment', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {
            u'author': u'/api/v1/users/%s/' % self.author.pk,
            u'message': u'message of the comment',
            u'ticket': u'/api/v1/tickets/%s/' % self.ticket.pk,
        }

        response = self.app.post_json('/api/v1/comments/',
                                      att,
                                      extra_environ=self.extra_environ,
                                      status=201)

        # 201 stands for CREATED Http status
        self.assertEqual(response.status_code, 201)

    def test_put_data(self):
        from articletrack import models

        perm = _makePermission(perm='add_comment', model='comment', app_label='articletrack')
        self.user.user_permissions.add(perm)
        perm = _makePermission(perm='change_comment', model='comment', app_label='articletrack')
        self.user.user_permissions.add(perm)

        att = {u'message': u'new message', }

        comment = articletrack_modelfactories.CommentFactory.create(author=self.author, ticket=self.ticket)
        response = self.app.put_json(
            '/api/v1/comments/%s/' % comment.pk,
            att,
            extra_environ=self.extra_environ,
            status=204)

        self.assertEqual(response.status_code, 204)
        comment_check = models.Comment.objects.get(pk=comment.pk)
        self.assertEqual(comment_check.message, u'new message')

    def test_del_data(self):
        response = self.app.delete(
            '/api/v1/comments/',
            extra_environ=self.extra_environ, status=405)

        self.assertEqual(response.status_code, 405)

    def test_access_denied_for_unauthenticated_users(self):
        response = self.app.get('/api/v1/comments/', status=401)

        self.assertEqual(response.status_code, 401)

    def test_checkin_index(self):
        articletrack_modelfactories.CommentFactory.create(author=self.author, ticket=self.ticket)
        response = self.app.get(
            '/api/v1/comments/',
            extra_environ=self.extra_environ)

        self.assertEqual(response.status_code, 200)
        self.assertTrue('objects' in response.content)

    def test_api_v1_data_checkin(self):
        comment = articletrack_modelfactories.CommentFactory.create(author=self.author, ticket=self.ticket)
        response = self.app.get(
            '/api/v1/comments/%s/' % comment.pk,
            extra_environ=self.extra_environ)

        expected_keys = [
            u'author',
            u'created_at',
            u'updated_at',
            u'id',
            u'message',
            u'ticket',
            u'resource_uri',
        ]

        self.assertEqual(sorted(response.json.keys()), sorted(expected_keys))
