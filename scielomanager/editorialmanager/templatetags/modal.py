#coding: utf-8
from django import template

register = template.Library()

@register.inclusion_tag('modal.html')
def modal(title):
    """
    Return a modal bootstrap html
    """
    return {'title': title}
