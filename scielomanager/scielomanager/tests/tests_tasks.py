from django.core import mail
from django.test import TestCase

from scielomanager.tasks import send_mail


class TestSendMailTask(TestCase):

    def test_sending_email(self):
        result = send_mail('Test', 'Body of mail', ['to@example.com'])

        self.assertTrue(result)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test')

    def test_sending_email_in_HTML(self):
        # with
        subject = 'Test'
        body = '<b>body of mail</b>'
        to_list = ['to1@example.com', 'to2@example.com']
        # when
        result = send_mail(subject, body, to_list)
        # then
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(len(email.to), len(to_list))
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, body)

    def test_sending_email_for_more_than_one_address(self):
        # with
        subject = 'Test'
        body = 'body of mail'
        to_list = ['to1@example.com', 'to2@example.com']
        bcc_list = ['bcc1@example.com', 'bcc2@example.com', 'bcc3@example.com',]
        # when
        result = send_mail(subject, body, to_list, bcc_list)

        # then
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(len(email.to), len(to_list))
        self.assertEqual(len(email.bcc), len(bcc_list))
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, body)

    def test_sending_email_for_more_than_one_address_as_BCC_only(self):
        # with
        subject = 'Test'
        body = 'body of mail'
        to_list = []
        bcc_list = ['bcc1@example.com', 'bcc2@example.com', 'bcc3@example.com',]
        # when
        result = send_mail(subject, body, to_list, bcc_list)

        # then
        self.assertTrue(result)
        self.assertEqual(len(mail.outbox), 1)
        email = mail.outbox[0]
        self.assertEqual(len(email.to), len(to_list))
        self.assertEqual(len(email.bcc), len(bcc_list))
        self.assertEqual(email.subject, subject)
        self.assertEqual(email.body, body)
