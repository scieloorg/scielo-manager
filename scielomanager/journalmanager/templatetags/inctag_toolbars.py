from django import template

register = template.Library()


@register.inclusion_tag('journalmanager/inctag_journaldash_toolbar.html', takes_context=True)
def journaldash_toolbar(context, page, journal_id):

    perms = context['perms']

    return {'page': page, 'journal_id': journal_id, 'perms': perms}
