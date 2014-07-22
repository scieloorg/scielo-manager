from django import template

register = template.Library()

@register.filter_function
def attr(obj, arg1):
    """
    Use in templates: 
    {% load field_attrs %}
    then, in a form field:
    {{ form.phone|attr:"style=width:143px;background-color:yellow"|attr:"size=30" }}

    """
    att, value = arg1.split("=")
    obj.field.widget.attrs[att] = value
    return obj
