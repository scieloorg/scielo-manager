# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django import template

from scielomanager import settings

register = template.Library()

GLOSSARY_URL = settings.DOCUMENTATION_BASE_URL +'/glossary.html#'


def easy_tag(func):
    """
    Deals with the repetitive parts of parsing template tags
    """
    def inner(parser, token):
        try:
            return func(*token.split_contents())
        except TypeError:
            raise template.TemplateSyntaxError('Bad arguments for tag "%s"' % token.split_contents()[0])
    inner.__name__ = func.__name__
    inner.__doc__ = inner.__doc__
    return inner


class AppendGetNode(template.Node):
    def __init__(self, params):
        self.dict_pairs = {}
        for pair in params.split(','):
            key, value = pair.split('=')
            self.dict_pairs[key] = template.Variable(value)

    def render(self, context):
        get = context['request'].GET.copy()

        for key, value in self.dict_pairs.items():
            get[key] = value.resolve(context)

        path = context['request'].META['PATH_INFO']

        if len(get):
            path += "?%s" % "&".join(["%s=%s" % (key, value) for (key, value) in get.items() if value])

        return path

@register.tag()
@easy_tag
def append_to_get(_tag_name, params):
    return AppendGetNode(params)


class FieldHelpText(template.Node):

    def __init__(self, field_name, help_text, glossary_refname):
        self.field_name = template.Variable(field_name)
        self.help_text = template.Variable(help_text)
        self.glossary_refname = glossary_refname

    def render(self, context):
        field_name = self.field_name.resolve(context)
        help_text = self.help_text.resolve(context)
        glossary_refname = self.glossary_refname

        for value in ['field_name', 'help_text', 'glossary_refname']:
            if len(locals().get(value)) < 1:
                return ''

        html_snippet = u'''
            <a class="help-text"
               target="_blank"
               rel="popover"
               data-original-title="{0} {1}"
               data-content="{2}"
               href="{3}{4}">
                <i class="icon-question-sign">&nbsp;</i>
            </a>
        '''.format(_('Help on:'),
                   field_name,
                   help_text,
                   GLOSSARY_URL,
                   glossary_refname).strip()

        return html_snippet

@register.tag()
@easy_tag
def field_help(_tag_name, *params):
    """
    Renders the help for a given field.

    Usage: {% field_help field_label help_text %}
    """
    return FieldHelpText(*params)
