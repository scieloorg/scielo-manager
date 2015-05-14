# coding: utf-8
import logging
import lxml
import pkg_resources
import packtools

logger = logging.getLogger(__name__)

try:
    PACKTOOLS_VERSION = pkg_resources.get_distribution('packtools').version
except pkg_resources.DistributionNotFound:
    PACKTOOLS_VERSION = None


def count(target, collection, key):
    """Total target count on collection.

    :param key: callable to get the comparison value
    """
    occurences = sum([1 for item in collection if key(item) == key(target)])
    return occurences


def make_error_filter(key):
    """Filtering function factory

    :param key: callable to get the filtering value
    """
    known_errors = set()

    def err_filter(err):
        _err = key(err)

        is_known = _err in known_errors
        if is_known is False:
            known_errors.add(_err)

        return not is_known
    return err_filter


def analyze_xml(file):
    """Analyzes `file` against packtools' XMLValidator.
    """
    result = err = None

    try:
        xml = packtools.XMLValidator(file)

    except (lxml.etree.XMLSyntaxError, IOError, ValueError) as e:
        err = e

    else:
        status, errors = xml.validate_all()
        err_xml = lxml.etree.tostring(
                    xml.annotate_errors(), pretty_print=True,
                    encoding='utf-8', xml_declaration=True)

        result = {
            'annotations': err_xml,
            'validation_errors': None,
            'meta': xml.meta,
        }

        if not status:
            err_filter = make_error_filter(lambda x: x.message)
            unique_err_list = filter(err_filter, errors)
            err_list = [(error, count(error, errors, lambda x: x.message)) for error in unique_err_list]

            result['validation_errors'] = err_list

    return result, err
