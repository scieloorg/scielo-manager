from django import template

register = template.Library()


@register.inclusion_tag('journalmanager/inctag_journaldash_toolbar.html', takes_context=True)
def journaldash_toolbar(context, page, journal, user):

    ret = {'page': page}

    # Checking if journal was alread created, in some cases like adding a new journal the
    # journal attribute represents a empty journal instance.
    if journal.id:
        perms = context['perms']
        is_editor = journal.is_editor(user)
        ret.update({'journal_id': journal.id, 'is_editor': is_editor, 'perms': perms})

    return ret
