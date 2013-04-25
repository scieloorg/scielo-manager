# coding: utf-8
import itertools

from django import template


register = template.Library()


@register.inclusion_tag('journalmanager/inctag_stamp_regular_field.html')
def stamp_regular_field(field, show_label=True):
    """
    Prints a form field using a standardized layout.

    ``show_label`` is set to True by default, but if you
    want to suppress it, just pass ``0``.
    """
    return {'field': field, 'show_label': bool(show_label)}


@register.inclusion_tag('journalmanager/inctag_sum_errors.html')
def summarize_errors(form1,
               form2=None,
               form3=None,
               form4=None,
               form5=None,
               form6=None,
               form7=None,
               form8=None,
               form9=None,
               form10=None,
               ):
    """
    This mess with form keyword arguments is a workaround over the
    *args and **kwargs limitation of django simple_tags/inclusion_tags.
    This django limitation is solved in >=1.4. See:
    https://docs.djangoproject.com/en/1.4/releases/1.4/#args-and-kwargs-support-for-template-tag-helper-functions
    """
    forms = [f for f in [form1, form2, form3, form4, form5, form6, form7, form8, form9, form10] if f]

    field_errors = [(field for field in form if field.errors) for form in forms]
    non_field_errors = [attr() for attr in [getattr(form, 'non_field_errors', None) for form in forms] if attr]

    expanded_field_errors = list(itertools.chain(*field_errors))
    expanded_non_field_errors = list(itertools.chain(*non_field_errors))

    return {
        'show_block': bool(expanded_field_errors),
        'field_errors': expanded_field_errors,
        'non_field_errors': expanded_non_field_errors,
    }
