from __future__ import absolute_import
import logging

from django.conf import settings
from django.core.mail import EmailMessage

from scielomanager.celery import app

logger = logging.getLogger(__name__)

@app.task
def send_mail(subject, content, to_list, html=True):
    """
    Send email to list set on ``to_list`` param.
    This tasks consider the settings.DEFAUL_FROM_EMAIL as from_mail param

    :param subject: A string as subject
    :param content: A HTML or a plain text content
    :param to_list: A list or tuple with the e-mails to send message
    :param html: Boolean to send as HTML or plain text, default is HTML

    Return the result of django.core.mail.message.EmailMessage.send
    """

    msg = EmailMessage(subject, content, settings.DEFAULT_FROM_EMAIL, to_list)

    if html:
        msg.content_subtype = 'html'

    try:
        ret = msg.send()
        logger.info("Successfully sent email message to %r.", to_list)

        return ret
    except Exception as e:
        logger.error("Failed to send email message to %r, traceback: %s",
                      (to_list, e))
