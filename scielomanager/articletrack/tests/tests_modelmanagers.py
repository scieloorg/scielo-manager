# coding: utf-8
from django.test import TestCase

from articletrack import (
    models,
    modelmanagers,
)

from articletrack.tests import modelfactories
from journalmanager.tests.modelfactories import UserFactory


class ArticleManagerTests(TestCase):

    def _make_user(self, *collection):
        user = UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Article.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.ArticleQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):

        article1 = modelfactories.ArticleFactory.create()
        article2 = modelfactories.ArticleFactory.create()

        collection1 = article1.journals.all()[0].collection
        collection2 = article2.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_user_collections():
            return user.user_collection.all()

        user_articles = models.Article.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_articles.count(), 2)
        self.assertIn(article1, user_articles)
        self.assertIn(article2, user_articles)

    def test_active_returns_user_objects_bound_to_the_active_context(self):

        article1 = modelfactories.ArticleFactory.create()
        article2 = modelfactories.ArticleFactory.create()

        collection1 = article1.journals.all()[0].collection
        collection2 = article2.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_articles = models.Article.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_articles.count(), 1)
        self.assertIn(article2, user_articles)


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

        collection1 = checkin1.article.journals.all()[0].collection
        collection2 = checkin2.article.journals.all()[0].collection

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

        collection1 = checkin1.article.journals.all()[0].collection
        collection2 = checkin2.article.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_checkins = models.Checkin.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_checkins.count(), 1)
        self.assertIn(checkin2, user_checkins)


class TicketManagerTests(TestCase):

    def _make_user(self, *collection):
        user = UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Ticket.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.TicketQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):

        ticket1 = modelfactories.TicketFactory.create()
        ticket2 = modelfactories.TicketFactory.create()

        collection1 = ticket1.article.journals.all()[0].collection
        collection2 = ticket2.article.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_user_collections():
            return user.user_collection.all()

        user_tickets = models.Ticket.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_tickets.count(), 2)
        self.assertIn(ticket1, user_tickets)
        self.assertIn(ticket2, user_tickets)

    def test_active_returns_user_objects_bound_to_the_active_context(self):

        ticket1 = modelfactories.TicketFactory.create()
        ticket2 = modelfactories.TicketFactory.create()

        collection1 = ticket1.article.journals.all()[0].collection
        collection2 = ticket2.article.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_tickets = models.Ticket.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_tickets.count(), 1)
        self.assertIn(ticket2, user_tickets)


class CommentManagerTests(TestCase):

    def _make_user(self, *collection):
        user = UserFactory(is_active=True)
        for coll in collection:
            coll.add_user(user, is_manager=True)

        return user

    def test_manager_base_interface(self):
        mandatory_attrs = ['all', 'active']

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(models.Comment.userobjects, attr))

    def test_queryset_base_interface(self):
        mandatory_attrs = ['all', 'active', 'available', 'unavailable']

        mm = modelmanagers.CommentQuerySet()

        for attr in mandatory_attrs:
            self.assertTrue(hasattr(mm, attr))

    def test_all_returns_user_objects_no_matter_the_active_context(self):

        comment1 = modelfactories.CommentFactory.create()
        comment2 = modelfactories.CommentFactory.create()

        collection1 = comment1.ticket.article.journals.all()[0].collection
        collection2 = comment2.ticket.article.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_user_collections():
            return user.user_collection.all()

        user_comments = models.Comment.userobjects.all(
            get_all_collections=get_user_collections)

        self.assertEqual(user_comments.count(), 2)
        self.assertIn(comment1, user_comments)
        self.assertIn(comment2, user_comments)

    def test_active_returns_user_objects_bound_to_the_active_context(self):

        comment1 = modelfactories.CommentFactory.create()
        comment2 = modelfactories.CommentFactory.create()

        collection1 = comment1.ticket.article.journals.all()[0].collection
        collection2 = comment2.ticket.article.journals.all()[0].collection

        user = self._make_user(collection1, collection2)
        collection2.make_default_to_user(user)

        def get_active_collection():
            return user.user_collection.get(usercollections__is_default=True)

        user_comments = models.Comment.userobjects.active(
            get_active_collection=get_active_collection)

        self.assertEqual(user_comments.count(), 1)
        self.assertIn(comment2, user_comments)
