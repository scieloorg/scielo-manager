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
