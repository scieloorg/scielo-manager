# coding: utf-8

import logging

from scielomanager import notifications


logger = logging.getLogger(__name__)


class IssueBoardMessage(notifications.Message):

    EMAIL_DATA_BY_ACTION = {
        'issue_add_no_replicated_board': {
            'subject_sufix': "Issue Board can't be replicated",
            'template_path': 'email/issue_add_no_replicated_board.txt',
        },
        'issue_add_replicated_board': {
            'subject_sufix': "Issue has a new replicated board",
            'template_path': 'email/issue_add_replicated_board.txt',
        },
    }

    def set_recipients(self, issue):
        editor = getattr(issue.journal, 'editor', None)
        if editor:
            self.recipients = [editor.email, ]
        else:
            logger.info("[IssueBoardMessage.set_recipients] Can't prepare a message, issue.journal.editor is None or empty. Issue pk == %s" % issue.pk)


class BoardMembersMessage(notifications.Message):

    EMAIL_DATA_BY_ACTION = {
        'board_add_member': {
            'subject_sufix': "Member of the journal board, was added",
            'template_path': 'email/board_add_member.txt',
        },
        'board_edit_member': {
            'subject_sufix': "Member of the journal board, was edited",
            'template_path': 'email/board_edit_member.txt',
        },
        'board_delete_member': {
            'subject_sufix': "Member of the journal board, was deleted",
            'template_path': 'email/board_delete_member.txt',
        }
    }

    def set_recipients(self, member):
        from scielomanager.tools import get_users_by_group
        from django.core.exceptions import ObjectDoesNotExist
        try:
            librarians = get_users_by_group('Librarian')
            self.recipients = [user.email for user in librarians if user.email]
        except ObjectDoesNotExist:
            logger.info("[BoardMembersMessage.set_recipients] Can't prepare a message, Can't retrieve a list of Librarian Users.")


def issue_board_replica(issue, action):
    message = IssueBoardMessage(action=action,)
    message.set_recipients(issue)
    extra_context = {'issue': issue,}
    message.render_body(extra_context)
    return message.send_mail()


def board_members_send_email_by_action(member, user, message, action):
    message = BoardMembersMessage(action=action)
    message.set_recipients(member)
    extra_context = {
        'user': user,
        'member': member,
        'issue': member.board.issue,
        'message': message,
    }
    message.render_body(extra_context)
    return message.send_mail()
