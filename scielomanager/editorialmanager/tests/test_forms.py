#coding: utf-8

from django_webtest import WebTest
from django.core.urlresolvers import reverse

from journalmanager.tests import modelfactories
from journalmanager.tests.tests_forms import _makePermission


class RestrictedJournalFormTests(WebTest):

    def setUp(self):
        #create a group 'Editors'
        group = modelfactories.GroupFactory(name="Editors")

        #create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

        #set the user as editor of the journal
        self.journal.editor = self.user
        self.journal.save()

    def test_editor_edit_journal_with_valid_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the journal's list and the new journal must be part
        of the list.

        In order to take this action, the user needs be part of this group:
        ``superuser`` or ``editors`` or ``librarian``
        """

        use_license = modelfactories.UseLicenseFactory.create()

        form = self.app.get(reverse('editorial.journal.edit', args=[self.journal.id,]), user=self.user).forms['journal-form']

        form['journal-use_license'] = use_license.pk
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
        form['journal-is_indexed_scie'] = True
        form['journal-is_indexed_ssci'] = False
        form['journal-is_indexed_aehci'] = True

        response = form.submit().follow()

        self.assertIn('Journal updated successfully.', response.body)

        self.assertIn('ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)', response.body)

        self.assertTemplateUsed(response, 'journal/journal_list.html')


class AddUserAsEditorFormTests(WebTest):

    def setUp(self):

        perm1 = _makePermission(perm='list_editor_journal', model='journal')
        perm2 = _makePermission(perm='change_editor', model='journal')

        #create a group 'Librarian'
        group = modelfactories.GroupFactory(name="Librarian")
        group.permissions.add(perm1)
        group.permissions.add(perm2)

        #create a user and set group 'Editors'
        self.user = modelfactories.UserFactory(is_active=True)
        self.user.groups.add(group)

        self.collection = modelfactories.CollectionFactory.create()
        self.collection.add_user(self.user, is_manager=False)
        self.collection.make_default_to_user(self.user)

        self.journal = modelfactories.JournalFactory.create()
        self.journal.join(self.collection, self.user)

    def test_add_user_as_editor_formdata(self):
        """
        When a valid form is submited, the user is redirected to
        the editor area and journal have a new editor of the journal

        In order to take this action, the user needs be part of this group:
        ``superuser`` or ``librarian``
        """

        group = modelfactories.GroupFactory(name="Editors")

        #create a user with group 'Editors'
        user_editor = modelfactories.UserFactory(is_active=True)
        user_editor.groups.add(group)

        form = self.app.get(reverse('editor.add', args=[self.journal.id,]), user=self.user).forms[0]

        form['editor'] = user_editor.pk

        response = form.submit().follow()

        response.mustcontain('Successfully selected %s as editor of this Journal' % user_editor.get_full_name())








