# coding: utf-8
from mocker import (
    MockerTestCase,
    ARGS,
    ANY,
    KWARGS,
)

from scielomanager.utils import extractors


class ArticleXMLDataExtractorTests(MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        return extractors.ArticleXMLDataExtractor(*args, **kwargs)

    def test_base_structure_check(self):
        porteira = self.mocker.mock()

        porteira(ARGS)
        self.mocker.result(porteira)

        porteira.deserialize(ANY)
        self.mocker.result(
            {'article': {'front': {'journal-meta': '', 'article-meta': ''}}}
        )

        self.mocker.replay()

        xml = '''
        <article>
          <front>
            <journal-meta></journal-meta>
            <article-meta></article-meta>
          </front>
        </article>'''

        extractor = self._makeOne(xml, porteira_lib=porteira)
        self.assertTrue(extractor._check_base_structure())

    def test_raises_UnknownDataStructure_for_invalid_xmls(self):
        porteira = self.mocker.mock()

        porteira(ARGS)
        self.mocker.result(porteira)

        porteira.deserialize(ANY)
        self.mocker.result(
            {'barbecue': {'front': {'journal-meta': '', 'foo-meta': ''}}}
        )

        self.mocker.replay()

        # this xml data is present only for sanity reasons, the
        # important data is returned from porteira.deserialize(ANY)
        xml = '''
        <barbecue>
          <front>
            <journal-meta></journal-meta>
            <foo-meta></foo-meta>
          </front>
        </barbecue>'''

        self.assertRaises(extractors.UnknownDataStructure,
            lambda: self._makeOne(xml, porteira_lib=porteira))

    def test_journal_meta_extraction(self):
        porteira = self.mocker.mock()

        porteira(ARGS)
        self.mocker.result(porteira)

        porteira.deserialize(ANY)
        self.mocker.result(
            {
                'article': {
                    'front': {
                        'journal-meta': {
                            'journal-title-group': {
                                'journal-title': 'FooBar',
                                'abbrev-journal-title': 'FB',
                            },
                            'issn': '0034-8910',
                            'publisher': {
                                'publisher-name': 'Baz',
                                'publisher-loc': 'Blah',
                            },
                            'journal-id': {'#text': 'xyz'},
                        },
                        'article-meta': ''
                    }
                }
            }
        )

        self.mocker.replay()

        # this xml data is present only for sanity reasons, the
        # important data is returned from porteira.deserialize(ANY)
        xml = """
        <article>
            <front>
                <journal-meta>
                    <journal-id journal-id-type="publisher">xyz</journal-id>
                    <journal-title-group>
                        <journal-title>FooBar</journal-title>
                        <abbrev-journal-title>FB</abbrev-journal-title>
                    </journal-title-group>
                    <issn>0034-8910</issn>
                    <publisher>
                        <publisher-name>Baz</publisher-name>
                        <publisher-loc>Blah</publisher-loc>
                    </publisher>
                </journal-meta>
            </front>
        </article>
        """

        expected = {
            'journal-title': 'FooBar',
            'abbrev-journal-title': 'FB',
            'issn': '0034-8910',
            'publisher-name': 'Baz',
            'publisher-loc': 'Blah',
            'journal-id': 'xyz',
        }

        extr = self._makeOne(xml, porteira_lib=porteira)
        self.assertEqual(extr._extract_front_journal_meta(), expected)

    def test_get_front_meta(self):
        import os
        import json
        here = os.path.abspath(os.path.dirname(__file__))
        extr = extractors.ArticleXMLDataExtractor(open(os.path.join(here, 'sample-article.xml')))
        expected_result = open(os.path.join(here, 'sample-article.json'))

        self.assertEqual(extr.get_front_meta(), json.load(expected_result))


class AffiliationsTests(MockerTestCase):

    def _makeOne(self, *args, **kwargs):
        return extractors.ArticleXMLDataExtractor(*args, **kwargs)

    def test_single_affiliation(self):
        xml = """
        <article>
            <front>
                <journal-meta>
                </journal-meta>
                <article-meta>
                    <aff id="A01">
                        <addr-line>São Paulo</addr-line>
                        <institution>Universidade de São Paulo</institution>
                        <country>Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        expected = {
            u'affiliations': [
                {
                    u'addr-line': u'São Paulo',
                    u'ref': u'A01',
                    u'institution': u'Universidade de São Paulo',
                    u'country': u'Brasil'
                }
            ]
        }

        extr = self._makeOne(xml)
        self.assertEqual(extr._extract_front_article_meta(), expected)

    def test_many_affiliations(self):
        xml = """
        <article>
            <front>
                <journal-meta>
                </journal-meta>
                <article-meta>
                    <aff id="A01">
                        <addr-line>São Paulo</addr-line>
                        <institution>Universidade de São Paulo</institution>
                        <country>Brasil</country>
                    </aff>
                    <aff id="A02">
                        <addr-line>São Paulo</addr-line>
                        <institution>Faculdades Metropolitanas Unidas</institution>
                        <country>Brasil</country>
                    </aff>
                </article-meta>
            </front>
        </article>
        """

        expected = {
            u'affiliations': [
                {
                    u'addr-line': u'São Paulo',
                    u'ref': u'A01',
                    u'institution': u'Universidade de São Paulo',
                    u'country': u'Brasil'
                },
                {
                    u'addr-line': u'São Paulo',
                    u'ref': u'A02',
                    u'institution': u'Faculdades Metropolitanas Unidas',
                    u'country': u'Brasil'
                }
            ]
        }

        extr = self._makeOne(xml)
        self.assertEqual(extr._extract_front_article_meta(), expected)
