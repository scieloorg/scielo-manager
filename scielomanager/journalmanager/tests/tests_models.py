# coding: utf-8
from django.test import TestCase

from .modelfactories import (
    IssueFactory,
)


class SectionTests(TestCase):

    def _makeOne(self):
        from .tests_assets import get_sample_section
        return get_sample_section()

    def test_section_not_being_used(self):
        section = self._makeOne()
        self.assertFalse(section.is_used())

    def test_section_bound_to_a_journal(self):
        issue = IssueFactory.create()
        section = issue.section.all()[0]

        self.assertTrue(section.is_used())
