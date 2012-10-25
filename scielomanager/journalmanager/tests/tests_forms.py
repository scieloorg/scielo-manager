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

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        journal = modelfactories.JournalFactory(collection=self.collection)
        response = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
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
        """
        When a valid form is submited, the user is redirected to
        the section's dashboard and the new section must be part
        of the list.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.change_section`` and
        ``journalmanager.list_section``.
        """
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        form['titles-0-title'] = 'Original Article'
        form.set('titles-0-language', language.pk)

        response = form.submit().follow()

        self.assertTemplateUsed(response,
            'journalmanager/section_dashboard.html')
        response.mustcontain('Original Article')

    def test_POST_workflow_with_invalid_formdata(self):
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')

    def test_POST_workflow_with_exist_title_on_the_same_journal(self):
        """
        Asserts that the Section invalid the insert with same title
        """
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        journal.languages.add(language)

        section = modelfactories.SectionFactory(journal=journal)
        section.add_title('Original Article', language=language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        form['titles-0-title'] = 'Original Article'
        form.set('titles-0-language', language.pk)

        response = form.submit()

        response.mustcontain('This section title already exists for this Journal.')
        self.assertTemplateUsed(response,
            'journalmanager/add_section.html')

    def test_section_title_must_be_case_insensitive(self):
        """
        Asserts that is not possible to create a Section if another with
        the same name already exists for this Journal, even if its
        font case is different.
        """
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        journal.languages.add(language)

        section = modelfactories.SectionFactory(journal=journal)
        section.add_title('original Article', language=language)

        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        form['titles-0-title'] = 'Original Article'
        form.set('titles-0-language', language.pk)

        response = form.submit()

        response.mustcontain('This section title already exists for this Journal.')
        self.assertTemplateUsed(response,
            'journalmanager/add_section.html')

    def test_section_must_allow_new_title_translations(self):
        """
        Asserts that is possible to create new title translations to
        existing Sections.
        """
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        language2 = modelfactories.LanguageFactory.create(iso_code='pt',
                                                         name='portuguese')
        journal.languages.add(language)
        journal.languages.add(language2)

        section = modelfactories.SectionFactory(journal=journal)
        section.add_title('Original Article', language=language)

        form = self.app.get(reverse('section.edit',
            args=[journal.pk, section.pk]), user=self.user).forms['section-form']

        form['titles-1-title'] = 'Artigo Original'
        form.set('titles-1-language', language2.pk)

        response = form.submit().follow()

        self.assertTemplateUsed(response,
            'journalmanager/section_dashboard.html')
        response.mustcontain('Original Article / Artigo Original')

    def test_section_translations_based_on_the_journal_languages(self):
        """
        The language list in a Section form must be contextualized with
        the languages bound to the Journal who it relates.
        """
        perm1 = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm1)
        perm2 = _makePermission(perm='list_section', model='section')
        self.user.user_permissions.add(perm2)

        journal = modelfactories.JournalFactory(collection=self.collection)
        language = modelfactories.LanguageFactory.create(iso_code='en',
                                                         name='english')
        language2 = modelfactories.LanguageFactory.create(iso_code='pt',
                                                         name='portuguese')
        journal.languages.add(language)

        form = self.app.get(reverse('section.add',
            args=[journal.pk]), user=self.user).forms['section-form']

        form['titles-0-title'] = 'Artigo Original'

        self.assertRaises(ValueError, lambda: form.set('titles-0-language', language2.pk))

    def test_form_enctype_must_be_urlencoded(self):
        """
        Asserts that the enctype attribute of the section form is
        ``application/x-www-form-urlencoded``
        """
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        self.assertEqual(form.enctype, 'application/x-www-form-urlencoded')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the section form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the section form is
        ``POST``.
        """
        perm = _makePermission(perm='change_section', model='section')
        self.user.user_permissions.add(perm)

        journal = modelfactories.JournalFactory(collection=self.collection)
        form = self.app.get(reverse('section.add', args=[journal.pk]),
            user=self.user).forms['section-form']

        self.assertEqual(form.method.lower(), 'post')


class UserFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        response = self.app.get(reverse('user.add'),
            user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_access_without_being_manager(self):
        """
        Asserts that authenticated users that are not managers of the
        collection are unable to access the form. They must be redirected
        to a page with informations about their lack of permissions.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        # adding another collection the user lacks manager privileges
        other_collection = modelfactories.CollectionFactory.create()
        other_collection.add_user(self.user, is_manager=False)
        other_collection.make_default_to_user(self.user)

        response = self.app.get(reverse('user.add'),
            user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
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
        """
        When a valid form is submited, the user is redirected to
        the user's dashboard and the new user must be part
        of the list.

        An email must be sent to the new user.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.change_user``.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        form['user-username'] = 'bazz'
        form['user-first_name'] = 'foo'
        form['user-last_name'] = 'bar'
        form['userprofile-0-email'] = 'bazz@spam.org'
        # form.set('asmSelect0', '1')  # groups
        form.set('usercollections-0-collection', self.collection.pk)

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
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        response = form.submit()

        response.mustcontain('There are some errors or missing data')

    def test_form_enctype_must_be_urlencoded(self):
        """
        Asserts that the enctype attribute of the user form is
        ``application/x-www-form-urlencoded``
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        self.assertEqual(form.enctype, 'application/x-www-form-urlencoded')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the user form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the user form is
        ``POST``.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        self.assertEqual(form.method.lower(), 'post')

    def test_add_users_only_to_managed_collections(self):
        """
        A user can only add users to collections which he is manager.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.change_user``.
        """
        perm = _makePermission(perm='change_user',
            model='user', app_label='auth')
        self.user.user_permissions.add(perm)

        other_collection = modelfactories.CollectionFactory.create()
        other_collection.add_user(self.user)

        form = self.app.get(reverse('user.add'),
            user=self.user).forms['user-form']

        self.assertRaises(ValueError, lambda: form.set('usercollections-0-collection', other_collection.pk))


class JournalFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        response = self.app.get(reverse('journal.add'),
            user=self.user).follow()

        response.mustcontain('not authorized to access')
        self.assertTemplateUsed(response, 'accounts/unauthorized.html')

    def test_basic_structure(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
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

    def test_POST_workflow_with_invalid_formdata(self):
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
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

        self.assertTrue('alert alert-error', response.body)
        self.assertIn('There are some errors or missing data', response.body)
        self.assertTemplateUsed(response, 'journalmanager/add_journal.html')

    def test_user_add_journal_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the journal's dashboard and the new user must be part
        of the list.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.change_journal`` and
        ``journalmanager.list_journal``.
        """
        perm_journal_change = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        sponsor = modelfactories.SponsorFactory.create()
        use_license = modelfactories.UseLicenseFactory.create()
        language = modelfactories.LanguageFactory.create()
        subject_category = modelfactories.SubjectCategoryFactory.create()

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
        form.set('journal-subject_categories', str(subject_category.pk))
        form['journal-is_indexed_scie'] = True
        form['journal-is_indexed_ssci'] = False
        form['journal-is_indexed_aehci'] = True

        upload_cover_name = os.path.dirname(__file__) + '/image_test/cover.gif'
        uploaded_cover_contents = open(upload_cover_name, "rb").read()

        form.set('journal-cover', (upload_cover_name, uploaded_cover_contents))

        response = form.submit().follow()

        self.assertIn('Saved.', response.body)
        self.assertIn('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xc3\xa3o Paulo)',
            response.body)
        self.assertTemplateUsed(response, 'journalmanager/journal_dashboard.html')

    def test_form_enctype_must_be_multipart_formdata(self):
        """
        Asserts that the enctype attribute of the user form is
        ``multipart/form-data``
        """
        perm_journal_change = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

        self.assertEqual(form.enctype, 'multipart/form-data')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the journal form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm_journal_change = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the journal form is
        ``POST``.
        """
        perm_journal_change = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

        self.assertEqual(form.method.lower(), 'post')

    def test_collections_field_must_only_display_collections_bound_to_the_user(self):
        """
        Asserts that the user cannot add a sponsor to a collection
        that he is not related to.
        """
        perm_journal_change = _makePermission(perm='change_journal',
            model='journal', app_label='journalmanager')
        perm_journal_list = _makePermission(perm='list_journal',
            model='journal', app_label='journalmanager')
        self.user.user_permissions.add(perm_journal_change)
        self.user.user_permissions.add(perm_journal_list)

        sponsor = modelfactories.SponsorFactory.create()
        use_license = modelfactories.UseLicenseFactory.create()
        language = modelfactories.LanguageFactory.create()

        collection2 = modelfactories.CollectionFactory.create()
        collection2.add_user(self.user)
        collection3 = modelfactories.CollectionFactory.create()

        form = self.app.get(reverse('journal.add'), user=self.user).forms[1]

        self.assertRaises(ValueError,
            lambda: form.set('journal-collection', collection3.pk))


class SponsorFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_basic_structure(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
        perm = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('sponsor.add'), user=self.user)

        page.mustcontain('sponsor-name', 'sponsor-collections')
        self.assertTemplateUsed(page, 'journalmanager/add_sponsor.html')

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        page = self.app.get(reverse('sponsor.add'), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')
        page.mustcontain('not authorized to access')

    def test_POST_workflow_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the sponsor's dashboard and the new sponsor must be part
        of the list.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.add_sponsor`` and
        ``journalmanager.list_sponsor``.
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        form['sponsor-name'] = u'Fundação de Amparo a Pesquisa do Estado de São Paulo'
        form['sponsor-address'] = u'Av. Professor Lineu Prestes, 338 Cidade Universitária \
                                    Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047'
        form['sponsor-email'] = 'fapesp@scielo.org'
        form['sponsor-complement'] = ''
        form['sponsor-collections'] = [self.collection.pk]

        response = form.submit().follow()

        self.assertTemplateUsed(response,
            'journalmanager/sponsor_dashboard.html')
        self.assertIn('Saved.', response.body)
        self.assertIn('Funda\xc3\xa7\xc3\xa3o de Amparo a Pesquisa do Estado de S\xc3\xa3o Paulo', response.body)

    def test_POST_workflow_with_invalid_formdata(self):
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        form['sponsor-address'] = u'Av. Professor Lineu Prestes, 338 Cidade Universitária \
                                    Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047'
        form['sponsor-email'] = 'fapesp@scielo.org'
        form['sponsor-complement'] = ''
        form['sponsor-collections'] = [self.collection.pk]

        response = form.submit()

        self.assertTrue('alert alert-error' in response.body)
        self.assertIn('There are some errors or missing data', response.body)
        self.assertTemplateUsed(response, 'journalmanager/add_sponsor.html')

    def test_form_enctype_must_be_urlencoded(self):
        """
        Asserts that the enctype attribute of the sponsor form is
        ``application/x-www-form-urlencoded``
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        self.assertEqual(form.enctype, 'application/x-www-form-urlencoded')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the sponsor form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the sponsor form is
        ``POST``.
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        self.assertEqual(form.method.lower(), 'post')

    def test_collections_field_must_only_display_collections_the_user_is_bound(self):
        """
        Asserts that the user cannot add a sponsor to a collection
        that he is not related to.
        """
        perm_sponsor_change = _makePermission(perm='add_sponsor',
            model='sponsor', app_label='journalmanager')
        perm_sponsor_list = _makePermission(perm='list_sponsor',
            model='sponsor', app_label='journalmanager')
        self.user.user_permissions.add(perm_sponsor_change)
        self.user.user_permissions.add(perm_sponsor_list)

        another_collection = modelfactories.CollectionFactory.create()

        form = self.app.get(reverse('sponsor.add'), user=self.user).forms[1]

        self.assertRaises(ValueError,
            lambda: form.set('sponsor-collections', [another_collection.pk]))


class IssueFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory(collection=self.collection)

    def test_basic_struture(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
        perm = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user)

        page.mustcontain('number', 'cover',
                         'title-0-title',
                         'title-0-language',
                         'title-TOTAL_FORMS',
                         'title-INITIAL_FORMS',
                         'title-MAX_NUM_FORMS')

        self.assertTemplateUsed(page, 'journalmanager/add_issue.html')

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        page = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')
        page.mustcontain('not authorized to access')

    def test_POST_workflow_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the issue's dashboard and the new user must be part
        of the list.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.add_issue`` and
        ``journalmanager.list_issue``.
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

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

        self.assertIn('Saved.', response.body)
        self.assertTemplateUsed(response, 'journalmanager/issue_dashboard.html')

    def test_POST_workflow_without_volume_and_number_formdata(self):
        """
        When a user submit a issue the form must contain unless one of the
        fields Volume or Number
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        form['total_documents'] = '16'
        form.set('ctrl_vocabulary', 'decs')
        form['number'] = ''
        form['volume'] = ''
        form['editorial_standard'] = ''
        form['is_press_release'] = False
        form['publication_start_month'] = '9'
        form['publication_end_month'] = '11'
        form['publication_year'] = '2012'
        form['order'] = '201203'
        form['is_marked_up'] = False
        form['editorial_standard'] = 'other'

        response = form.submit()

        self.assertIn('You must complete at least one of two fields volume or number.', response.body)
        self.assertTemplateUsed(response, 'journalmanager/add_issue.html')

    def test_POST_workflow_with_invalid_formdata(self):
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        form['total_documents'] = '16'
        form.set('ctrl_vocabulary', 'decs')
        form['number'] = '3'
        form['editorial_standard'] = ''
        form['volume'] = ''
        form['is_press_release'] = False
        form['publication_end_month'] = '11'
        form['publication_year'] = '2012'
        form['order'] = '201203'
        form['is_marked_up'] = False
        form['editorial_standard'] = 'other'

        response = form.submit()

        self.assertTrue('alert alert-error' in response.body)
        self.assertIn('There are some errors or missing data', response.body)
        self.assertTemplateUsed(response, 'journalmanager/add_issue.html')

    def test_POST_workflow_with_exist_year_number_volume_on_the_same_journal(self):
        """
        Asserts if any message error display when try to insert a duplicate
        Year, Number and Volume issue object from a specific Journal
        """

        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        issue = modelfactories.IssueFactory(journal=self.journal)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        form['total_documents'] = '16'
        form.set('ctrl_vocabulary', 'decs')
        form['number'] = str(issue.number)
        form['volume'] = str(issue.volume)
        form['editorial_standard'] = ''
        form['is_press_release'] = False
        form['publication_start_month'] = '9'
        form['publication_end_month'] = '11'
        form['publication_year'] = str(issue.publication_year)
        form['order'] = '201203'
        form['is_marked_up'] = False
        form['editorial_standard'] = 'other'

        response = form.submit()

        self.assertTrue('alert alert-error' in response.body)
        self.assertIn('There are some errors or missing data', response.body)
        self.assertTrue('Issue with this Year and (Volume or Number) already exists for this Journal.' \
            in response.body)

        self.assertTemplateUsed(response, 'journalmanager/add_issue.html')

    def test_form_enctype_must_be_multipart_formdata(self):
        """
        Asserts that the enctype attribute of the issue form is
        ``multipart/form-data``
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.enctype, 'multipart/form-data')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the issue form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the issue form is
        ``POST``.
        """
        perm_issue_change = _makePermission(perm='add_issue',
            model='issue', app_label='journalmanager')
        perm_issue_list = _makePermission(perm='list_issue',
            model='issue', app_label='journalmanager')
        self.user.user_permissions.add(perm_issue_change)
        self.user.user_permissions.add(perm_issue_list)

        form = self.app.get(reverse('issue.add',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.method.lower(), 'post')


class StatusFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

        self.journal = modelfactories.JournalFactory(collection=self.collection)

    def test_basic_struture(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        page = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user)

        page.mustcontain('pub_status', 'pub_status_reason')
        self.assertTemplateUsed(page, 'journalmanager/edit_journal_status.html')

    def test_access_without_permission(self):
        """
        Asserts that authenticated users without the required permissions
        are unable to access the form. They must be redirected to a page
        with informations about their lack of permissions.
        """
        page = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).follow()

        self.assertTemplateUsed(page, 'accounts/unauthorized.html')
        page.mustcontain('not authorized to access')

    def test_POST_workflow_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the status page and the new status must be part
        of the list.

        In order to take this action, the user needs the following
        permissions: ``journalmanager.list_publication_events``.
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).forms[1]

        form.set('pub_status', 'deceased')
        form['pub_status_reason'] = 'Motivo 1'

        response = form.submit().follow()

        self.assertTrue('Saved.' in response.body)
        self.assertTemplateUsed(response,
            'journalmanager/edit_journal_status.html')

    def test_POST_workflow_with_invalid_formdata(self):
        """
        When an invalid form is submited, no action is taken, the
        form is rendered again and an alert is shown with the message
        ``There are some errors or missing data``.
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).forms[1]
        form.set('pub_status', 'deceased')

        response = form.submit()

        self.assertTrue('alert alert-error' in response.body)
        self.assertIn('There are some errors or missing data', response.body)
        self.assertTemplateUsed(response,
            'journalmanager/edit_journal_status.html')

    def test_form_enctype_must_be_urlencoded(self):
        """
        Asserts that the enctype attribute of the status form is
        ``application/x-www-form-urlencoded``
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.enctype, 'application/x-www-form-urlencoded')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the status form is
        empty. This is needed because the same form is used to add
        a new or edit an existing entry.
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.action, '')

    def test_form_method_must_be_post(self):
        """
        Asserts that the method attribute of the status form is
        ``POST``.
        """
        perm = _makePermission(perm='list_publication_events',
            model='journalpublicationevents', app_label='journalmanager')
        self.user.user_permissions.add(perm)

        form = self.app.get(reverse('journal_status.edit',
            args=[self.journal.pk]), user=self.user).forms[1]

        self.assertEqual(form.method.lower(), 'post')


