import packtools

# packtools.stylechecker double


class XMLValidatorDouble(packtools.XMLValidator):
    def __init__(self, file, dtd=None, no_doctype=False):
        pass

    def validate_all(self, fail_fast=False):
        return True, None

    @property
    def meta(self):
        return {
            'article_title': 'HIV/AIDS knowledge among men who have sex with men: applying the item response theory',
            'issue_year': '2014',
            'journal_title': u'Revista de Sa\xfade P\xfablica',
            'journal_pissn': '0034-8910',
            'journal_eissn': '1518-8787',
            'issue_number': '2',
            'issue_volume': '48'
        }


class XMLValidatorAnnotationsDouble(XMLValidatorDouble):
    def annotate_errors(self, fail_fast=False):
        return "some annotations in xml string"

    def validate_all(self, fail_fast=False):
        error_list = []

        class DummyError(object):
            line = 1
            column = 6
            message = u'Premature end of data in tag xml line 1, line 1, column 6'
            level_name = 'ERROR'

        for x in xrange(0,6):
            error_list.append(DummyError())

        return False, error_list
