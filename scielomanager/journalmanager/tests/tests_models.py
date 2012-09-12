# coding: utf-8
from django.test import TestCase


class SectionTests(TestCase):

    def _makeOne(self):
        from .tests_assets import get_sample_section
        return get_sample_section()

    def test_section_not_being_used(self):
        section = self._makeOne()
        self.assertFalse(section.is_used())

    def test_section_bound_to_a_journal(self):
        from .tests_assets import (
            get_sample_journal,
            get_sample_creator,
            get_sample_uselicense,
            get_sample_issue,
        )

        creator = get_sample_creator()
        creator.save()

        use_license = get_sample_uselicense()
        use_license.save()

        journal = get_sample_journal()
        journal.creator = creator
        journal.pub_status_changed_by = creator
        journal.use_license = use_license
        journal.save()

        section = self._makeOne()
        section.journal = journal
        section.save()

        issue = get_sample_issue()
        issue.journal = journal
        issue.save()
        issue.section.add(section)
        issue.save()

        self.assertTrue(section.is_used())
