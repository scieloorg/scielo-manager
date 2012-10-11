# coding:utf-8
"""
Use this module to write functional tests for the view-functions, only!
"""
import os
from django_webtest import WebTest
from django.core.urlresolvers import reverse
from django.core import mail
from django_factory_boy import auth

from journalmanager.tests import modelfactories


HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


def _makePermission(perm, model, app_label='journalmanager'):
    """
    Retrieves a Permission according to the given model and app_label.
    """
    from django.contrib.contenttypes import models
    from django.contrib.auth import models as auth_models

    ct = models.ContentType.objects.get(model=model,
                                        app_label=app_label)
    return auth_models.Permission.objects.get(codename=perm, content_type=ct)


class SectionFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_user_access_section_list_without_itens(self):
        perm_sponsor_list = _makePermission(perm='list_section', model='section', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_list)

        journal = modelfactories.JournalFactory(collection=self.collection)

        page = self.app.get(reverse('section.index', args=[journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in page.body)

    def test_access_without_permission(self):
        journal = modelfactories.JournalFactory(collection=self.collection)
        response = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user)

        self.assertTemplateUsed(form, 'journalmanager/add_section.html')
        form.mustcontain('section-form',
                         'csrfmiddlewaretoken',
                         'titles-TOTAL_FORMS',
                         'titles-INITIAL_FORMS',
                         'titles-MAX_NUM_FORMS',
                        )

    def test_POST_workflow_with_valid_formdata(self):
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        form['titles-0-title'] = 'Original Article'
        form.set('titles-0-language', language.pk)

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/section_dashboard.html')
        response.mustcontain('Original Article')

    def test_POST_workflow_with_invalid_formdata(self):
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en', name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')


class UserFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_access_without_permission(self):
        response = self.app.get(reverse('user.add'), user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('user.add'), user=self.user)

        self.assertTemplateUsed(page, 'journalmanager/add_user.html')
        page.mustcontain('user-form',
                         'csrfmiddlewaretoken',
                         'usercollections-TOTAL_FORMS',
                         'usercollections-INITIAL_FORMS',
                         'usercollections-MAX_NUM_FORMS',
                        )

    def test_POST_workflow_with_valid_formdata(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'), user=self.user).forms['user-form']

        form['user-username'] = 'bazz'
        form['user-first_name'] = 'foo'
        form['user-last_name'] = 'bar'
        form['userprofile-0-email'] = 'bazz@spam.org'
        # form.set('asmSelect0', '1')  # groups
        form.set('usercollections-0-collection', self.collection.pk)  # collections

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/user_dashboard.html')
        response.mustcontain('bazz', 'bazz@spam.org')

        # check if an email has been sent to the new user
        self.assertTrue(len(mail.outbox), 1)
        self.assertIn('bazz@spam.org', mail.outbox[0].recipients())

        # check if basic state has been set
        self.assertTrue(response.context['user'].user_collection.get(
            pk=self.collection.pk))

    def test_POST_workflow_with_invalid_formdata(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'), user=self.user).forms['user-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')


class IndexPageTests(WebTest):

    def test_logged_user_access_to_index(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('index'), user=user)

        self.assertTemplateUsed(response, 'journalmanager/home_journal.html')

    def test_not_logged_user_access_to_index(self):
        response = self.app.get(reverse('index')).follow()

        self.assertTemplateUsed(response, 'registration/login.html')


class UserIndexPageTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_logged_user_access(self):
        perm = _makePermission(perm='change_user', model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(self.user, is_manager=True)

        response = self.app.get(reverse('user.index'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/user_dashboard.html')

    def test_logged_user_access_users_not_being_manager_of_the_collection(self):
        user = auth.UserF(is_active=True)

        collection = modelfactories.CollectionFactory.create()
        collection.add_user(user)

        response = self.app.get(reverse('user.index'), user=user).follow()

        self.assertTemplateUsed(response, 'accounts/unauthorized.html')
        response.mustcontain('not authorized to access')


class JournalFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_access_without_permission(self):
        response = self.app.get(reverse('journal.add'), user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        perm = _makePermission(perm='change_journal',
                               model='journal',
                               app_label='journalmanager')
        self.user.user_permissions.add(perm)

        response = self.app.get(reverse('journal.add'), user=self.user)

        self.assertTemplateUsed(response, 'journalmanager/add_journal.html')
        response.mustcontain('journal-form',
                             'csrfmiddlewaretoken',
                             'title-TOTAL_FORMS',
                             'title-INITIAL_FORMS',
                             'title-MAX_NUM_FORMS',
                             'studyarea-TOTAL_FORMS',
                             'studyarea-INITIAL_FORMS',
                             'studyarea-MAX_NUM_FORMS',
                             'mission-TOTAL_FORMS',
                             'mission-INITIAL_FORMS',
                             'mission-MAX_NUM_FORMS',
                            )

    def test_user_access_journals_list_without_itens(self):
        perm_journal_list = _makePermission(perm='list_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_list)

        response = self.app.get(reverse('journal.index'), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_user_add_journal_with_invalid_formdata(self):
        perm = _makePermission(perm='change_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        sponsor = modelfactories.SponsorFactory.create()

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

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

        self.assertTrue('errors_list', response.body)

        self.assertTemplateUsed(response, 'journalmanager/add_journal.html')

    def test_user_add_journal_with_valid_formdata(self):
        perm_journal_change = _makePermission(perm='change_journal', model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal', model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        sponsor = modelfactories.SponsorFactory.create()

        use_license = modelfactories.UseLicenseFactory.create()

        language = modelfactories.LanguageFactory.create()

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

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

        form['journal-use_license'] = use_license.pk

        form['journal-collection'] = str(self.collection.pk)

        form['journal-languages'] = [language.pk]

        form['journal-abstract_keyword_languages'] = [language.pk]

        response = form.submit().follow()

        self.assertTrue('Saved.' in response.body)

        self.assertTrue('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xc3\xa3o Paulo)' in response.body)

        self.assertTemplateUsed(response, 'journalmanager/journal_dashboard.html')

class SponsorFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_user_access_journals_list_without_itens(self):
        perm_sponsor_list = _makePermission(perm='list_sponsor', model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_list)

        response = self.app.get(reverse('sponsor.index'), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_basic_structure(self):
        perm = _makePermission(perm='add_sponsor', model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('sponsor.add'), user=self.user)

        page.mustcontain('sponsor-name', 'sponsor-collections')

        self.assertTemplateUsed(page, 'journalmanager/add_sponsor.html')

    def test_user_access_without_permission(self):

        page = self.app.get(reverse('sponsor.add'), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')

        page.mustcontain('not authorized to access')

    def test_user_add_sponsor_with_valid_formdata(self):
        perm_sponsor_change = _makePermission(perm='add_sponsor', model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor', model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]
        
        form['sponsor-name'] =  u'Fundação de Amparo a Pesquisa do Estado de São Paulo'
        form['sponsor-address'] =  u'Av. Professor Lineu Prestes, 338 Cidade Universitária \
                                    Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047'
        form['sponsor-email'] =  'fapesp@scielo.org'
        form['sponsor-complement'] =  ''

        form['sponsor-collections'] = [self.collection.pk]

        response = form.submit().follow()

        self.assertTemplateUsed(response, 'journalmanager/sponsor_dashboard.html') 

        self.assertTrue('Saved.' in response.body)  

        self.assertTrue('Funda\xc3\xa7\xc3\xa3o de Amparo a Pesquisa do Estado de S\xc3\xa3o Paulo' in response.body)       

    def test_user_add_sponsor_with_invalid_formdata(self):
        perm_sponsor_change = _makePermission(perm='add_sponsor', model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor', model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]
        
        form['sponsor-address'] =  u'Av. Professor Lineu Prestes, 338 Cidade Universitária \
                                    Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047'
        form['sponsor-email'] =  'fapesp@scielo.org'
        form['sponsor-complement'] =  ''

        form['sponsor-collections'] = [self.collection.pk]

        response = form.submit()

        self.assertTrue('errors_list' in response.body)  

        self.assertTemplateUsed(response, 'journalmanager/add_sponsor.html') 

class IssueFormTests(WebTest):  

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory(collection=self.collection)

    def test_user_access_issue_list_without_itens(self):
        perm_issue_list = _makePermission(perm='list_issue', model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_list)

        response = self.app.get(reverse('issue.index', args=[self.journal.pk]), user=self.user)

        self.assertTrue('There are no items.' in response.body)

    def test_basic_struture(self):
        perm = _makePermission(perm='add_issue', model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('issue.add', args=[self.journal.pk]), user=self.user)

        page.mustcontain('number', 'cover',
                         'title-0-title',
                         'title-0-language',
                         'title-TOTAL_FORMS',
                         'title-INITIAL_FORMS',
                         'title-MAX_NUM_FORMS')

        self.assertTemplateUsed(page, 'journalmanager/add_issue.html')

    def test_user_access_without_permission(self):

        page = self.app.get(reverse('issue.add', args=[self.journal.pk]), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')

        page.mustcontain('not authorized to access')

    def test_user_add_issue_with_valid_formdata(self):
        perm_issue_change = _makePermission(perm='add_issue', model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue', model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add', args=[self.journal.pk]), user=self.user).forms[1]

        form['total_documents'] = '16'
        form.set('ctrl_vocabulary', 'decs')
        form['number'] = '3'
        form['volume'] = '29'
        form['editorial_standard'] = ''
        form['is_press_release'] = False
        form['publication_start_month'] = '9'
        form['publication_end_month'] = '11'
        form['publication_year'] = '2012'
        form['order'] = '201203'
        form['is_marked_up'] = False
        form['editorial_standard'] = 'other'
        
        response = form.submit().follow()

        self.assertTrue('Saved.' in response.body)

        self.assertTemplateUsed(response, 'journalmanager/issue_dashboard.html')

    def test_user_add_issue_with_invalid_formdata(self):
        perm_issue_change = _makePermission(perm='add_issue', model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue', model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add', args=[self.journal.pk]), user=self.user).forms[1]

        form['total_documents'] = '16'
        form.set('ctrl_vocabulary', 'decs')
        form['number'] = '3'
        form['editorial_standard'] = ''
        form['is_press_release'] = False
        form['publication_start_month'] = '9'
        form['publication_end_month'] = '11'
        form['publication_year'] = '2012'
        form['order'] = '201203'
        form['is_marked_up'] = False
        form['editorial_standard'] = 'other'
        
        response = form.submit()

        self.assertTrue('errors_list' in response.body)

        self.assertTemplateUsed(response, 'journalmanager/add_issue.html')

class StatusFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory(collection=self.collection)

    def test_basic_struture(self):
        perm = _makePermission(perm='list_publication_events', model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('journal_status.edit', args=[self.journal.pk]), user=self.user)

        page.mustcontain('pub_status', 'pub_status_reason')

        self.assertTemplateUsed(page, 'journalmanager/edit_journal_status.html')

    def test_user_access_without_permission(self):

        page = self.app.get(reverse('journal_status.edit', args=[self.journal.pk]), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')

        page.mustcontain('not authorized to access')

    def test_user_add_status_with_valid_formdata(self):
        perm = _makePermission(perm='list_publication_events', model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit', args=[self.journal.pk]), user=self.user).forms[1]

        form.set('pub_status', 'deceased')
        form['pub_status_reason'] = 'Motivo 1'

        response = form.submit().follow()

        self.assertTrue('Saved.' in response.body)

        self.assertTemplateUsed(response, 'journalmanager/edit_journal_status.html')

    def test_user_add_status_with_invalid_formdata(self):
        perm = _makePermission(perm='list_publication_events', model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit', args=[self.journal.pk]), user=self.user).forms[1]

        form.set('pub_status', 'deceased')

        response = form.submit()

        self.assertTrue('errors_list' in response.body)

        self.assertTemplateUsed(response, 'journalmanager/edit_journal_status.html')

class SearchFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_basic_struture(self):
        page = self.app.get(reverse('index'), user=self.user)

        page.mustcontain('list_model', 'q')

        self.assertTemplateUsed(page, 'journalmanager/home_journal.html')


