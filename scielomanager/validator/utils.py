# coding: utf-8
import logging
import lxml
from packtools import stylechecker

logger = logging.getLogger(__name__)


class ErrorCollection(object):
    _errors = []

    def __init__(self):
        self._errors = []

    def add_object_error(self, error_obj=None, line='--', column='--', message='', level="ERROR", allow_repeted=True):
        if error_obj:
            line = getattr(error_obj, 'line', line)
            column = getattr(error_obj, 'column', column)
            message = getattr(error_obj, 'message', message)
            level = getattr(error_obj, 'level', level)

        error_data = {
            'line': line,
            'column': column,
            'message': message,
            'level': level,
        }
        if (error_data not in self._errors) or allow_repeted:
            # if error was not included yet, let's append it.
            # if error already included but allow_repeted == True, it's ok to append it again.
            self._errors.append(error_data)

    def add_exception_error(self, exception_instance, allow_repeted=True):
        message = exception_instance.message
        if hasattr(exception_instance, 'position'):
            line, column = exception_instance.position
        else:
            line, column = None, None
        self.add_object_error(error_obj=None, line=line, column=column, message=message, allow_repeted=allow_repeted)

    def add_list_of_errors(self, iterable, allow_repeted=True):
        if iterable:
            for error in iterable:
                self.add_object_error(error, allow_repeted=allow_repeted)

    def get_list(self):
        return self._errors

    def get_lines(self):
        result = []
        for error in self._errors:
            line = error['line']
            if line not in result and line > 0:
                result.append(str(line))
        return result



class StyleCheckerAnalyzer(object):
    target_input = None
    _target_data = None
    _can_be_analyzed = (False, "Can't be analyzed")
    _can_be_analyzed_as_exception = False
    _annotations = None
    _validation_errors = {'results': [], 'error_lines': [], }
    _error_collection = None

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
        self._validation_errors = {'results': [], 'error_lines': [], }
        self._error_collection = ErrorCollection()


    def get_validation_errors(self):
        """
            returns a dict like { 'results' : ... , 'error_lines': ''}
            'results' is a dict with a structure necessary to display errors table (error level, line, cols, message)
            'error_lines' is a coma separated string that list the un-repeated numbers of lines, where the XML has a error annotation
            (this list is used to highlight the line to the user with a plugin).
        """
        self._validation_errors['results'] = self._error_collection.get_list()
        lines_distinct = [str(l) for l in set(self._error_collection.get_lines())]
        self._validation_errors['error_lines'] = ", ".join(lines_distinct)
        return self._validation_errors


    def analyze(self):
        results = {
            'can_be_analyzed': (False, "Can't be analyzed"),
            'annotations': None,
            'validation_errors': None,
        }
        if self._can_be_analyzed_as_exception:
            # in case of exceptions: self._target_data is the exception
            self._annotations = self._target_data.message
            self._error_collection.add_exception_error(self._target_data, allow_repeted=False)
            results['can_be_analyzed'] = (True, None)
        elif self._can_be_analyzed[0]:
            try:
                vs_status, vs_errors = self._target_data.validate_style()
                v_status, v_errors = self._target_data.validate()
            except Exception as e:
                self._annotations = e.message
                self._error_collection.add_exception_error(e, allow_repeted=False)
                results['can_be_analyzed'] = (True, None)
            else:
                if not vs_status or not v_status:  # have errors
                    self._target_data.annotate_errors()
                    self._annotations = str(self._target_data)
                if not vs_status:
                    self._error_collection.add_list_of_errors(vs_errors)
                if not v_status:
                    self._error_collection.add_list_of_errors(v_errors)
                results['can_be_analyzed'] = (True, None)
        else:
            results['can_be_analyzed'] = self._can_be_analyzed

        results['annotations'] = self._annotations
        results['validation_errors'] = self.get_validation_errors()
        return results
