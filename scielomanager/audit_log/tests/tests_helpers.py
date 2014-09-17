# coding:utf-8
import unittest

from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.forms.models import inlineformset_factory
from django.contrib.auth.models import User
from django.utils.text import get_text_list
from django.utils.encoding import force_unicode
from django.contrib.contenttypes.models import ContentType

from journalmanager.tests import modelfactories as jm_modelfactories
from journalmanager import forms as jm_forms
from journalmanager import models as jm_models
from journalmanager.tests.tests_forms import _makePermission, _makeUseLicense

from audit_log import models as audit_models


# based on JournalFormTests from journalmanager.tests_forms,
# changing the forms will generate audit log entries


class AuditLogFromJournalFormTests(WebTest):

    def setUp(self):
        self.user = jm_modelfactories.UserFactory(is_active=True)

        self.collection = jm_modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)
        _makeUseLicense()

    def tearDown(self):
        """
        Restore the default values.
        """

    def test_POST_invalid_formdata_do_not_log(self):
        """
        When an invalid form is submited, no action is taken, no changes are made, so no log are recorded.
        """
        perm = _makePermission(perm='change_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        sponsor = jm_modelfactories.SponsorFactory.create()

        form = self.app.get(reverse('journal.add'), user=self.user).forms['journal-form']

        form['journal-sponsor'] = [sponsor.pk]
        form['journal-ctrl_vocabulary'] = 'decs'
        form['journal-frequency'] = 'Q'
        form['journal-final_num'] = ''
        form['journal-eletronic_issn'] = '0102-6720'
        form['journal-init_vol'] = '1'
        form['journal-title'] = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
        form['journal-title_iso'] = u'ABCD. Arquivos B. de C. D. (São Paulo)'
        form['journal-short_title'] = u'ABCD.(São Paulo)'
        form['journal-editorial_standard'] = 'vancouv'
        form['journal-scielo_issn'] = 'print'
        form['journal-init_year'] = '1986'
        form['journal-acronym'] = 'ABCD'
        form['journal-pub_level'] = 'CT'
        form['journal-init_num'] = '1'
        form['journal-final_vol'] = ''
        form['journal-subject_descriptors'] = 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA'
        form['journal-print_issn'] = '0102-6720'
        form['journal-copyrighter'] = 'Texto do copyrighter'
        form['journal-publisher_name'] = 'Colégio Brasileiro de Cirurgia Digestiva'
        form['journal-publisher_country'] = 'BR'
        form['journal-publisher_state'] = 'SP'
        form['journal-publication_city'] = 'São Paulo'
        form['journal-editor_address'] = 'Av. Brigadeiro Luiz Antonio, 278 - 6° - Salas 10 e 11, 01318-901 \
                                          São Paulo/SP Brasil, Tel.: (11) 3288-8174/3289-0741'
        form['journal-editor_email'] = 'cbcd@cbcd.org.br'

        response = form.submit()
        self.assertIn('There are some errors or missing data', response.body)
        self.assertEqual(audit_models.AuditLogEntry.objects.count(), 0)


    def test_POST_valid_formdata_do_log(self):
        # with:
        perm_journal_change = _makePermission(perm='change_journal', model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        sponsor = jm_modelfactories.SponsorFactory.create()
        use_license = jm_modelfactories.UseLicenseFactory.create()
        language = jm_modelfactories.LanguageFactory.create()
        subject_category = jm_modelfactories.SubjectCategoryFactory.create()
        study_area = jm_modelfactories.StudyAreaFactory.create()

        form = self.app.get(reverse('journal.add'), user=self.user).forms['journal-form']
        form['journal-sponsor'] = [sponsor.pk]
        form['journal-study_areas'] = [study_area.pk]
        form['journal-ctrl_vocabulary'] = 'decs'
        form['journal-frequency'] = 'Q'
        form['journal-final_num'] = ''
        form['journal-eletronic_issn'] = '0102-6720'
        form['journal-init_vol'] = '1'
        form['journal-title'] = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
        form['journal-title_iso'] = u'ABCD. Arquivos B. de C. D. (São Paulo)'
        form['journal-short_title'] = u'ABCD.(São Paulo)'
        form['journal-editorial_standard'] = 'vancouv'
        form['journal-scielo_issn'] = 'print'
        form['journal-init_year'] = '1986'
        form['journal-acronym'] = 'ABCD'
        form['journal-pub_level'] = 'CT'
        form['journal-init_num'] = '1'
        form['journal-final_vol'] = ''
        form['journal-subject_descriptors'] = 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA'
        form['journal-print_issn'] = '0102-6720'
        form['journal-copyrighter'] = 'Texto do copyrighter'
        form['journal-publisher_name'] = 'Colégio Brasileiro de Cirurgia Digestiva'
        form['journal-publisher_country'] = 'BR'
        form['journal-publisher_state'] = 'SP'
        form['journal-publication_city'] = 'São Paulo'
        form['journal-editor_name'] = 'Colégio Brasileiro de Cirurgia Digestiva'
        form['journal-editor_address'] = 'Av. Brigadeiro Luiz Antonio, 278 - 6° - Salas 10 e 11'
        form['journal-editor_address_city'] = 'São Paulo'
        form['journal-editor_address_state'] = 'SP'
        form['journal-editor_address_zip'] = '01318-901'
        form['journal-editor_address_country'] = 'BR'
        form['journal-editor_phone1'] = '(11) 3288-8174'
        form['journal-editor_phone2'] = '(11) 3289-0741'
        form['journal-editor_email'] = 'cbcd@cbcd.org.br'
        form['journal-use_license'] = use_license.pk
        form['journal-languages'] = [language.pk]
        form['journal-abstract_keyword_languages'] = [language.pk]
        form.set('journal-subject_categories', [str(subject_category.pk),])
        form['journal-is_indexed_scie'] = True
        form['journal-is_indexed_ssci'] = False
        form['journal-is_indexed_aehci'] = True

        # when:
        response = form.submit().follow()

        # then:
        self.assertIn('Saved.', response.body)
        self.assertIn('ABCD.(São Paulo)', response.body)
        self.assertTemplateUsed(response, 'journalmanager/journal_dash.html')

        self.assertEqual(audit_models.AuditLogEntry.objects.count(), 1)
        log_entry = audit_models.AuditLogEntry.objects.all()[0]
        audited_object = log_entry.get_audited_object()
        # inspect audited log entry data:
        self.assertEqual(log_entry.action_flag, audit_models.ADDITION)
        self.assertEqual(log_entry.object_id, unicode(audited_object.pk))
        self.assertEqual(log_entry.content_type, ContentType.objects.get_for_model(audited_object))
        self.assertEqual(log_entry.old_values, None)
        self.assertEqual(log_entry.user, self.user)

        fields_edited = [
            'sponsor',
            'use_license',
            'languages',
            'abstract_keyword_languages',
            'subject_categories',
            'study_areas',
            'current_ahead_documents',
            'previous_ahead_documents',
            'title',
            'title_iso',
            'short_title',
            'acronym',
            'scielo_issn',
            'print_issn',
            'eletronic_issn',
            'subject_descriptors',
            'init_year',
            'init_vol',
            'init_num',
            'frequency',
            'editorial_standard',
            'ctrl_vocabulary',
            'pub_level',
            'copyrighter',
            'editor_name',
            'editor_address',
            'editor_address_city',
            'editor_address_state',
            'editor_address_zip',
            'editor_address_country',
            'editor_phone1',
            'editor_phone2',
            'editor_email',
            'publisher_name',
            'publisher_country',
            'publisher_state',
            'publication_city',
            'is_indexed_scie',
            'is_indexed_aehci',
        ]

        expected_change_message = u'Changed fields: %s.' % get_text_list(fields_edited, 'and')
        self.assertEqual(log_entry.change_message, expected_change_message)

        self.assertEqual(log_entry.new_values.keys(), [u'form_data', u'formsets_data'])
        # all edited fields are in "new_values"-dict
        for field_edited in fields_edited:
            self.assertIn(field_edited, log_entry.new_values['form_data'].keys())

        # compare form data and stored new_values data
        for k,v in log_entry.new_values['form_data'].iteritems():
            if k in ['previous_ahead_documents', 'current_ahead_documents']:
                # when created, are set by default to None,
                # and when saved to db are transformed to jsonfield, is saved as u'None'
                self.assertEqual(log_entry.new_values['form_data'][k], u'None')
            else:
                form_value = form['journal-%s' % k].value
                self.assertEqual(log_entry.new_values['form_data'][k], force_unicode(v))
