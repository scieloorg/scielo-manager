from django import template
from django.utils.translation import ugettext as _

register = template.Library()

def get_title_for_pended(pending_item):
    try:
        title = pending_item.data.all().get(name='journal-title').value
    except:
        title = None
    return title if title else _('## This record doesn\'t have title ##')

register.simple_tag(get_title_for_pended)