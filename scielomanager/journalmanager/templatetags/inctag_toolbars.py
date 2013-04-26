from django import template

register = template.Library()


@register.inclusion_tag('journalmanager/inctag_journaldash_toolbar.html', takes_context=True)
def journaldash_toolbar(context, page):

    perms = context['perms']
    journal = context['journal']

    return {'page': page, 'journal': journal, 'perms': perms}
