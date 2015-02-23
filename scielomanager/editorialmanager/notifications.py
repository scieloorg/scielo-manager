# coding: utf-8

import logging
from django.core.exceptions import ObjectDoesNotExist
from scielomanager.tools import get_users_by_group_by_collections, user_receive_emails
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
            if user_receive_emails(editor):
                self.recipients = [editor.email, ]
            else:
                logger.info("[IssueBoardMessage.set_recipients] editor (user.pk: %s) does not have a profile or decides to not receive emails." % editor.pk)
        else:
            logger.error("[IssueBoardMessage.set_recipients] Can't prepare a message, issue.journal.editor is None or empty. Issue pk == %s" % issue.pk)


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

    def set_recipients(self):
        """ emails must be sent as BCC """
        self.recipients = []

    def set_bcc_recipients(self, member):
        """ recipients must belong to the same collection as member """
        collections_of_board_member = member.board.issue.journal.collections.all()

        if collections_of_board_member:
            librarians = get_users_by_group_by_collections('Librarian', collections_of_board_member)
        else:
            logger.error("[BoardMembersMessage.set_bcc_recipients] Can't define the collection of member (pk: %s), to filter bcc_recipients" % member.pk)
            return

        if librarians:
            filtered_librarians = [librarian for librarian in librarians if user_receive_emails(librarian)]
            self.bcc_recipients = map(lambda u: u.email, filtered_librarians)
        else:
            logger.error("[BoardMembersMessage.set_bcc_recipients] Can't prepare a message, Can't retrieve a list of Librarian Users.")


def issue_board_replica(issue, action):
    message = IssueBoardMessage(action=action,)
    message.set_recipients(issue)
    extra_context = {'issue': issue,}
    message.render_body(extra_context)
    return message.send_mail()


def board_members_send_email_by_action(member, user, audit_log_msg, action):
    message = BoardMembersMessage(action=action)
    message.set_recipients()
    message.set_bcc_recipients(member)
    extra_context = {
        'user': user,
        'member': member,
        'issue': member.board.issue,
        'message': audit_log_msg,
    }
    message.render_body(extra_context)
    return message.send_mail()
