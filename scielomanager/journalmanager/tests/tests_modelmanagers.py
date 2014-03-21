# coding: utf-8
from django.test import TestCase

from journalmanager import (
    models,
    modelmanagers,
)
from journalmanager.tests import modelfactories


class JournalManagerTests(TestCase):

    def _make_user(self, *collection):
        user = modelfactories.UserFactory(is_active=True)
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

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

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

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()
        modelfactories.JournalFactory.create()

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_journals = models.Journal.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal2, user_journals)

    def test_startswith_is_based_on_title_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(title=u'ABC')
        journal2 = modelfactories.JournalFactory.create(title=u'XYZ')

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal2,
            publication_status=status2
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('ABC')

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal1, user_journals)

    def test_startswith_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(title=u'ABC')
        journal2 = modelfactories.JournalFactory.create(title=u'XYZ')

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal2,
            publication_status=status2
        )

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

        journal = modelfactories.JournalFactory.create(title=u'ABC')

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith('XYZ')

        self.assertEqual(user_journals.count(), 0)

    def test_startswith_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(title=u'7ABC')

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).startswith(7)

        self.assertEqual(user_journals.count(), 1)

    def test_simple_search_is_based_on_title_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(title=u'ABC 123')
        journal2 = modelfactories.JournalFactory.create(title=u'XYZ')

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal2,
            publication_status=status2
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('123')

        self.assertEqual(user_journals.count(), 1)
        self.assertIn(journal1, user_journals)

    def test_simple_search_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal1 = modelfactories.JournalFactory.create(title=u'ABC BAZ')
        journal2 = modelfactories.JournalFactory.create(title=u'XYZ')

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal2,
            publication_status=status2
        )

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

        journal = modelfactories.JournalFactory.create(title=u'ABC')

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search('XYZ')

        self.assertEqual(user_journals.count(), 0)

    def test_simple_search_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(title=u'7 ABC')

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).simple_search(7)

        self.assertEqual(user_journals.count(), 1)

    def test_available_returns_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(is_trashed=False)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_journals.count(), 1)

    def test_available_ignores_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(is_trashed=True)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_journals.count(), 0)

    def test_unavailable_returns_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(is_trashed=True)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_journals.count(), 1)

    def test_unavailable_ignores_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create(is_trashed=False)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_journals.count(), 0)

    def test_current(self):
        def makeStatusParty(collection, journal, status):

            return modelfactories.StatusPartyFactory.create(
                collection=collection,
                journal=journal,
                publication_status=status
            )

        user = modelfactories.UserFactory(is_active=True)

        collection1 = modelfactories.CollectionFactory.create(name="Collection1")
        collection2 = modelfactories.CollectionFactory.create(name="Collection2")        
        collection1.add_user(user, is_manager=True)
        collection2.add_user(user, is_manager=True)

        journal1 = modelfactories.JournalFactory.create(title=u'Journal 1')
        journal2 = modelfactories.JournalFactory.create(title=u'Journal 2')
        journal3 = modelfactories.JournalFactory.create(title=u'Journal 3')

        status1 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=True)

        status2 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status3 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='gostei!', last_status=False)
        status4 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', reason='gostei!', last_status=True)

        status5 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status6 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', last_status=True)

        status7 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status8 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', last_status=True)

        #Colombia
        makeStatusParty(collection1, journal1, status1)
        makeStatusParty(collection1, journal2, status2)
        makeStatusParty(collection1, journal2, status3)

        #Brasil
        makeStatusParty(collection2, journal2, status4)
        makeStatusParty(collection2, journal2, status5)
        makeStatusParty(collection2, journal2, status6)
        makeStatusParty(collection2, journal3, status7)
        makeStatusParty(collection2, journal3, status8)

        def get_user_collections():
            return user.user_collection.all()
        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).current()

        self.assertEqual(user_journals.count(), 1)

    def test_suspended(self):

        def makeStatusParty(collection, journal, status):

            return modelfactories.StatusPartyFactory.create(
                collection=collection,
                journal=journal,
                publication_status=status
            )

        user = modelfactories.UserFactory(is_active=True)

        collection1 = modelfactories.CollectionFactory.create(name="Collection1")
        collection2 = modelfactories.CollectionFactory.create(name="Collection2")        
        collection1.add_user(user, is_manager=True)
        collection2.add_user(user, is_manager=True)

        journal1 = modelfactories.JournalFactory.create(title=u'Journal 1')
        journal2 = modelfactories.JournalFactory.create(title=u'Journal 2')
        journal3 = modelfactories.JournalFactory.create(title=u'Journal 3')

        status1 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=True)

        status2 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status3 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='gostei!', last_status=False)
        status4 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', reason='gostei!', last_status=True)

        status5 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status6 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', last_status=True)

        status7 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status8 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', last_status=True)

        #Colombia
        makeStatusParty(collection1, journal1, status1)
        makeStatusParty(collection1, journal2, status2)
        makeStatusParty(collection1, journal2, status3)

        #Brasil
        makeStatusParty(collection2, journal2, status4)
        makeStatusParty(collection2, journal2, status5)
        makeStatusParty(collection2, journal2, status6)
        makeStatusParty(collection2, journal3, status7)
        makeStatusParty(collection2, journal3, status8)

        def get_user_collections():
            return user.user_collection.all()
        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).suspended()

        self.assertEqual(user_journals.count(), 2)

    def test_deceased(self):
        def makeStatusParty(collection, journal, status):

            return modelfactories.StatusPartyFactory.create(
                collection=collection,
                journal=journal,
                publication_status=status
            )

        user = modelfactories.UserFactory(is_active=True)

        collection1 = modelfactories.CollectionFactory.create(name="Collection1")
        collection2 = modelfactories.CollectionFactory.create(name="Collection2")        
        collection1.add_user(user, is_manager=True)
        collection2.add_user(user, is_manager=True)

        journal1 = modelfactories.JournalFactory.create(title=u'Journal 1')
        journal2 = modelfactories.JournalFactory.create(title=u'Journal 2')
        journal3 = modelfactories.JournalFactory.create(title=u'Journal 3')

        status1 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=True)

        status2 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status3 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='gostei!', last_status=True)

        status4 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status5 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='gostei!', last_status=False)
        status6 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', reason='não gostei!', last_status=False)
        status7 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='ta lindo de novo!', last_status=False)
        status8 = modelfactories.JournalPublicationEventsFactory.create(status=u'deceased', reason='que pena!', last_status=False)
        status9 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='eu voltei!', last_status=False)
        status10 = modelfactories.JournalPublicationEventsFactory.create(status=u'deceased', reason='ja era! .', last_status=True)

        status11 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status12 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', last_status=False)
        status13 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', last_status=False)
        status14 = modelfactories.JournalPublicationEventsFactory.create(status=u'deceased', last_status=True)

        makeStatusParty(collection1, journal1, status1)

        makeStatusParty(collection1, journal2, status2)
        makeStatusParty(collection1, journal2, status3)

        makeStatusParty(collection2, journal2, status4)
        makeStatusParty(collection2, journal2, status5)
        makeStatusParty(collection2, journal2, status6)
        makeStatusParty(collection2, journal2, status7)
        makeStatusParty(collection2, journal2, status8)
        makeStatusParty(collection2, journal2, status9)
        makeStatusParty(collection2, journal2, status10)

        makeStatusParty(collection2, journal3, status11)
        makeStatusParty(collection2, journal3, status12)
        makeStatusParty(collection2, journal3, status13)
        makeStatusParty(collection2, journal3, status14)

        def get_user_collections():
            return user.user_collection.all()
        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).deceased()

        self.assertEqual(user_journals.count(), 2)

    def test_inprogress(self):
        def makeStatusParty(collection, journal, status):

            return modelfactories.StatusPartyFactory.create(
                collection=collection,
                journal=journal,
                publication_status=status
            )

        user = modelfactories.UserFactory(is_active=True)

        collection1 = modelfactories.CollectionFactory.create(name="Collection1")
        collection2 = modelfactories.CollectionFactory.create(name="Collection2")        
        collection1.add_user(user, is_manager=True)
        collection2.add_user(user, is_manager=True)

        journal1 = modelfactories.JournalFactory.create(title=u'Journal 1')
        journal2 = modelfactories.JournalFactory.create(title=u'Journal 2')
        journal3 = modelfactories.JournalFactory.create(title=u'Journal 3')

        status1 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=True)

        status2 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status3 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', reason='gostei!', last_status=False)
        status4 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', reason='gostei!', last_status=True)

        status5 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status6 = modelfactories.JournalPublicationEventsFactory.create(status=u'current', last_status=True)

        status7 = modelfactories.JournalPublicationEventsFactory.create(status=u'inprogress', last_status=False)
        status8 = modelfactories.JournalPublicationEventsFactory.create(status=u'suspended', last_status=True)

        #Colombia
        makeStatusParty(collection1, journal1, status1)
        makeStatusParty(collection1, journal2, status2)
        makeStatusParty(collection1, journal2, status3)

        #Brasil
        makeStatusParty(collection2, journal2, status4)
        makeStatusParty(collection2, journal2, status5)
        makeStatusParty(collection2, journal2, status6)
        makeStatusParty(collection2, journal3, status7)
        makeStatusParty(collection2, journal3, status8)

        def get_user_collections():
            return user.user_collection.all()
        user_journals = models.Journal.userobjects.all(
            get_all_collections=get_user_collections).inprogress()

        self.assertEqual(user_journals.count(), 1)


