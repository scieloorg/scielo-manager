#coding: utf-8
from django import template

register = template.Library()

@register.inclusion_tag('modal.html')
def modal(title):
    """
    Return a modal bootstrap html
    """
    return {'title': title}

@register.inclusion_tag('modal_form.html')
def modal_form(title='', modal_id='id_modal_form', form_tag_id='id_modal_form_tag'):
    """
    Return a modal bootstrap html,
    with custom code for manipulate form submition
    """
    return {
        'modal_id': modal_id,
        'title': title,
        'form_tag_id': form_tag_id,
    }
