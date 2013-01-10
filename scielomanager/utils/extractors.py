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
        """
        Extracts metadata from ``/article/front/journal-meta/`` substructure.
        """
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
            front['journal-id'] = journal_meta['journal-id']['#text']

        return front

    def _extract_front_article_meta(self):
        article_meta = self._data['article']['front']['article-meta']

        front = {}

        # default-language
        if '@lang_id' in self._data['article']:
            front['default-language'] = self._data['article']['@lang_id']

        # pub-date
        if 'pub-date' in article_meta:
            pub_date = {}
            if 'month' in article_meta['pub-date']:
                pub_date['month'] = article_meta['pub-date']['month']

            if 'year' in article_meta['pub-date']:
                pub_date['year'] = article_meta['pub-date']['year']

            if 'day' in article_meta['pub-date']:
                pub_date['day'] = article_meta['pub-date']['day']

            if pub_date:
                front['pub-date'] = pub_date

        # volume
        if 'volume' in article_meta:
            front['volume'] = article_meta['volume']

        # number
        if 'number' in article_meta:
            front['number'] = article_meta['number']

        # fpage
        if 'fpage' in article_meta:
            front['fpage'] = article_meta['fpage']

        # lpage
        if 'lpage' in article_meta:
            front['lpage'] = article_meta['lpage']

        # article-ids
        if 'article-id' in article_meta:
            for art_id in article_meta['article-id']:
                id_node = front.setdefault('article-ids', {})
                id_node[art_id['@pub-id-type']] = art_id['#text']

        # subjects
        if 'article-categories' in article_meta:
            subj_node = front.setdefault('subjects', {})
            for subj in article_meta['article-categories']['subj-group']['subject']:
                wos_node = subj_node.setdefault('wos', [])
                wos_node.append(subj)

        # title-group
        if 'title-group' in article_meta:
            titlegroup_node = front.setdefault('title-group', {})
            if 'article-title' in article_meta['title-group']:
                lang_key = article_meta['title-group']['article-title']['@lang_id']
                titlegroup_node[lang_key] = article_meta['title-group']['article-title']['#text']

            if 'trans-title-group' in article_meta['title-group']:
                for title_trans in article_meta['title-group']['trans-title-group']:
                    titlegroup_node[title_trans['@lang_id']] = title_trans['trans-title']

        # contrib-group
        if 'contrib-group' in article_meta:
            if 'contrib' in article_meta['contrib-group']:
                contribgrp_node = front.setdefault('contrib-group', {})
                for contrib in article_meta['contrib-group']['contrib']:
                    contrib_node = contribgrp_node.setdefault(contrib['@contrib-type'], [])
                    contrib_data = {
                        'surname': contrib['name']['surname'],
                        'given-names': contrib['name']['given-names'],
                        'role': contrib['role'],
                        'affiliations': contrib['xref']['@rid'].split(),
                    }
                    contrib_node.append(contrib_data)

        # affiliations
        if 'aff' in article_meta:
            front['affiliations'] = self._get_affiliations()

        # abstract
        if 'abstract' in article_meta:
            abstract_node = front.setdefault('abstract', {})
            if '@lang_id' in article_meta['abstract']:
                # the abstract must be persisted as html
                abs_as_dict = article_meta['abstract'].copy()
                del(abs_as_dict['@lang_id'])

                lang_key = article_meta['abstract']['@lang_id']
                abs_text = self._schema.serialize(abs_as_dict).replace('<?xml version="1.0" encoding="utf-8"?>\n', '')
                abstract_node[lang_key] = abs_text

            for abs_trans in article_meta['trans-abstract']:
                if '@lang_id' in abs_trans:
                    # the abstract must be persisted as html
                    abs_as_dict = abs_trans.copy()
                    del(abs_as_dict['@lang_id'])

                    abs_text = self._schema.serialize(abs_as_dict).replace('<?xml version="1.0" encoding="utf-8"?>\n', '')

                    lang_key = abs_trans['@lang_id']
                    abstract_node[lang_key] = abs_text

        # keyword-group
        if 'kwd-group' in article_meta:
            keywordgroup_node = front.setdefault('keyword-group', {})
            for kwd in article_meta['kwd-group']:
                kwd_node = keywordgroup_node.setdefault(kwd['@lang_id'], [])
                kwd_node.extend(kwd['kwd'])

        return front

    def _get_affiliations(self):
        article_meta = self._data['article']['front']['article-meta']
        aff_node = []

        # handle single elements as multiple
        if isinstance(article_meta['aff'], dict):
            raw_affs = [article_meta['aff']]
        else:
            raw_affs = article_meta['aff']

        for aff in raw_affs:
            aff_data = {
                'addr-line': aff['addr-line'],
                'institution': aff['institution'],
                'country': aff['country'],
                'ref': aff['@id'],
            }
            aff_node.append(aff_data)

        return aff_node

    def get_front_meta(self):
        """
        Extracts the meaningful metadata from the given XML and returns
        a new data structure based on the spec described at:
        http://ref.scielo.org/9dm5st
        """
        data = {}
        data.update(self._extract_front_journal_meta())
        data.update(self._extract_front_article_meta())

        return data