class SectionManagerTests(TestCase):

    def _make_user(self, *collection):
        user = modelfactories.UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Section.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.SectionQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        section1 = modelfactories.SectionFactory.create(journal=journal1)

        journal2 = modelfactories.JournalFactory.create()
        section2 = modelfactories.SectionFactory.create(journal=journal2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_user_collections():
            return user.user_collection.all()

        user_sections = models.Section.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_sections.count(), 2)
        self.assertIn(section1, user_sections)
        self.assertIn(section2, user_sections)

    def test_active_returns_user_objects_bound_to_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        section1 = modelfactories.SectionFactory.create(journal=journal1)

        journal2 = modelfactories.JournalFactory.create()
        section2 = modelfactories.SectionFactory.create(journal=journal2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_sections = models.Section.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_sections.count(), 1)
        self.assertIn(section2, user_sections)

    def test_available_returns_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create()

        modelfactories.SectionFactory.create(
            journal=journal, is_trashed=False)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_sections = models.Section.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_sections.count(), 1)

    def test_available_ignores_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create()

        modelfactories.SectionFactory.create(
            journal=journal, is_trashed=True)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_sections = models.Section.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_sections.count(), 0)

    def test_unavailable_returns_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create()

        modelfactories.SectionFactory.create(
            journal=journal, is_trashed=True)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_sections = models.Section.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_sections.count(), 1)

    def test_unavailable_ignores_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        journal = modelfactories.JournalFactory.create()

        modelfactories.SectionFactory.create(
            journal=journal, is_trashed=False)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_user_collections():
            return user.user_collection.all()

        user_sections = models.Section.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_sections.count(), 0)


