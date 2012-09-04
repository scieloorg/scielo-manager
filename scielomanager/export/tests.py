# coding:utf-8
# from django.test import TestCase
from mocker import (
    MockerTestCase,
    # ANY,
    # KWARGS,
)


class AutomataTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from scielomanager.export import markupfiles
        return markupfiles.Automata(*args, **kwargs)

    def test_instantiation(self):
        from scielomanager.export.markupfiles import Automata

        dummy_journal = self.mocker.mock()
        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertIsInstance(automata, Automata)

    def test_citat_iso690(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('iso690')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.citat, 'icitat')

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
        self.assertEqual(automata.norma, 'iso')

    def test_norma_nbr6023(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('nbr6023')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, 'abnt')

    def test_norma_other(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('other')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, 'other')

    def test_norma_vancouv(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('vancouv')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, 'vanc')

    def test_norma_apa(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('apa')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, 'apa')

    def test_norma_unknown_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result('foo')

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, '')

    def test_norma_none_value_must_return_empty_string(self):
        dummy_journal = self.mocker.mock()

        dummy_journal.editorial_standard
        self.mocker.result(None)

        self.mocker.replay()

        automata = self._makeOne(dummy_journal)
        self.assertEqual(automata.norma, '')

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
        from scielomanager.export import markupfiles
        return markupfiles.Issue(*args, **kwargs)

    def test_legend(self):
        dummy_issue = self.mocker.mock()
        dummy_journal = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        unicode(dummy_issue)
        self.mocker.result('(ep 1)')

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)
        self.assertTrue(issue.legend, 'Star Wars (ep 1)')

    def test_period(self):
        dummy_issue = self.mocker.mock()

        dummy_issue.publication_start_month
        self.mocker.result(3)

        dummy_issue.publication_end_month
        self.mocker.result(5)

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)
        self.assertTrue(issue.period, '03/05')

    def test_order(self):
        dummy_issue = self.mocker.mock()

        dummy_issue.order
        self.mocker.result(7)

        self.mocker.replay()

        issue = self._makeOne(dummy_issue)
        self.assertTrue(issue.order, '7')

    def test_perfect_unicode_representation(self):
        dummy_issue = self.mocker.mock()
        dummy_journal = self.mocker.mock()

        dummy_issue.journal
        self.mocker.result(dummy_journal)

        dummy_journal.title_iso
        self.mocker.result('Star Wars')

        unicode(dummy_issue)
        self.mocker.result('(ep 1)')

        dummy_issue.publication_start_month
        self.mocker.result(3)

        dummy_issue.publication_end_month
        self.mocker.result(5)

        dummy_issue.order
        self.mocker.result(7)

        self.mocker.replay()

        expected_result = 'Star Wars (ep 1)\r\n03/05\r\n7\r\n\r\n'

        issue = self._makeOne(dummy_issue)
        self.assertTrue(unicode(issue), expected_result)


class L10nIssueTests(MockerTestCase):
    def _makeOne(self, *args, **kwargs):
        from scielomanager.export import markupfiles
        return markupfiles.L10nIssue(*args, **kwargs)

