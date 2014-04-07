# coding: utf-8
import datetime
from django.test import TestCase
from django_factory_boy import auth

from articletrack import models
from . import modelfactories


class CommentTests(TestCase):

    def test_comment_ordering(self):
        ordering = models.Comment._meta.ordering
        self.assertEqual(ordering, ['created_at'])


class TicketTests(TestCase):

    def test_ticket_ordering(self):
        ordering = models.Ticket._meta.ordering
        self.assertEqual(ordering, ['started_at'])


class CheckinTests(TestCase):
    def test_accept(self):
        checkin = modelfactories.CheckinFactory()
        self.assertIsNone(checkin.accepted_by)
        self.assertIsNone(checkin.accepted_at)

        user = auth.UserF(is_active=True)
        checkin.accept(user)

        self.assertEqual(checkin.accepted_by, user)
        self.assertIsNotNone(checkin.accepted_at)

    def test_accept_raises_ValueError_when_already_accepted(self):
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory(accepted_by=user,
                                                accepted_at=datetime.datetime.now())

        self.assertRaises(ValueError, lambda: checkin.accept(user))

    def test_accept_raises_ValueError_when_user_is_inactive(self):
        user = auth.UserF.build(is_active=False)
        checkin = modelfactories.CheckinFactory()

        self.assertRaises(ValueError, lambda: checkin.accept(user))

    def test_is_accepted_method_with_accepted_checkin(self):
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory(accepted_by=user,
                                                accepted_at=datetime.datetime.now())

        self.assertTrue(checkin.is_accepted())

    def test_is_accepted_method_without_accepted_checkin(self):
        checkin = modelfactories.CheckinFactory()
        self.assertIsNone(checkin.accepted_by)
        self.assertIsNone(checkin.accepted_at)

        self.assertFalse(checkin.is_accepted())

    def test_get_newest_checkin(self):
        user = auth.UserF(is_active=True)
        checkin1 = modelfactories.CheckinFactory()

        self.assertEqual(checkin1.get_newest_checkin,
                         checkin1.article.checkins.order_by('uploaded_at')[0])

        checkin2 = modelfactories.CheckinFactory(accepted_by=user,
                                                 accepted_at=datetime.datetime.now())
        self.assertEqual(checkin2.get_newest_checkin,
                         checkin2.article.checkins.order_by('uploaded_at')[0])

    def test_is_newest_checkin(self):
        user = auth.UserF(is_active=True)
        checkin1 = modelfactories.CheckinFactory()
        article = checkin1.article

        self.assertTrue(checkin1.is_newest_checkin)

        checkin2 = modelfactories.CheckinFactory(accepted_by=user,
                                                 accepted_at=datetime.datetime.now(),
                                                 article=article)
        self.assertTrue(checkin2.is_newest_checkin)
        self.assertFalse(checkin1.is_newest_checkin)


class ArticleTests(TestCase):

    def test_is_accepted_method_with_accepted_checkins(self):

        user = auth.UserF(is_active=True)

        article = modelfactories.ArticleFactory()
        modelfactories.CheckinFactory(accepted_by=user,
                                      accepted_at=datetime.datetime.now(),
                                      article=article)

        self.assertTrue(article.is_accepted())

    def test_is_accepted_method_without_accepted_checkins(self):
        article = modelfactories.ArticleFactory()

        modelfactories.CheckinFactory(article=article)
        modelfactories.CheckinFactory(article=article)

        self.assertFalse(article.is_accepted())
