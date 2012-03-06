# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
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


class Pagination(template.Node):

    def __init__(self, object_record):
        self.object_record = template.Variable(object_record)

    def render(self, context):
        object_record = self.object_record.resolve(context)

        if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
            html_snippet = u'''<div class="pagination"><ul>'''

            class_li_previous = 'disabled' if not object_record.has_previous() else ''

            #Previous
            html_snippet += u'''<li class="prev {0}"><a href="?page={1}">&larr; {2}</a></li>
                '''.format(class_li_previous, object_record.previous_page_number(), _('Previous')) 

            #Numbers
            for page in object_record.paginator.page_range:

                class_li_page = 'active' if object_record.number == page else ''

                html_snippet += u'''<li class="{0}">
                    <a href="?page={1}">{1}</a></li>'''.format(class_li_page, page)

            #Next
            class_li_next = 'disabled' if not object_record.has_next() else ''

            html_snippet += u'''<li class="next {0}">
                <a href="?page={1}">{2} &rarr;</a></li>
                '''.format(class_li_next, object_record.next_page_number(), _('Next') )

            html_snippet += u'''</ul></div>'''

            return html_snippet
          
        else: return ''

@register.tag()
@easy_tag
def pagination(_tag_name, params):
    return Pagination(params)

class SimplePagination(template.Node):

    def __init__(self, object_record):
        self.object_record = template.Variable(object_record)

    def render(self, context):

        object_record = self.object_record.resolve(context)

        if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:

            html_snippet = u'''<strong> {0}-{1} {2} {3} </strong><span class="pagination">
                '''.format(object_record.start_index(), object_record.end_index(), _('of'), object_record.paginator.count)

            html_snippet += u'''<ul>'''

            #Previous
            class_li_previous = 'disabled' if not object_record.has_previous() else ''

            html_snippet += u'''<li class="prev {0}"><a href="?page={1}">&larr;</a></li>
                '''.format(class_li_previous, object_record.previous_page_number()) 

            #Next
            class_li_next = 'disabled' if not object_record.has_next() else ''

            html_snippet += u'''<li class="next {0}">
                <a href="?page={1}">&rarr;</a></li>
                '''.format(class_li_next, object_record.next_page_number())

            html_snippet += u'''</ul></span>'''

            return html_snippet

        else: return ''


@register.tag()
@easy_tag
def simple_pagination(_tag_name, params):
    return SimplePagination(params)

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



