# Usage:
#
# {% query_string request variables mode %}
#
# request:
# HttpRequest object
#
# variables:
# string of GET variables separed by spaces
#
# mode:
# 1. if mode is set to include_ampersand, and the result string is not empty,
#    the result string gets an ampersand at the end
# 2. if mode is set to include_ampersand, but there are no variables
#    in query string, a question mark goes to the result string
# 3. if mode is set to html_form, the result string turns to a set of
#    html hidden input fields.
# 4. or leave mode empty for the default behavior
#
# Example:
# {% query_string request "size colour" "include_ampersand" %}

from django.utils.safestring import mark_safe
from django.utils.html import escape
from django import template

register = template.Library()


def query_string(request, variables, mode):
    variable_list = variables.split(' ')
    query_string_dict = {}
    for variable in variable_list:
        value = request.GET.get(variable, '')
        if value:
            query_string_dict[variable] = escape(value)
    if query_string_dict:
        if mode == "html_form":
            query_string = ' '.join([u'<input type="hidden" name="%s" value="%s">' % (k, v) for k, v in query_string_dict.items()])
        else:
            query_string = '?' + '&amp;'.join([u'%s=%s' % (k, v) for k, v in query_string_dict.items()]).replace(' ', '%20')
            if mode == "include_ampersand":
                query_string += '&amp;'
    else:
        if mode == "include_ampersand":
            query_string = '?'
        else:
            query_string = ''
    return mark_safe(query_string)

register.simple_tag(query_string)
