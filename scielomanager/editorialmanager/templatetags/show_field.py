# coding: utf-8
from django import template

register = template.Library()


@register.inclusion_tag('inctag/field.html')
def show_field(field):
    return {'field': field}
