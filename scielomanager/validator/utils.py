# coding: utf-8
import logging

from packtools import stylechecker

logger = logging.getLogger(__name__)

def extract_validation_errors(validation_errors):
    """
    Return a "parsed" dict of validation errors returned by stylechecker
    """
    # iterate over the errors and get the relevant data
    results = []
    error_lines = []  # only to simplify the line's highlights of prism.js plugin on template
    for error in validation_errors:
        error_data = {
            'line': error.line or '--',
            'column': error.column or '--',
            'message': error.message or '',
            'level': error.level_name or 'ERROR',
        }
        results.append(error_data)
        if error.line:
            error_lines.append(str(error.line))
    return {
        'results': results,
        'error_lines': ", ".join(error_lines)
    }


def stylechecker_analyze(data_type, data_input):
    results = {
        'can_be_analyzed': (False, ''),
        'annotations': None,
        'validation_errors': None,
    }
    try:
        xml_check = stylechecker.XML(data_input)
    except Exception as e:  # any exception means that cannot be analyzed
        results['can_be_analyzed'] = (False, "Error while starting Stylechecker.XML()")
        # logger.error('ValueError while creating: Stylechecker.XML(%s) of type: %s. Traceback: %s' % (data_input, data_type, e))
    else:
        results['can_be_analyzed'] = (True, None)
        status, errors = xml_check.validate_style()
        if not status:  # have errors
            xml_check.annotate_errors()
            results['annotations'] = str(xml_check)
            results['validation_errors'] = extract_validation_errors(errors)

    return results