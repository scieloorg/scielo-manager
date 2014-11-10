# coding: utf-8

from editorialmanager import models
from django.test import TestCase


class RoleTypeTranslationTests(TestCase):

    def test_comment_ordering(self):
        unique_together = models.RoleTypeTranslation._meta.unique_together
        self.assertEqual(unique_together, (('role', 'language'),))
