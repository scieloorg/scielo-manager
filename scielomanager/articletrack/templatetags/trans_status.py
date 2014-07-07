from django import template
from scielomanager.tools import asbool
register = template.Library()

dict_status = {'ok': 'success'}
label_status_translation = {'ok': 'success', 'error': 'important'}


def trans_status(status, to_label=False):
    status = status.lower()
    if asbool(to_label):
        return label_status_translation.get(status, status)
    return dict_status.get(status, status)

register.simple_tag(trans_status)
