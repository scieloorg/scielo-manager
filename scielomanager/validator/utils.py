# coding: utf-8
import logging
import lxml
import pkg_resources
import packtools
from scielomanager.tools import get_setting_or_raise
logger = logging.getLogger(__name__)

try:
    PACKTOOLS_VERSION = pkg_resources.get_distribution('packtools').version
except pkg_resources.DistributionNotFound:
    PACKTOOLS_VERSION = None

PACKTOOLS_DEPRECATION_WARNING_VERSION = get_setting_or_raise('PACKTOOLS_DEPRECATION_WARNING_VERSION')


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


def analyze_xml(file, extra_schematron=None):
    """Analyzes `file` against packtools' XMLValidator.
    """
    result = err = None
    if extra_schematron:
        extra_sch = packtools.utils.get_schematron_from_filepath(
                extra_schematron)
        extra_sch = [extra_sch]
    else:
        extra_sch = None

    try:
        xml = packtools.XMLValidator.parse(file,
                extra_sch_schemas=extra_sch)

    except (lxml.etree.XMLSyntaxError, IOError, ValueError,
            packtools.exceptions.XMLDoctypeError) as e:
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
            'sps_version': xml.sps_version,
            'is_deprecated_version': xml.sps_version == PACKTOOLS_DEPRECATION_WARNING_VERSION,
        }

        if not status:
            err_filter = make_error_filter(lambda x: x.message)
            unique_err_list = filter(err_filter, errors)
            err_list = [(error, count(error, errors, lambda x: x.message)) for error in unique_err_list]

            result['validation_errors'] = err_list

    return result, err
