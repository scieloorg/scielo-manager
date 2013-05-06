# coding: utf-8
from django.test import TestCase
from django_factory_boy import auth

from journalmanager import (
    models,
    modelmanagers,
)
from journalmanager.tests import modelfactories


class JournalManagerTests(TestCase):

    def _make_user(self, *collection):
        user = auth.UserF(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Journal.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.JournalQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create(collection=collection1)
        journal2 = modelfactories.JournalFactory.create(collection=collection2)
        modelfactories.JournalFactory.create()

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_journals.count(), 2)
        self.assertIn(journal1, user_journals)
        self.assertIn(journal2, user_journals)

    def test_active_returns_user_objects_bound_to_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        modelfactories.JournalFactory.create(collection=collection1)
        journal2 = modelfactories.JournalFactory.create(collection=collection2)
        modelfactories.JournalFactory.create()

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_journals = models.Journal.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal2, user_journals)

    def test_startswith_is_based_on_title_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(
            title=u'ABC', collection=collection)
        journal2 = modelfactories.JournalFactory.create(
            title=u'XYZ', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('ABC')

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal1, user_journals)

    def test_startswith_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(
            title=u'ABC', collection=collection)
        journal2 = modelfactories.JournalFactory.create(
            title=u'XYZ', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        upper_cased = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('ABC')

        lower_cased = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('abc')

        self.assertEqual(
            [j.pk for j in upper_cased],
            [j.pk for j in lower_cased]
        )

    def test_startswith_returns_empty_if_there_are_not_matches(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            title=u'ABC', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('XYZ')

        self.assertEqual(user_journals.count(), 0)

    def test_startswith_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            title=u'7ABC', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith(7)

        self.assertEqual(user_journals.count(), 1)

    def test_simple_search_is_based_on_title_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(
            title=u'ABC 123', collection=collection)
        journal2 = modelfactories.JournalFactory.create(
            title=u'XYZ', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('123')

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal1, user_journals)

    def test_simple_search_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(
            title=u'ABC BAZ', collection=collection)
        journal2 = modelfactories.JournalFactory.create(
            title=u'XYZ', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        upper_cased = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('BAZ')

        lower_cased = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('baz')

        self.assertEqual(
            [j.pk for j in upper_cased],
            [j.pk for j in lower_cased]
        )

    def test_simple_search_returns_empty_if_there_are_not_matches(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            title=u'ABC', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('XYZ')

        self.assertEqual(user_journals.count(), 0)

    def test_simple_search_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            title=u'7 ABC', collection=collection)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search(7)

        self.assertEqual(user_journals.count(), 1)

    def test_available_returns_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, is_trashed=False)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_journals.count(), 1)

    def test_available_ignores_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, is_trashed=True)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_journals.count(), 0)

    def test_unavailable_returns_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, is_trashed=True)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_journals.count(), 1)

    def test_unavailable_ignores_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, is_trashed=False)

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_journals.count(), 0)

    def test_current(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, pub_status='current')

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).current()

        self.assertEqual(user_journals.count(), 1)
        for j in user_journals:
            self.assertEqual(j.pub_status, 'current')

    def test_suspended(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, pub_status='suspended')

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).suspended()

        self.assertEqual(user_journals.count(), 1)
        for j in user_journals:
            self.assertEqual(j.pub_status, 'suspended')

    def test_deceased(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, pub_status='deceased')

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).deceased()

        self.assertEqual(user_journals.count(), 1)
        for j in user_journals:
            self.assertEqual(j.pub_status, 'deceased')

    def test_inprogress(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        modelfactories.JournalFactory.create(
            collection=collection, pub_status='inprogress')

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).inprogress()

        self.assertEqual(user_journals.count(), 1)
        for j in user_journals:
            self.assertEqual(j.pub_status, 'inprogress')