class SearchFormTests(WebTest):

    def setUp(self):
        self.user = auth.UserF(is_active=True)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=True)

    def test_basic_struture(self):
        """
        Just to make sure that the required hidden fields are all
        present.

        All the management fields from inlineformsets used in this
        form should be part of this test.
        """
        page = self.app.get(reverse('index'), user=self.user)

        page.mustcontain('list_model', 'q')
        self.assertTemplateUsed(page, 'journalmanager/home_journal.html')

    def test_form_enctype_must_be_urlencoded(self):
        """
        Asserts that the enctype attribute of the search form is
        ``application/x-www-form-urlencoded``
        """
        form = self.app.get(reverse('index'),
            user=self.user).forms['search-form']

        self.assertEqual(form.enctype, 'application/x-www-form-urlencoded')

    def test_form_action_must_be_empty(self):
        """
        Asserts that the action attribute of the search form is
        the journal home.
        """
        form = self.app.get(reverse('index'),
            user=self.user).forms['search-form']

        self.assertEqual(form.action, '')

    def test_form_method_must_be_get(self):
        """
        Asserts that the method attribute of the search form is
        ``GET``.
        """
        form = self.app.get(reverse('index'),
            user=self.user).forms['search-form']

        self.assertEqual(form.method.lower(), 'get')

    def test_GET_search_journal(self):
        """
        Asserts that the search return the correct journal list
        """
        perm = _makePermission(perm='list_journal', model='journal',
                app_label='journalmanager')
        self.user.user_permissions.add(perm)

        modelfactories.JournalFactory(collection=self.collection)

        page = self.app.get(reverse('journal.index') + '?q=Arquivos',
                user=self.user)

        self.assertIn('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xc3\xa3o Paulo)',
            page.body)

    def test_GET_search_sponsor(self):
        """
        Asserts that the search return the correct sponsor list
        """
        perm = _makePermission(perm='list_sponsor', model='sponsor',
                app_label='journalmanager')
        self.user.user_permissions.add(perm)

        sponsor = modelfactories.SponsorFactory.create()

        sponsor.collections.add(self.collection)

        page = self.app.get(reverse('sponsor.index') + '?q=Amparo',
                user=self.user)

        self.assertIn('Funda\xc3\xa7\xc3\xa3o de Amparo a Pesquisa do Estado de S\xc3\xa3o Paulo',
            page.body)

    def test_GET_journal_filter_by_letter(self):
        """
        Asserts that the filter with letter return the correct journal list
        """
        perm = _makePermission(perm='list_journal', model='journal',
                app_label='journalmanager')
        self.user.user_permissions.add(perm)

        modelfactories.JournalFactory(collection=self.collection)

        page = self.app.get(reverse('journal.index') + '?letter=A', user=self.user)

        self.assertIn('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (S\xc3\xa3o Paulo)',
            page.body)

    def test_GET_sponsor_filter_by_letter(self):
        """
        Asserts that the filter with letter return the correct journal list
        """
        perm = _makePermission(perm='list_sponsor', model='sponsor',
                app_label='journalmanager')
        self.user.user_permissions.add(perm)

        sponsor = modelfactories.SponsorFactory.create()

        sponsor.collections.add(self.collection)

        page = self.app.get(reverse('sponsor.index') + '?letter=F', user=self.user)

        self.assertIn('Funda\xc3\xa7\xc3\xa3o de Amparo a Pesquisa do Estado de S\xc3\xa3o Paulo',
            page.body)
