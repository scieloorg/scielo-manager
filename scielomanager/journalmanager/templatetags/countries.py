from django import template
from django_countries.fields import Country


register = template.Library()


@register.assignment_tag
def get_country_name(code):
    return Country(code=code).name

register.simple_tag(get_country_name)
