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
