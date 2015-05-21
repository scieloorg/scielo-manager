# coding: utf-8
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.conf import settings
from django import template


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

def full_path(context, page_param_name='page', **params):
    
    url_path = ''
    url_get = context['request'].GET.copy()

    if 'PATH_INFO' in context['request'].META:
        url_path = context['request'].META['PATH_INFO']

    for key, value in params.items():
        if key == 'page' and page_param_name and page_param_name.lower() != 'page':
            key = page_param_name.lower()
        url_get[key] = value

    if len(url_get):
        url_path += '&' if '?' in url_get else '?'
        url_path += "%s" % "&".join(("%s=%s" % (key, value) for key, value in url_get.items() if value))

    return url_path.encode('utf8')


class NamedPagination(template.Node):

    def __init__(self, letters, selected):
        self.letters = template.Variable(letters)
        self.selected = template.Variable(selected)

    def render(self, context):
        letters = self.letters.resolve(context)
        selected = self.selected.resolve(context)

        html_snippet = '''<div class="pagination">
            <ul><li><a href="?">''' + str(__('All')) + '''</a></li>'''

        for letter in letters:
            if letter != selected:
                html_snippet += '''
                <li><a href="{0}">{1}</a></li>'''\
                    .format(full_path(context, letter=letter),letter.encode('utf8'))
            else:
                html_snippet += '''
                <li class="active"><a href="{0}">{1}</a></li>'''\
                    .format(full_path(context, letter=letter),letter.encode('utf8'))

        html_snippet += '''
            </ul></div>'''

        return html_snippet

@register.tag()
@easy_tag
def named_pagination(_tag_name, *params):
    return NamedPagination(*params)

class Pagination(template.Node):

    def __init__(self, object_record, page_param_name='page'):
        self.object_record = template.Variable(object_record)
        self.page_param_name = template.Variable(page_param_name) if page_param_name.lower() != 'page' else None

    def render(self, context):
        object_record = self.object_record.resolve(context)
        page_param_name = self.page_param_name.resolve(context) if self.page_param_name else None

        if not object_record.paginator:
            # the paginator is empty
            return ''

        if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
            class_li_previous = 'disabled' if not object_record.has_previous() else ''
            class_li_next = 'disabled' if not object_record.has_next() else ''
            html_pages = []

            for page in object_record.paginator.page_range:
                class_li_page = 'active' if object_record.number == page else ''
                html_pages.append(u'<li class="{0}"><a href="{1}">{2}</a></li>'.format(class_li_page, full_path(context, page_param_name=page_param_name, page=page), page))

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
                    full_path(context, page_param_name=page_param_name, page=object_record.previous_page_number()),
                    _('Previous'),
                    ''.join(html_pages),
                    class_li_next,
                    full_path(context, page_param_name=page_param_name, page=object_record.next_page_number()),
                    _('Next')
                )
            return html_snippet
        else:
            return ''

@register.tag()
@easy_tag
def pagination(_tag_name, params, page_param_name='page'):
    return Pagination(params, page_param_name)

class SimplePagination(template.Node):

    def __init__(self, object_record, page_param_name='page'):
        self.object_record = template.Variable(object_record)
        self.page_param_name = template.Variable(page_param_name) if page_param_name.lower() != 'page' else None

    def render(self, context):

        object_record = self.object_record.resolve(context)
        page_param_name = self.page_param_name.resolve(context) if self.page_param_name else None

        if not object_record.paginator:
            # the paginator is empty
            return ''

        if object_record.paginator.count > settings.PAGINATION__ITEMS_PER_PAGE:
            class_li_previous = 'disabled' if not object_record.has_previous() else ''
            class_li_next = 'disabled' if not object_record.has_next() else ''

            html_snippet = u'''
                <ul class="pager">
                    <li class="prev {4}">
                        <a href="{5}">&larr;</a>
                    </li>
                    <li class="middle">
                        <span>
                            <strong>{0}-{1}</strong> {2} <strong>{3}</strong>
                        </span>
                    </li>
                    <li class="next {6}">
                        <a href="{7}">&rarr;</a>
                    </li>
                </ul>
                '''.format(object_record.start_index(),
                    object_record.end_index(), _('of'),
                    object_record.paginator.count,
                    class_li_previous,
                    full_path(context, page_param_name=page_param_name, page=object_record.previous_page_number()),
                    class_li_next,
                    full_path(context, page_param_name=page_param_name, page=object_record.next_page_number()))

            return html_snippet

        else:
            return ''

@register.tag()
@easy_tag
def simple_pagination(_tag_name, params, page_param_name='page'):
    return SimplePagination(params, page_param_name)

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



