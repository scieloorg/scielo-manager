# coding: utf-8
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
        import datetime
        user = auth.UserF(is_active=True)
        checkin = modelfactories.CheckinFactory(accepted_by=user,
            accepted_at=datetime.datetime.now())

        self.assertRaises(ValueError, lambda: checkin.accept(user))

    def test_accept_raises_ValueError_when_user_is_inactive(self):
        import datetime
        user = auth.UserF.build(is_active=False)
        checkin = modelfactories.CheckinFactory()

        self.assertRaises(ValueError, lambda: checkin.accept(user))

