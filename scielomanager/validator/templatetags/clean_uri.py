# -*- coding: utf-8 -*-
import os

from django.utils.safestring import mark_safe
from django import template

register = template.Library()

def clean_uri(text):
    if text.startswith('http'):
        return mark_safe(text)
    else:
        return mark_safe(os.path.basename(text))

register.filter('clean_uri', clean_uri)

