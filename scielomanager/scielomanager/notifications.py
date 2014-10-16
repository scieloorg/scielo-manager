# coding: utf-8
import logging
from django.conf import settings
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

from . import tasks

EMAIL_DATA_BY_ACTION =  {
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
    'issue_add_no_replicated_board': {
        'subject_sufix': "Issue Board can't be replicated",
        'template_path': 'email/issue_add_no_replicated_board.txt',
    },
    'issue_add_replicated_board': {
        'subject_sufix': "Issue has a new replicated board",
        'template_path': 'email/issue_add_replicated_board.txt',
    },
}


logger = logging.getLogger(__name__)


class Message(object):
    subject = ''
    recipients = []
    template_path = ''
    body = ''

    def __init__(self, action, subject='', recipients=[], template_path=None):
        """
        @param ``action``: key of EMAIL_DATA_BY_ACTION dict, will define some message presets
        @param ``subject``: middle text of the message subject, prepended by:
            settings.EMAIL_SUBJECT_PREFIX, appended by EMAIL_DATA_BY_ACTION[action]['subject_sufix']
        @param ``recipients`` (optional), set the list of recipients of the message
        @param ``template_path`` (optional), is the path of the templated used to render the message body,
            if not provided, the template defined in EMAIL_DATA_BY_ACTION[action]['template_path'] will be used.
        """
        if not EMAIL_DATA_BY_ACTION.has_key(action):
            raise ValueError("This action: %s is not available. Please use one of this: %s " % (action, EMAIL_DATA_BY_ACTION.keys()))

        subject_sequence = [
            settings.EMAIL_SUBJECT_PREFIX,
            subject,
            EMAIL_DATA_BY_ACTION[action]['subject_sufix'],
        ]
        self.subject = ' '.join(subject_sequence)
        self.recipients = recipients

        if template_path:
            self.template_path = template_path
        else:
            self.template_path = EMAIL_DATA_BY_ACTION[action]['template_path']

    def render_body(self, context=None):
        """
        render to string the body content.
        Will include a default context, and also the @param context dict.
        The result will be in self.body
        """
        domain = Site.objects.get_current().domain
        default_context = {
            'domain': domain,
        }
        if context:
            context.update(default_context)
        else:
            context = default_context

        self.body = render_to_string(self.template_path, context)


    def set_recipients(self, *args, **kwargs):
        """
        Implement this method to update the recipients list, based in args and kwargs data.
        """
        raise NotImplementedError("Please Implement this method")

    def send_mail(self):
        """
        if self.recipients is not empty, will call task.send_mail
        """
        if self.recipients:
            return tasks.send_mail.delay(self.subject, self.body, self.recipients)
        else:
            logger.info("[Message.send_mail] Can't send a message without recipients, did you call 'set_recipients(...)'?")


class CheckinMessage(Message):

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


class TicketMessage(Message):

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


class IssueBoardMessage(Message):

    def set_recipients(self, issue):
        editor = getattr(issue.journal, 'editor', None)
        if editor:
            self.recipients = [editor,]


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

def issue_board_replica(issue, action):
    message = IssueBoardMessage(action=action,)
    message.set_recipients(issue)
    extra_context = {'issue': issue,}
    message.render_body(extra_context)
    return message.send_mail()
