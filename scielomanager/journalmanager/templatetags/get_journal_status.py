from django import template

register = template.Library()

def get_journal_status(journal, collection):
    return journal.membership_info(collection=collection).status

register.simple_tag(get_journal_status)
