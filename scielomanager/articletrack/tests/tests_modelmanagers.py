# coding: utf-8
from django.test import TestCase
# from django_factory_boy import auth

from articletrack import (
    models,
    modelmanagers,
)

from articletrack.tests import modelfactories
from journalmanager.tests.modelfactories import UserFactory


class CheckinManagerTests(TestCase):

    def _make_user(self, *collection):
        user = UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Checkin.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.CheckinQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):

        checkin1 = modelfactories.CheckinFactory.create()
        checkin2 = modelfactories.CheckinFactory.create()

        collection1 = checkin1.journals.all()[0].collection
        collection2 = checkin2.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_user_collections():
            return user.user_collection.all()

        user_checkins = models.Checkin.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_checkins.count(), 2)
        self.assertIn(checkin1, user_checkins)
        self.assertIn(checkin2, user_checkins)

    def test_active_returns_user_objects_bound_to_the_active_context(self):

        checkin1 = modelfactories.CheckinFactory.create()
        checkin2 = modelfactories.CheckinFactory.create()

        collection1 = checkin1.journals.all()[0].collection
        collection2 = checkin2.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_checkins = models.Checkin.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_checkins.count(), 1)
        self.assertIn(checkin2, user_checkins)
