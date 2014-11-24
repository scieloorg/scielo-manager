from django.core import mail
from django.test import TestCase

from django_factory_boy import auth
from scielomanager.tools import get_users_by_group_by_collections
from journalmanager.tests import modelfactories

class TestTools(TestCase):

    def test_get_users_by_group_by_collections_only_one_user_match(self):
        # with:
        # create librarian group and those members
        group_name = "Librarian"
        librarian_group = modelfactories.GroupFactory(name=group_name)
        librarian1 = auth.UserF(is_active=True)
        librarian2 = auth.UserF(is_active=True)

        librarian1.groups.add(librarian_group)
        librarian1.save()

        librarian2.groups.add(librarian_group)
        librarian2.save()

        # create col1. user: librarian1 belongs to it
        col1 = modelfactories.CollectionFactory.create()
        col1.add_user(librarian1)
        # create col2. without users.
        col2 = modelfactories.CollectionFactory.create()

        # when:
        users = get_users_by_group_by_collections(group_name, [col1, col2,])
        # then:
        self.assertEqual(1, len(users))
        self.assertIn(librarian1, users)
        self.assertNotIn(librarian2, users)

    def test_get_users_by_group_by_collections_diff_collections(self):
        # with:
        # create librarian group and those members
        group_name = "Librarian"
        librarian_group = modelfactories.GroupFactory(name=group_name)
        librarian1 = auth.UserF(is_active=True)
        librarian2 = auth.UserF(is_active=True)

        librarian1.groups.add(librarian_group)
        librarian1.save()

        librarian2.groups.add(librarian_group)
        librarian2.save()

        # create col1. user: librarian1 belongs to it
        col1 = modelfactories.CollectionFactory.create()
        col1.add_user(librarian1)
        # create col2. user: librarian2 belongs to it
        col2 = modelfactories.CollectionFactory.create()
        col2.add_user(librarian2)

        # when:
        users = get_users_by_group_by_collections(group_name, [col1, col2,])
        # then:
        self.assertEqual(2, len(users))
        self.assertIn(librarian1, users)
        self.assertIn(librarian2, users)


    def test_get_users_by_group_by_collections_all_users_in_one_col(self):
        # with:
        # create librarian group and those members
        group_name = "Librarian"
        librarian_group = modelfactories.GroupFactory(name=group_name)
        librarian1 = auth.UserF(is_active=True)
        librarian2 = auth.UserF(is_active=True)

        librarian1.groups.add(librarian_group)
        librarian1.save()

        librarian2.groups.add(librarian_group)
        librarian2.save()

        # create col1. user: librarian1 belongs to it
        col1 = modelfactories.CollectionFactory.create()
        col1.add_user(librarian1)
        col1.add_user(librarian2)
        # create col2.
        col2 = modelfactories.CollectionFactory.create()

        # when:
        users = get_users_by_group_by_collections(group_name, [col1, col2,])
        # then:
        self.assertEqual(2, len(users))
        self.assertIn(librarian1, users)
        self.assertIn(librarian2, users)


    def test_get_users_by_group_by_collections_NO_collections(self):
                # with:
        # create librarian group and those members
        group_name = "Librarian"
        librarian_group = modelfactories.GroupFactory(name=group_name)
        librarian1 = auth.UserF(is_active=True)
        librarian2 = auth.UserF(is_active=True)

        librarian1.groups.add(librarian_group)
        librarian1.save()

        librarian2.groups.add(librarian_group)
        librarian2.save()

        # collection list is an empty list

        # when:
        users = get_users_by_group_by_collections(group_name, [])
        # then:
        self.assertEqual(0, len(users))
        self.assertNotIn(librarian1, users)
        self.assertNotIn(librarian2, users)

    def test_user_receive_emails_by_default(self):
        # with
        user = auth.UserF(is_active=True)

        # then
        self.assertTrue(user.get_profile().email_notifications)

    def test_user_can_NOT_receive_emails(self):
        # with
        user = auth.UserF(is_active=True)
        # when
        user_profile = user.get_profile()
        user_profile.email_notifications = False
        user_profile.save()
        # then
        self.assertFalse(user_profile.email_notifications)
