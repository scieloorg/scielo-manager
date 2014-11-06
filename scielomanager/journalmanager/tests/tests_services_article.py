#coding: utf-8
import io
import copy

from lxml import isoschematron, etree
from django.test import TestCase

from journalmanager.services import article


SCH = etree.parse(article.BASIC_ARTICLE_META)


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

    def test_abbrev_journal_title(self):
        sample = u"""<article>
                       <front>
                         <journal-meta>
                           <journal-title-group>
                             <journal-title>Revista de Saude Publica</journal-title>
                             <abbrev-journal-title abbrev-type='publisher'>Rev. Saude Publica</abbrev-journal-title>
                           </journal-title-group>
                         </journal-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertTrue(self._run_validation(sample))


class ArticleMetaElementsTests(PhaseBasedTestCase):
    sch_phase = 'phase.article-meta-elements'

    def test_case1(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
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
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case3(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case4(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case5(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case6(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case7(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case8(self):
        """
        //article-meta/volume is present
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case9(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case10(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case11(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case12(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case13(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case14(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case15(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case16(self):
        """
        //article-meta/volume is present
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <volume>1</volume>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case17(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case18(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
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
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case19(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case20(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case21(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case22(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case23(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case24(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is present
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <issue>10</issue>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case25(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case26(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case27(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case28(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is present
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                             <year>2014</year>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case29(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
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
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case30(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is present
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                           </pub-date>
                           <title-group>
                             <article-title>Foobar</article-title>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case31(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is present
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                                 <surname>Bar</surname>
                               </name>
                             </contrib>
                           </contrib-group>
                         </article-meta>
                       </front>
                     </article>"""
        sample = io.BytesIO(sample.encode('utf-8'))
        self.assertFalse(self._run_validation(sample))

    def test_case32(self):
        """
        //article-meta/volume is absent
        //article-meta/issue is absent
        //article-meta/pub-date/year is absent
        //article-meta/title-group/article-title is absent
        //article-meta/contrib-group/contrib/name/surname is absent
        """
        sample = u"""<article>
                       <front>
                         <article-meta>
                           <pub-date>
                           </pub-date>
                           <title-group>
                           </title-group>
                           <contrib-group>
                             <contrib contrib-type='author'>
                               <name>
                               </name>
                             </contrib>
                           </contrib-group>
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
                     </article-meta>
                   </front>
                 </article>"""

    def test_byte_strings(self):
        self.assertRaises(TypeError, article.add_from_string, self.sample.encode('utf-8'))

    def test_unicode_strings_and_valid_xml(self):
        new_aid = article.add_from_string(self.sample)
        # aid is a 32-byte string
        self.assertTrue(len(new_aid), 32)

    def test_duplicated_articles_are_not_allowed(self):
        from django.db import IntegrityError

        new_aid = article.add_from_string(self.sample)
        self.assertTrue(new_aid)
        self.assertRaises(IntegrityError, article.add_from_string, self.sample)

    def test_xml_with_syntax_error(self):
        err_xml = u"<article></articlezzzz>"
        self.assertRaises(ValueError, article.add_from_string, err_xml)