class SponsorManagerTests(TestCase):

    def _make_user(self, *collection):
        user = modelfactories.UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Sponsor.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.SponsorQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        sponsor1 = modelfactories.SponsorFactory.create()
        sponsor1.collections.add(collection1)

        sponsor2 = modelfactories.SponsorFactory.create()
        sponsor2.collections.add(collection2)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_sponsors.count(), 2)
        self.assertIn(sponsor1, user_sponsors)
        self.assertIn(sponsor2, user_sponsors)

    def test_active_returns_user_objects_bound_to_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        sponsor1 = modelfactories.SponsorFactory.create()
        sponsor1.collections.add(collection1)

        sponsor2 = modelfactories.SponsorFactory.create()
        sponsor2.collections.add(collection2)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_sponsors = models.Sponsor.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor2, user_sponsors)

    def test_startswith_is_based_on_name_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).startswith('F')

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor1, user_sponsors)

    def test_startswith_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        upper_cased = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).startswith('F')

        lower_cased = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).startswith('f')

        self.assertEqual(
            [j.pk for j in upper_cased],
            [j.pk for j in lower_cased]
        )

    def test_startswith_returns_empty_if_there_are_not_matches(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).startswith('ZAP')

        self.assertEqual(user_sponsors.count(), 0)

    def test_startswith_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'7 BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).startswith(7)

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor2, user_sponsors)

    def test_simple_search_is_based_on_name_attr(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).simple_search('FOO')

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor1, user_sponsors)

    def test_simple_search_is_case_insensitive(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        upper_cased = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).simple_search('FOO')

        lower_cased = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).simple_search('foo')

        self.assertEqual(
            [j.pk for j in upper_cased],
            [j.pk for j in lower_cased]
        )

    def test_simple_search_returns_empty_if_there_are_not_matches(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).simple_search('ZAP')

        self.assertEqual(user_sponsors.count(), 0)

    def test_simple_search_coerces_term_to_unicode(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO')
        sponsor1.collections.add(collection)

        sponsor2 = modelfactories.SponsorFactory.create(
            name=u'7 BAR')
        sponsor2.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).simple_search(7)

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor2, user_sponsors)

    def test_available_returns_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO', is_trashed=False)
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_sponsors.count(), 1)
        self.assertIn(sponsor1, user_sponsors)

    def test_available_ignores_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO', is_trashed=True)
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).available()

        self.assertEqual(user_sponsors.count(), 0)

    def test_unavailable_returns_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO', is_trashed=True)
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_sponsors.count(), 1)

    def test_unavailable_ignores_non_trashed_items(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)

        sponsor1 = modelfactories.SponsorFactory.create(
            name=u'FOO', is_trashed=False)
        sponsor1.collections.add(collection)

        def get_user_collections():
            return user.user_collection.all()

        user_sponsors = models.Sponsor.userobjects.all(
            get_all_collections=get_user_collections).unavailable()

        self.assertEqual(user_sponsors.count(), 0)


