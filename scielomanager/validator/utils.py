# coding: utf-8
import logging
import lxml
from packtools import stylechecker

logger = logging.getLogger(__name__)


class StyleCheckerAnalyzer(object):
    target_input = None
    _target_data = None
    _can_be_analyzed = (False, "Can't be analyzed")
    _can_be_analyzed_as_exception = False
    _annotations = None
    _validation_errors = None

    def __init__(self, target_input):
        if not bool(target_input):
            raise ValueError("Can't analyze, target is None or empty")
        self.target_input = target_input
        try:
            self._target_data = stylechecker.XML(self.target_input)
            self._can_be_analyzed = (True, "")
        except lxml.etree.XMLSyntaxError as e:
            self._target_data = e
            self._can_be_analyzed_as_exception = True
        except IOError as e:
            self._can_be_analyzed = (False, "IOError while starting Stylechecker.XML(), please verify if the input is correct")
        except Exception as e:
            self._can_be_analyzed = (False, "Error while starting Stylechecker.XML()")

    def analyze(self):
        results = {
            'can_be_analyzed': (False, "Can't be analyzed"),
            'annotations': None,
            'validation_errors': None,
        }
        if self._can_be_analyzed_as_exception:
            # in case of exceptions: self._target_data is the exception
            self._annotations = self._target_data.message
            self._validation_errors = self.extract_errors_from_exception(self._target_data)
            results['can_be_analyzed'] = (True, None)
        elif self._can_be_analyzed[0]:
            vs_status, vs_errors = self._target_data.validate_style()
            if not vs_status:  # have errors
                self._target_data.annotate_errors()
                self._annotations = str(self._target_data)
                self._validation_errors = self.extract_validation_errors(vs_errors)
            results['can_be_analyzed'] = (True, None)
        else:
            results['can_be_analyzed'] = self._can_be_analyzed

        results['annotations'] = self._annotations
        results['validation_errors'] = self._validation_errors
        return results

    def extract_errors_from_exception(self, exception_instance):
        """
        Return a dict with information about the syntax error exception
        """
        results = []
        error_lines = []
        if hasattr(exception_instance, 'position'):
            line, column = exception_instance.position
            error_data = {
                'line': line or '--',
                'column': column or '--',
                'message': exception_instance.message or '',
                'level': 'ERROR',
            }
            results.append(error_data)
            error_lines.append(str(line))
        return {
            'results': results,
            'error_lines': ", ".join(error_lines)
        }

    def extract_validation_errors(self, validation_errors):
        """
        Return a dict of validation errors returned by stylechecker
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


