# coding:utf-8
# from django.test import TestCase
from mocker import (
    MockerTestCase,
    # ANY,
    # KWARGS,
)


class AutomataTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.Automata(*args, **kwargs)

    def test_instantiation(self):
        from export.markupfile import Automata

        dummy_journal = self.mocker.mock()
        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertIsInstance(automata, Automata)

    def test_citat_iso690(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result(u'iso690')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, u'icitat')

    def test_citat_nbr6023(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('nbr6023')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, 'acitat')

    def test_citat_other(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('other')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, 'ocitat')

    def test_citat_vancouv(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('vancouv')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, 'vcitat')

    def test_citat_apa(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('apa')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, 'pcitat')

    def test_citat_unknown_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('foo')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, '')

    def test_citat_none_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result(None)

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, '')

    def test_norma_iso690(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('iso690')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, 'iso')

    def test_norma_nbr6023(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('nbr6023')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, 'abnt')

    def test_norma_other(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('other')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, 'other')

    def test_norma_vancouv(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('vancouv')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, 'vanc')

    def test_norma_apa(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('apa')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, 'apa')

    def test_norma_unknown_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('foo')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, '')

    def test_norma_none_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result(None)

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma_acron, '')

    def test_issn_for_printed(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('print')

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.issn, '1234-1234')

    def test_issn_for_electronic(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.issn, '1234-1234')

    def test_issn_for_printed_missing_value(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('print')

        dummy_journal.print_issn
        self.mocker.result(None)

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.issn, '')

    def test_issn_for_electronic_missing_value(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        dummy_journal.eletronic_issn
        self.mocker.result(None)

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.issn, '')

    def test_acron_must_be_the_same_as_journals(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.acronym
        self.mocker.result('foo')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.acron, 'foo')

    def test_acron_must_be_lowercase(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.acronym
        self.mocker.result('FOO')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.acron, 'foo')

    def test_perfect_unicode_representation(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('print')

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        dummy_journal.editorial_standard
        self.mocker.result('nbr6023')
        self.mocker.count(2)

        dummy_journal.acronym
        self.mocker.result('foo')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(unicode(automata), '1234-1234;acitat;foo.amd;tgabnt.amd')


class IssueTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.Issue(*args, **kwargs)

    def test_legend(self):
        dummy_issue = self.mocker.mock()
        dummy_journal = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_issue.volume
        self.mocker.result('33')

        dummy_issue.identification
        self.mocker.result('3')

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)

        self.assertEqual(issue.legend, 'Star Wars v.33 n.3')

    def test_period(self):
        dummy_issue = self.mocker.mock()

        dummy_issue.publication_start_month
        self.mocker.result(3)

        dummy_issue.publication_end_month
        self.mocker.result(5)

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)
        self.assertEqual(issue.period, 'Mar/May')

    def test_order(self):
        dummy_issue = self.mocker.mock()

        dummy_issue.order
        self.mocker.result(7)

        dummy_issue.publication_year
        self.mocker.result(2012)

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)
        self.assertEqual(issue.order, '20127')

    def test_perfect_unicode_representation(self):
        dummy_issue = self.mocker.mock()
        dummy_journal = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        dummy_issue.volume
        self.mocker.result('33')

        dummy_issue.identification
        self.mocker.result('3')

        dummy_issue.publication_year
        self.mocker.result(2012)

        dummy_issue.publication_start_month
        self.mocker.result(3)

        dummy_issue.publication_end_month
        self.mocker.result(5)

        dummy_issue.order
        self.mocker.result(7)

        self.mocker.replay()

        expected_result = 'Star Wars v.33 n.3\r\nMar/May\r\n20127\r\n\r\n'

        issue = self._makeOne(dummy_issue)
        self.assertEqual(unicode(issue), expected_result)


class JournalStandardTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.JournalStandard(*args, **kwargs)

    def test_pub_type_for_print(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('print')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        pub_type = journalstd.pub_type
        self.assertEqual(pub_type, u'ppub')
        self.assertIsInstance(pub_type, unicode)

    def test_pub_type_for_electronic(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        pub_type = journalstd.pub_type
        self.assertEqual(pub_type, u'epub')
        self.assertIsInstance(pub_type, unicode)

    def test_study_area(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([dummy_study_area for i in range(5)])

        dummy_study_area.study_area
        self.mocker.result('bar')
        self.mocker.count(5)

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        expected_study_area = u'bar/bar/bar/bar/bar'
        self.assertEqual(journalstd.study_area, expected_study_area)
        self.assertIsInstance(expected_study_area, unicode)

    def test_study_area_empty_queryset(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([])

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        self.assertEqual(journalstd.study_area, '')

    def test_medline_title_is_the_journal_title(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.title
        self.mocker.result('spam')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        title = journalstd.medline_title
        self.assertEqual(title, u'spam')
        self.assertIsInstance(title, unicode)

    def test_medline_code_must_always_be_empty(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        code = journalstd.medline_code
        self.assertEqual(code, u'')
        self.assertIsInstance(code, unicode)

    def test_pissn_is_the_journal_print_issn(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        pissn = journalstd.pissn
        self.assertEqual(pissn, u'1234-1234')
        self.assertIsInstance(pissn, unicode)

    def test_pissn_is_the_journal_electronic_issn(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        eissn = journalstd.eissn
        self.assertEqual(eissn, u'1234-1234')
        self.assertIsInstance(eissn, unicode)

    def test_publisher_is_the_journal_publisher(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.publisher_name
        self.mocker.result('foo')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        publisher = journalstd.publisher
        self.assertEqual(publisher, u'foo')
        self.assertIsInstance(publisher, unicode)

    def test_title_is_the_journal_title(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_journal.title
        self.mocker.result('foo')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        title = journalstd.title
        self.assertEqual(title, u'foo')
        self.assertIsInstance(title, unicode)

    def test_journal_meta(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result(u'blitz')

        dummy_journal.editorial_standard
        self.mocker.result('apa')
        self.mocker.count(2)

        dummy_journal.scielo_issn
        self.mocker.result('electronic')
        self.mocker.count(3)

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')
        self.mocker.count(3)

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([dummy_study_area for i in range(5)])

        dummy_study_area.study_area
        self.mocker.result('bar')
        self.mocker.count(5)

        dummy_journal.title
        self.mocker.result('spam')
        self.mocker.count(2)

        dummy_journal.acronym
        self.mocker.result('foo')

        dummy_journal.print_issn
        self.mocker.result('1234-123X')

        dummy_journal.publisher_name
        self.mocker.result('fizz')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal, dummy_issue)
        journal_meta = journalstd.journal_meta
        expected_journal_meta = u"""
        1234-1234#blitz#apa#epub#1234-1234#bar/bar/bar/bar/bar#spam##spam#foo#1234-123X#1234-1234#fizz
        """.strip()
        self.assertEqual(journal_meta, expected_journal_meta)
        self.assertIsInstance(journal_meta, unicode)


class L10nIssueTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.L10nIssue(*args, **kwargs)

    def test_instantiation(self):
        from export.markupfile import L10nIssue

        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertIsInstance(l10nissue, L10nIssue)

    def test_abbrev_title(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertEqual(l10nissue.abbrev_title, u'blitz')

    def test_abbrev_title_must_return_unicode(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertIsInstance(l10nissue.abbrev_title, unicode)

    def test_short_title(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertEqual(l10nissue.short_title, u'blitz')

    def test_short_title_must_return_unicode(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertIsInstance(l10nissue.short_title, unicode)

    def test_volume(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.volume
        self.mocker.result('7')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        volume = l10nissue.volume
        self.assertEqual(volume, u'7')
        self.assertIsInstance(volume, unicode)

    def test_volume_must_return_unicode_even_when_empty(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.volume
        self.mocker.result(None)

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        volume = l10nissue.volume
        self.assertIsInstance(volume, unicode)

    def test_number(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.number
        self.mocker.result('7')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        number = l10nissue.number
        self.assertEqual(number, u'7')
        self.assertIsInstance(number, unicode)

    def test_number_must_return_unicode_even_when_empty(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.number
        self.mocker.result(None)

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        number = l10nissue.number
        self.assertIsInstance(number, unicode)

    def test_suppl_volume(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.type
        self.mocker.result('supplement')

        dummy_issue.number
        self.mocker.result('')

        dummy_issue.suppl_text
        self.mocker.result('foo')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        suppl_volume = l10nissue.suppl_volume
        self.assertEqual(suppl_volume, u'foo')
        self.assertIsInstance(suppl_volume, unicode)

    def test_suppl_number(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.type
        self.mocker.result('supplement')

        dummy_issue.number
        self.mocker.result('5')

        dummy_issue.suppl_text
        self.mocker.result('foo')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        suppl_number = l10nissue.suppl_number
        self.assertEqual(suppl_number, u'foo')
        self.assertIsInstance(suppl_number, unicode)

    def test_suppl_number_must_return_unicode_even_when_empty(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.type
        self.mocker.result('supplement')

        dummy_issue.number
        self.mocker.result('')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        suppl_number = l10nissue.suppl_number
        self.assertIsInstance(suppl_number, unicode)

    def test_date_iso(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.publication_end_month
        self.mocker.result(00)

        dummy_issue.publication_year
        self.mocker.result('foo')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        date_iso = l10nissue.date_iso
        self.assertEqual(date_iso, u'foo0000')
        self.assertIsInstance(date_iso, unicode)

    def test_date_iso_must_return_unicode_even_when_empty(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.publication_end_month
        self.mocker.result(00)

        dummy_issue.publication_year
        self.mocker.result(None)

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        date_iso = l10nissue.date_iso
        self.assertIsInstance(date_iso, unicode)

    def test_status_must_return_always_1(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')

        status = l10nissue.status
        self.assertEqual(status, u'1')
        self.assertIsInstance(status, unicode)

    def test_issue_meta(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        dummy_issue.type
        self.mocker.result('supplement')
        self.mocker.count(2)

        dummy_issue.volume
        self.mocker.result('7')

        dummy_issue.number
        self.mocker.result('4')
        self.mocker.count(3)

        dummy_issue.suppl_text
        self.mocker.result('bar')

        dummy_issue.publication_end_month
        self.mocker.result(00)

        dummy_issue.publication_year
        self.mocker.result('baz')

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        expected_issue_meta = u'blitz;7;;4;bar;baz0000;1234-1234;1'
        self.assertEqual(l10nissue.issue_meta, expected_issue_meta)

    def test_issue_meta_must_return_unicode(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.short_title
        self.mocker.result('blitz')

        dummy_issue.volume
        self.mocker.result('7')

        dummy_issue.number
        self.mocker.result('4')
        self.mocker.count(3)  # accessed by suppl_number and suppl_volume

        dummy_issue.type
        self.mocker.result('supplement')
        self.mocker.count(2)  # accessed by suppl_number and suppl_volume

        dummy_issue.suppl_text
        self.mocker.result('bar')

        dummy_issue.publication_end_month
        self.mocker.result(00)

        dummy_issue.publication_year
        self.mocker.result('baz')

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertIsInstance(l10nissue.issue_meta, unicode)

    def test_sections(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_section = self.mocker.mock()

        dummy_issue.section
        self.mocker.result(dummy_section)

        dummy_section.available(True)
        self.mocker.result(dummy_section)

        dummy_section.all()
        self.mocker.result(['sec%s' % i for i in range(5)])

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        expected_sections = u'sec0;sec1;sec2;sec3;sec4;No section title'
        sections = l10nissue.sections
        self.assertEqual(sections, expected_sections)
        self.assertIsInstance(sections, unicode)

    def test_sections_with_empty_queryset(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_section = self.mocker.mock()

        dummy_issue.section
        self.mocker.result(dummy_section)

        dummy_section.available(True)
        self.mocker.result(dummy_section)

        dummy_section.all()
        self.mocker.result([])

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        sections = l10nissue.sections
        self.assertEqual(sections, u'No section title')
        self.assertIsInstance(sections, unicode)

    def test_section_ids(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_section = self.mocker.mock()

        dummy_issue.section
        self.mocker.result(dummy_section)

        dummy_section.available(True)
        self.mocker.result(dummy_section)

        dummy_section.all()
        self.mocker.result([dummy_section for i in range(5)])

        dummy_section.actual_code
        self.mocker.result('6')
        self.mocker.count(5)

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        expected_ids = u'6;6;6;6;6;nd'
        ids = l10nissue.sections_ids
        self.assertEqual(ids, expected_ids)
        self.assertIsInstance(ids, unicode)

    def test_section_ids_with_empty_queryset(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()
        dummy_section = self.mocker.mock()

        dummy_issue.section
        self.mocker.result(dummy_section)

        dummy_section.available(True)
        self.mocker.result(dummy_section)

        dummy_section.all()
        self.mocker.result([])

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        ids = l10nissue.sections_ids
        self.assertEqual(ids, 'nd')
        self.assertIsInstance(ids, unicode)

    def test_ctrl_vocabulary_decs(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.ctrl_vocabulary
        self.mocker.result('decs')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        vocabulary = l10nissue.ctrl_vocabulary
        self.assertEqual(vocabulary, u'Health Sciences Descriptors')
        self.assertIsInstance(vocabulary, unicode)

    def test_date_iso_if_publication_end_month_is_None(self):
        dummy_journal = self.mocker.mock()
        dummy_issue = self.mocker.mock()

        dummy_issue.publication_end_month
        self.mocker.result(None)

        dummy_issue.publication_year
        self.mocker.result('2013')

        self.mocker.replay()

        l10nissue = self._makeOne(dummy_journal, dummy_issue, 'en')
        self.assertEqual(l10nissue.date_iso, u'20130000')


class AheadTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.Ahead(*args, **kwargs)

    def test_legend(self):
        dummy_journal = self.mocker.mock()
        dummy_year = self.mocker.mock()

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        self.mocker.replay()

        ahead = self._makeOne(dummy_journal, dummy_year)

        self.assertEqual(ahead.legend, 'Star Wars n.ahead')

    def test_period(self):
        dummy_journal = self.mocker.mock()
        dummy_year = self.mocker.mock()

        self.mocker.replay()

        ahead = self._makeOne(dummy_journal, dummy_year)

        self.assertEqual(ahead.period, '/')

    def test_order(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        journal = self._makeOne(dummy_journal, '2012')
        self.assertEqual(journal.order, '201250')

    def test_perfect_unicode_representation(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        self.mocker.replay()

        expected_result = 'Star Wars n.ahead\r\n/\r\n201250\r\n\r\n'

        ahead = self._makeOne(dummy_journal, '2012')
        self.assertEqual(unicode(ahead), expected_result)


class L10nAheadTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.L10nAhead(*args, **kwargs)

    def test_instantiation(self):
        from export.markupfile import L10nAhead

        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')
        self.assertIsInstance(l10nahead, L10nAhead)

    def test_short_title(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')
        self.assertEqual(l10nahead.short_title, u'blitz')

    def test_short_title_must_return_unicode(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')
        self.assertIsInstance(l10nahead.short_title, unicode)

    def test_date_iso(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')

        date_iso = l10nahead.date_iso
        self.assertEqual(date_iso, u'20120000')
        self.assertIsInstance(date_iso, unicode)

    def test_date_iso_must_return_unicode_even_when_empty(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '', 'en')

        date_iso = l10nahead.date_iso
        self.assertIsInstance(date_iso, unicode)


    def test_status_must_return_always_1(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')

        status = l10nahead.status
        self.assertEqual(status, u'1')
        self.assertIsInstance(status, unicode)

    def test_issue_meta(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result(u'blitz')

        dummy_journal.scielo_issn
        self.mocker.result(u'print')

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        l10nahead = self._makeOne(dummy_journal, '2012', 'en')
        expected_issue_meta = u'blitz;;;ahead;;20120000;1234-1234;1'
        self.assertEqual(l10nahead.ahead_meta, expected_issue_meta)

    def test_issue_meta_must_return_unicode(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result('blitz')

        dummy_journal.scielo_issn
        self.mocker.result(u'print')

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        l10nhead = self._makeOne(dummy_journal, '2012', 'en')
        self.assertIsInstance(l10nhead.ahead_meta, unicode)

    def test_sections(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        l10nhead = self._makeOne(dummy_journal, '2012', 'en')
        expected_sections = u'No section title'

        sections = l10nhead.sections
        self.assertEqual(sections, expected_sections)
        self.assertIsInstance(sections, unicode)

    def test_ctrl_vocabulary_decs(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.ctrl_vocabulary
        self.mocker.result('decs')

        self.mocker.replay()

        l10nhead = self._makeOne(dummy_journal, '2012', 'en')
        vocabulary = l10nhead.ctrl_vocabulary
        self.assertEqual(vocabulary, u'Health Sciences Descriptors')
        self.assertIsInstance(vocabulary, unicode)


class JournalStandardAheadTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from export import markupfile
        return markupfile.JournalStandardAhead(*args, **kwargs)

    def test_pub_type_for_print(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('print')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        pub_type = journalstd.pub_type
        self.assertEqual(pub_type, u'ppub')
        self.assertIsInstance(pub_type, unicode)

    def test_pub_type_for_electronic(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.scielo_issn
        self.mocker.result('electronic')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        pub_type = journalstd.pub_type
        self.assertEqual(pub_type, u'epub')
        self.assertIsInstance(pub_type, unicode)

    def test_study_area(self):
        dummy_journal = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([dummy_study_area for i in range(5)])

        dummy_study_area.study_area
        self.mocker.result('bar')
        self.mocker.count(5)

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        expected_study_area = u'bar/bar/bar/bar/bar'
        self.assertEqual(journalstd.study_area, expected_study_area)
        self.assertIsInstance(expected_study_area, unicode)

    def test_study_area_empty_queryset(self):
        dummy_journal = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([])

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        self.assertEqual(journalstd.study_area, '')

    def test_medline_title_is_the_journal_title(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.title
        self.mocker.result('spam')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        title = journalstd.medline_title
        self.assertEqual(title, u'spam')
        self.assertIsInstance(title, unicode)

    def test_medline_code_must_always_be_empty(self):
        dummy_journal = self.mocker.mock()

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        code = journalstd.medline_code
        self.assertEqual(code, u'')
        self.assertIsInstance(code, unicode)

    def test_pissn_is_the_journal_print_issn(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.print_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        pissn = journalstd.pissn
        self.assertEqual(pissn, u'1234-1234')
        self.assertIsInstance(pissn, unicode)

    def test_pissn_is_the_journal_electronic_issn(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        eissn = journalstd.eissn
        self.assertEqual(eissn, u'1234-1234')
        self.assertIsInstance(eissn, unicode)

    def test_publisher_is_the_journal_publisher(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.publisher_name
        self.mocker.result('foo')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        publisher = journalstd.publisher
        self.assertEqual(publisher, u'foo')
        self.assertIsInstance(publisher, unicode)

    def test_title_is_the_journal_title(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result(u'foo')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        title = journalstd.title
        self.assertEqual(title, u'foo')
        self.assertIsInstance(title, unicode)

    def test_journal_meta(self):
        dummy_journal = self.mocker.mock()
        dummy_study_area = self.mocker.mock()

        dummy_journal.short_title
        self.mocker.result(u'foo')
        self.mocker.count(2)

        dummy_journal.editorial_standard
        self.mocker.result('apa')
        self.mocker.count(2)

        dummy_journal.scielo_issn
        self.mocker.result('electronic')
        self.mocker.count(3)

        dummy_journal.eletronic_issn
        self.mocker.result('1234-1234')
        self.mocker.count(3)

        dummy_journal.study_areas
        self.mocker.result(dummy_study_area)

        dummy_study_area.all()
        self.mocker.result([dummy_study_area for i in range(5)])

        dummy_study_area.study_area
        self.mocker.result('bar')
        self.mocker.count(5)

        dummy_journal.title
        self.mocker.result('spam')

        dummy_journal.acronym
        self.mocker.result('foo')

        dummy_journal.print_issn
        self.mocker.result('1234-123X')

        dummy_journal.publisher_name
        self.mocker.result('fizz')

        self.mocker.replay()

        journalstd = self._makeOne(dummy_journal)
        journal_meta = journalstd.journal_meta
        expected_journal_meta = u"""
        1234-1234#foo#apa#epub#1234-1234#bar/bar/bar/bar/bar#spam##foo#foo#1234-123X#1234-1234#fizz
        """.strip()
        self.assertEqual(journal_meta, expected_journal_meta)
        self.assertIsInstance(journal_meta, unicode)
