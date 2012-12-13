from porteira import porteira


class UnknownDataStructure(Exception):
    pass


class ArticleXMLDataExtractor(object):

    def __init__(self, xml, porteira_lib=porteira.Schema):
        self._raw_xml = xml
        self._schema = porteira_lib()
        self._data = self._schema.deserialize(xml)

        if not self._check_base_structure():
            raise UnknownDataStructure('the data structure is incompatible')

    def _check_base_structure(self):
        """
        Checks if ``self._data`` has the expected structure to be mined.

        ``self._data`` is the representation of the given XML in Python
        data structures.
        """
        try:
            self._data['article']['front']['journal-meta']
            self._data['article']['front']['article-meta']
        except KeyError:
            return False
        else:
            return True

    def _extract_front_journal_meta(self):
        journal_meta = self._data['article']['front']['journal-meta']

        front = {}

        # journal-title and abbrev-journal-title
        if 'journal-title-group' in journal_meta:
            if 'journal-title' in journal_meta['journal-title-group']:
                front['journal-title'] = journal_meta['journal-title-group']['journal-title']

            if 'abbrev-journal-title' in journal_meta['journal-title-group']:
                front['abbrev-journal-title'] = journal_meta['journal-title-group']['abbrev-journal-title']

        # issn
        if 'issn' in journal_meta:
            front['issn'] = journal_meta['issn']

        # publisher-name and publisher-loc
        if 'publisher' in journal_meta:
            if 'publisher-name' in journal_meta['publisher']:
                front['publisher-name'] = journal_meta['publisher']['publisher-name']

            if 'publisher-loc' in journal_meta['publisher']:
                front['publisher-loc'] = journal_meta['publisher']['publisher-loc']

        # journal-id
        if 'journal-id' in journal_meta:
            front['journal-id'] = journal_meta['journal-id']

        return front.copy()

    def get_front_meta(self):
        """
        Extracts the meaningful metadata from the given XML and returns
        a new data structure based on the spec described at:
        http://ref.scielo.org/9dm5st
        """
        data = {}
        data.update(self._extract_front_journal_meta())

        return data
