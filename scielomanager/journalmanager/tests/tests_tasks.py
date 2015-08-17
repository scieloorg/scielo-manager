#coding: utf-8
import io
import copy
import unittest

from lxml import isoschematron, etree
from django.test import TestCase

from journalmanager import tasks, models
from . import modelfactories


SCH = etree.parse(tasks.BASIC_ARTICLE_META_PATH)


def TestPhase(phase_name, cache):
    """Factory of parsed Schematron phases.

    :param phase_name: the phase name
    :param cache: mapping type
    """
    if phase_name not in cache:
        phase = isoschematron.Schematron(SCH, phase=phase_name)
        cache[phase_name] = phase

    return copy.deepcopy(cache[phase_name])


class PhaseBasedTestCase(TestCase):
    cache = {}

    def _run_validation(self, sample):
        schematron = TestPhase(self.sch_phase, self.cache)
        return schematron.validate(etree.parse(sample))


class RootElementsTests(PhaseBasedTestCase):
    sch_phase = 'phase.root-elements'

    def test_case1(self):
        """
        article/front/journal-meta is present
        article/front/article-meta is present
        """
        sample = u"""<article>
                       <front>
                         <journal-meta></journal-meta>
                         <article-meta></article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        article/front/journal-meta is present
        article/front/article-meta is absent
        """
        sample = u"""<article>
                       <front>
                         <journal-meta></journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        article/front/journal-meta is absent
        article/front/article-meta is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta></article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        article/front/journal-meta is absent
        article/front/article-meta is absent
        """
        sample = u"""<article>
                       <front>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))


class JournalMetaElementsTests(PhaseBasedTestCase):
    sch_phase = 'phase.journal-meta-elements'
    def test_case1(self):
        """
        //journal-meta/journal-title-group/journal-title is present
        //journal-meta/issn[@pub-type="ppub"] is present
        //journal-meta/issn[@pub-type="epub"] is present
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                             <journal-title>Revista de Saude Publica</journal-title>
                           </journal-title-group>
                           <issn pub-type="ppub">1808-8686</issn>
                           <issn pub-type="epub">1808-8694</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        //journal-meta/journal-title-group/journal-title is present
        //journal-meta/issn[@pub-type="ppub"] is present
        //journal-meta/issn[@pub-type="epub"] is absent
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                             <journal-title>Revista de Saude Publica</journal-title>
                           </journal-title-group>
                           <issn pub-type="ppub">1808-8686</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case3(self):
        """
        //journal-meta/journal-title-group/journal-title is present
        //journal-meta/issn[@pub-type="ppub"] is absent
        //journal-meta/issn[@pub-type="epub"] is present
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                             <journal-title>Revista de Saude Publica</journal-title>
                           </journal-title-group>
                           <issn pub-type="epub">1808-8694</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case4(self):
        """
        //journal-meta/journal-title-group/journal-title is present
        //journal-meta/issn[@pub-type="ppub"] is absent
        //journal-meta/issn[@pub-type="epub"] is absent
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                             <journal-title>Revista de Saude Publica</journal-title>
                           </journal-title-group>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case5(self):
        """
        //journal-meta/journal-title-group/journal-title is absent
        //journal-meta/issn[@pub-type="ppub"] is present
        //journal-meta/issn[@pub-type="epub"] is present
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                           </journal-title-group>
                           <issn pub-type="ppub">1808-8686</issn>
                           <issn pub-type="epub">1808-8694</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case6(self):
        """
        //journal-meta/journal-title-group/journal-title is absent
        //journal-meta/issn[@pub-type="ppub"] is present
        //journal-meta/issn[@pub-type="epub"] is absent
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                           </journal-title-group>
                           <issn pub-type="ppub">1808-8686</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case7(self):
        """
        //journal-meta/journal-title-group/journal-title is absent
        //journal-meta/issn[@pub-type="ppub"] is absent
        //journal-meta/issn[@pub-type="epub"] is present
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                           </journal-title-group>
                           <issn pub-type="epub">1808-8694</issn>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case8(self):
        """
        //journal-meta/journal-title-group/journal-title is absent
        //journal-meta/issn[@pub-type="ppub"] is absent
        //journal-meta/issn[@pub-type="epub"] is absent
        """
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                           </journal-title-group>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))


class ArticleMetaElementsTests(PhaseBasedTestCase):
    sch_phase = 'phase.article-meta-elements'

    def test_case1(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/fpage is present
        //article-meta/lpage is present
        //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case1_with_elocationid(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/fpage is absent
        //article-meta/lpage is absent
        //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <elocation-id>1029k3</elocation-id>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))

    def test_case2(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>13</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case5(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case6(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case7(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case8(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case9(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case10(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case11(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>13</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case12(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case13(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case14(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case15(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                           </pub-date>
                           <fpage>10</fpage>
                           <lpage>15</lpage>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case16(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        (//article-meta/fpage and //article-meta/lpage) or //article-meta/elocation-id is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                           </pub-date>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))


class FunctionAddFromStringTests(TestCase):
    sample = u"""<article>
                   <front>
                     <journal-meta>
                       <journal-title-group>
                         <journal-title>Revista de Saude Publica</journal-title>
                         <abbrev-journal-title abbrev-type='publisher'>Rev. Saude Publica</abbrev-journal-title>
                       </journal-title-group>
                       <issn pub-type="epub">1808-8686</issn>
                     </journal-meta>
                     <article-meta>
                       <volume>1</volume>
                       <issue>10</issue>
                       <pub-date>
                         <year>2014</year>
                       </pub-date>
                       <title-group>
                         <article-title>Foobar</article-title>
                       </title-group>
                       <contrib-group>
                         <contrib contrib-type='author'>
                           <name>
                             <surname>Bar</surname>
                           </name>
                         </contrib>
                       </contrib-group>
                       <fpage>10</fpage>
                       <lpage>15</lpage>
                     </article-meta>
                   </front>
                 </article>"""

    def test_byte_strings(self):
        self.assertRaises(TypeError,
                tasks.create_article_from_string, self.sample.encode('utf-8'))

    def test_unicode_strings_and_valid_xml(self):
        new_aid = tasks.create_article_from_string(self.sample)
        # aid is a 32-byte string
        self.assertTrue(len(new_aid), 32)

    def test_duplicated_articles_are_not_allowed(self):
        from django.db import IntegrityError

        new_aid = tasks.create_article_from_string(self.sample)
        self.assertTrue(new_aid)
        self.assertRaises(IntegrityError,
                tasks.create_article_from_string, self.sample)

    def test_xml_with_syntax_error(self):
        err_xml = u"<article></articlezzzz>"
        self.assertRaises(ValueError,
                tasks.create_article_from_string, err_xml)


class LinkArticleToJournalTests(TestCase):
    def test_many_journals_without_print_issn(self):
        article = modelfactories.ArticleFactory.create()
        article.issn_ppub = ''
        article.issn_epub = '1518-8787'
        article.save()

        for _ in range(2):
            journal = modelfactories.JournalFactory.create(print_issn='')
            # o valor de `eletronic_issn` deve ser diferente para o teste ser
            # válido
            self.assertTrue(journal.eletronic_issn != article.issn_epub)

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        # não houve match.
        self.assertEquals(fresh_article.journal, None)

    def test_many_journals_without_electronic_issn(self):
        article = modelfactories.ArticleFactory.create()
        article.issn_epub = ''
        article.issn_ppub = '1518-8787'
        article.save()

        for _ in range(2):
            journal = modelfactories.JournalFactory.create(eletronic_issn='')
            # o valor de `print_issn` deve ser diferente para o teste ser
            # válido
            self.assertTrue(journal.print_issn != article.issn_ppub)

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        # não houve match.
        self.assertEquals(fresh_article.journal, None)

    def test_match_based_on_print_issn(self):
        article = modelfactories.ArticleFactory.create()
        article.issn_epub = ''
        article.issn_ppub = '1518-8787'
        article.save()

        journal = modelfactories.JournalFactory.create(print_issn='1518-8787')

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        self.assertEquals(fresh_article.journal.pk, journal.pk)

    def test_match_based_on_crossed_print_issn(self):
        """Quando issn_ppub está identificado como issn_epub
        """
        article = modelfactories.ArticleFactory.create()
        article.issn_ppub = ''
        article.issn_epub = '1518-8787'
        article.save()

        journal = modelfactories.JournalFactory.create(print_issn='1518-8787')

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        self.assertEquals(fresh_article.journal.pk, journal.pk)

    def test_match_based_on_electronic_issn(self):
        article = modelfactories.ArticleFactory.create()
        article.issn_ppub = ''
        article.issn_epub = '1518-8787'
        article.save()

        journal = modelfactories.JournalFactory.create(eletronic_issn='1518-8787')

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        self.assertEquals(fresh_article.journal.pk, journal.pk)

    def test_match_based_on_crossed_electronic_issn(self):
        """Quando issn_epub está identificado como issn_ppub
        """
        article = modelfactories.ArticleFactory.create()
        article.issn_epub = ''
        article.issn_ppub = '1518-8787'
        article.save()

        journal = modelfactories.JournalFactory.create(eletronic_issn='1518-8787')

        tasks.link_article_to_journal(article.pk)

        fresh_article = models.Article.objects.get(pk=article.pk)
        self.assertEquals(fresh_article.journal.pk, journal.pk)

