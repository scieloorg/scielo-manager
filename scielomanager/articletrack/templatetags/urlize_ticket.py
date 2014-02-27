# -*- coding: utf-8 -*-
import re
from django.utils.safestring import mark_safe
from django import template
from django.core.urlresolvers import reverse

register = template.Library()

def urlize_ticket_link(text):
    url_pattern = reverse('ticket_detail', args=['0'])
    output = re.sub(r'#(\d+)',
                  r'<a href="%s\1/">#\1</a>' % url_pattern.replace('/0', ''),
                  text)
    return mark_safe(output)

register.filter('urlize_ticket_link', urlize_ticket_link)