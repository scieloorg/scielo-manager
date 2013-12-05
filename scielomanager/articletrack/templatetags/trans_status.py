from django import template

register = template.Library()

dict_status = {'ok': 'success'}

def trans_status(status):
    return dict_status.get(status, status)

register.simple_tag(trans_status)
