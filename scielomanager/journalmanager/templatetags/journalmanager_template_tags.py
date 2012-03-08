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

def full_path(context, **params):

    url_get = context['request'].GET.copy()

    url_path = context['request'].META['PATH_INFO']

    for key, value in params.items():
        url_get[key] = value

    if len(url_get):
        url_path += "?%s" % "&".join(("%s=%s" % (key, value) for key, value in url_get.items() if value))

    return url_path

class Pagination(template.Node):

    def __init__(self, object_record):
        self.object_record = template.Variable(object_record)

    def render(self, context):
        object_record = self.object_record.resolve(context)

        if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
            class_li_previous = 'disabled' if not object_record.has_previous() else ''
            class_li_next = 'disabled' if not object_record.has_next() else ''
            html_pages = []

            for page in object_record.paginator.page_range:
                class_li_page = 'active' if object_record.number == page else ''
                html_pages.append(u'<li class="{0}"><a href="{1}">{2}</a></li>'.format(class_li_page, full_path(context, page=page), page))

            html_snippet = u'''
                <div class="pagination">
                <ul>
                <li class="prev {0}"><a href="{1}">&larr; {2}</a></li>
                {3}
                <li class="next {4}"><a href="{5}">{6} &rarr;</a></li>
                </ul>
                </div>
                '''.format(
                    class_li_previous,
                    full_path(context, page=object_record.previous_page_number()),
                    _('Previous'),
                    ''.join(html_pages),
                    class_li_next,
                    full_path(context, page=object_record.next_page_number()),
                    _('Next')
                )
            return html_snippet
        else:
            return ''

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
            class_li_previous = 'disabled' if not object_record.has_previous() else ''
            class_li_next = 'disabled' if not object_record.has_next() else ''

            html_snippet = u'''
                <strong> {0}-{1} {2} {3} </strong>
                <span class="pagination"><ul>
                <li class="prev {4}">
                <a href="{5}">&larr;</a></li>
                <li class="next {6}">
                <a href="{7}">&rarr;</a></li>
                </ul></span>
                '''.format(object_record.start_index(), 
                    object_record.end_index(), _('of'),
                    object_record.paginator.count,
                    class_li_previous,
                    full_path(context, page=object_record.previous_page_number()),
                    class_li_next,
                    full_path(context, page=object_record.next_page_number()))

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