class RegularPressReleaseManagerTests(TestCase):

    def _make_user(self, *collection):
        user = modelfactories.UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.RegularPressRelease.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.RegularPressReleaseQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()

        issue1 = modelfactories.IssueFactory.create(journal=journal1)
        issue2 = modelfactories.IssueFactory.create(journal=journal2)

        pr1 = modelfactories.RegularPressReleaseFactory.create(issue=issue1)
        pr2 = modelfactories.RegularPressReleaseFactory.create(issue=issue2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_user_collections():
            return user.user_collection.all()

        user_prs = models.RegularPressRelease.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_prs.count(), 2)
        self.assertIn(pr1, user_prs)
        self.assertIn(pr2, user_prs)

    def test_active_returns_user_objects_bound_to_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()

        issue1 = modelfactories.IssueFactory.create(journal=journal1)
        issue2 = modelfactories.IssueFactory.create(journal=journal2)

        pr1 = modelfactories.RegularPressReleaseFactory.create(issue=issue1)
        pr2 = modelfactories.RegularPressReleaseFactory.create(issue=issue2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.RegularPressRelease.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr2, user_prs)

    def test_journal_accepts_journal_objects(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)
        collection.make_default_to_user(user)

        journal = modelfactories.JournalFactory.create()

        issue = modelfactories.IssueFactory.create(journal=journal)

        pr = modelfactories.RegularPressReleaseFactory.create(issue=issue)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.RegularPressRelease.userobjects.active(
            get_active_collection=get_active_collection).journal(journal)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr, user_prs)

    def test_journal_accepts_journal_pk(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)
        collection.make_default_to_user(user)

        journal = modelfactories.JournalFactory.create()

        issue = modelfactories.IssueFactory.create(journal=journal)

        pr = modelfactories.RegularPressReleaseFactory.create(issue=issue)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.RegularPressRelease.userobjects.active(
            get_active_collection=get_active_collection).journal(journal.pk)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr, user_prs)


class AheadPressReleaseManagerTests(TestCase):

    def _make_user(self, *collection):
        user = modelfactories.UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.AheadPressRelease.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.AheadPressReleaseQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()

        pr1 = modelfactories.AheadPressReleaseFactory.create(journal=journal1)
        pr2 = modelfactories.AheadPressReleaseFactory.create(journal=journal2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_user_collections():
            return user.user_collection.all()

        user_prs = models.AheadPressRelease.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_prs.count(), 2)
        self.assertIn(pr1, user_prs)
        self.assertIn(pr2, user_prs)

    def test_active_returns_user_objects_bound_to_the_active_context(self):
        collection1 = modelfactories.CollectionFactory.create()
        collection2 = modelfactories.CollectionFactory.create()

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        journal1 = modelfactories.JournalFactory.create()
        journal2 = modelfactories.JournalFactory.create()

        pr1 = modelfactories.AheadPressReleaseFactory.create(journal=journal1)
        pr2 = modelfactories.AheadPressReleaseFactory.create(journal=journal2)

        status1 = modelfactories.JournalPublicationEventsFactory.create()
        status2 = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection1,
            journal=journal1,
            publication_status=status1
        )

        modelfactories.StatusPartyFactory.create(
            collection=collection2,
            journal=journal2,
            publication_status=status2
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.AheadPressRelease.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr2, user_prs)

    def test_journal_accepts_journal_objects(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)
        collection.make_default_to_user(user)

        journal = modelfactories.JournalFactory.create()

        pr = modelfactories.AheadPressReleaseFactory.create(journal=journal)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.AheadPressRelease.userobjects.active(
            get_active_collection=get_active_collection).journal(journal)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr, user_prs)

    def test_journal_accepts_journal_pk(self):
        collection = modelfactories.CollectionFactory.create()

        user = self._make_user(collection)
        collection.make_default_to_user(user)

        journal = modelfactories.JournalFactory.create()

        pr = modelfactories.AheadPressReleaseFactory.create(journal=journal)

        status = modelfactories.JournalPublicationEventsFactory.create()

        modelfactories.StatusPartyFactory.create(
            collection=collection,
            journal=journal,
            publication_status=status
        )

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_prs = models.AheadPressRelease.userobjects.active(
            get_active_collection=get_active_collection).journal(journal.pk)

        self.assertEqual(user_prs.count(), 1)
        self.assertIn(pr, user_prs)
