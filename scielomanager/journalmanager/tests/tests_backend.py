# coding: utf-8
from django.test import TestCase
from django_factory_boy import auth

from journalmanager.tests import modelfactories
from journalmanager.backends import ModelBackend


HASH_FOR_123 = 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799'


class ModelBackendTest(TestCase):

    def setUp(self):

        self.user = auth.UserF(username='foo',
                               password=HASH_FOR_123,
                               email='foo@bar.org',
                               is_active=True)
        self.profile = modelfactories.UserProfileFactory.build(user=self.user,
            email=self.user.email).save()

    def test_right_username_and_right_password(self):
        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('foo', '123')
        self.assertEqual(auth_response, self.user)

    def test_right_username_and_wrong_password(self):
        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('foo', 'baz')
        self.assertEqual(auth_response, None)

    def test_right_email_and_right_password(self):
        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('foo@bar.org', '123')
        self.assertEqual(auth_response, self.user)

    def test_right_email_and_wrong_password(self):
        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('foo@bar.org', 'baz')
        self.assertEqual(auth_response, None)

    def test_wrong_email_and_wrong_password(self):
        mbkend = ModelBackend()

        auth_response = mbkend.authenticate('bleh@spam.org', 'baz')
        self.assertEqual(auth_response, None)
