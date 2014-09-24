#coding: utf-8

from django_webtest import WebTest
from django.core.urlresolvers import reverse

from journalmanager.tests import modelfactories


class IndexPageTests(WebTest):

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

    def test_logged_editor_access_to_index_of_editorial_manager(self):

        response = self.app.get(reverse('editorial.index'), user=self.user)

        self.assertTemplateUsed(response, 'journal/journal_list.html')

    def test_logged_editor_access_to_index_and_see_your_journals(self):

        response = self.app.get(reverse('editorial.index'), user=self.user)

        response.mustcontain(self.journal.title)

        self.assertTemplateUsed(response, 'journal/journal_list.html')
