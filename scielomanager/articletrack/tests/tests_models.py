# coding: utf-8
from django.test import TestCase
from articletrack import models

class CommentTests(TestCase):

    def test_comment_ordering(self):
        ordering = models.Comment._meta.ordering
        self.assertEqual(ordering, ['date'])
