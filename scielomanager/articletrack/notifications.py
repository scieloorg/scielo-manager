# coding: utf-8

import logging

from scielomanager import notifications


logger = logging.getLogger(__name__)


class CheckinMessage(notifications.Message):

    EMAIL_DATA_BY_ACTION = {
        'checkin_reject': {
            'subject_sufix': 'Package rejected',
            'template_path': 'email/checkin_rejected.txt',
        },
        'checkin_review': {
            'subject_sufix': 'Package reviewed',
            'template_path': 'email/checkin_reviewed.txt',
        },
        'checkin_accept': {
            'subject_sufix': 'Package accepted',
            'template_path': 'email/checkin_accepted.txt',
        },
        'checkin_send_to_pending': {
            'subject_sufix': 'Package send to pending',
            'template_path': 'email/checkin_sent_to_pending.txt',
        },
        'checkin_send_to_review': {
            'subject_sufix': 'Package sent to review',
            'template_path': 'email/checkin_sent_to_review.txt',
        },
        'checkin_send_to_checkout': {
            'subject_sufix': 'Package sent to checkout',
            'template_path': 'email/checkin_sent_to_checkout.txt',
        },
        'checkout_confirmed': {
            'subject_sufix': 'Package checkout confirmed',
            'template_path': 'email/checkout_confirmed.txt',
        },
    }

    def set_recipients(self, checkin):
        """
        Set the list of emails that will receive the message.
        In case of checkins actions, the recipients will be the members of the team that include the user: checkin.submitted_by
        and the submitter (checkin.submitted_by).
        """
        if checkin.team_members:
            send_to = set([member.email for member in checkin.team_members])
            # the submitter already belong to a related team
            self.recipients = list(send_to)
        else:
            logger.info("[CheckinMessage.set_recipients] Can't prepare a message, checkin.team_members is empty. Checkin pk == %s" % checkin.pk)


class TicketMessage(notifications.Message):

    EMAIL_DATA_BY_ACTION = {
        'ticket_add': {
            'subject_sufix': 'Ticket created',
            'template_path': 'email/ticket_created.txt',
        },
        'ticket_edit': {
            'subject_sufix': 'Ticket edited',
            'template_path': 'email/ticket_modify.txt',
        },
        'ticket_close': {
            'subject_sufix': 'Ticket closed',
            'template_path': 'email/ticket_closed.txt',
        },
        'comment_created': {
            'subject_sufix': 'New comment',
            'template_path': 'email/comment_created.txt',
        },
        'comment_edit': {
            'subject_sufix': 'Comment edited',
            'template_path': 'email/comment_modify.txt',
        },
    }

    def set_recipients(self, ticket):
        """
        Set the list of emails that will receive the message.
        In case of tickets or comments, the recipients will be:
        the each member of a team, of each checkin related with the ticket,
        and the submitter (checkin.submitted_by, already belong to a team) of each checkin,
        and the author to the ticket related.
        """
        send_to = set([ticket.author.email, ])
        for checkin in ticket.article.checkins.all():
            # the submitter already belong to a related team
            if checkin.team_members:
                send_to.update([member.email for member in checkin.team_members])
            else:
                logger.info("[TicketMessage.set_recipients] Can't prepare a message, checkin.team_members is empty. Checkin pk == %s" % checkin.pk)
        self.recipients = list(send_to)


def checkin_send_email_by_action(checkin, action):

    message = CheckinMessage(action=action, subject=checkin.package_name)
    message.set_recipients(checkin)
    extra_context = {'checkin': checkin, }
    if checkin.rejected_cause:
        extra_context['reason'] = checkin.rejected_cause
    message.render_body(extra_context)
    return message.send_mail()


def ticket_send_mail_by_action(ticket, action):

    message = TicketMessage(action=action)
    message.set_recipients(ticket)
    extra_context = {'ticket': ticket,}
    message.render_body(extra_context)
    return message.send_mail()


def comment_send_mail_by_action(comment, action):

    ticket = comment.ticket
    message = TicketMessage(action=action)
    message.set_recipients(ticket)
    extra_context = {'ticket': ticket, 'comment': comment, }
    message.render_body(extra_context)
    return message.send_mail()

