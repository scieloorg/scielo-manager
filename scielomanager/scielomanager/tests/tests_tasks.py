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
        result = send_mail('Test', '<b>body of mail</b>', ['to@example.com'])

        self.assertTrue(result)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'Test')
        self.assertEqual(mail.outbox[0].body, '<b>body of mail</b>')

    def test_sending_email_for_more_than_one_address(self):
        result = send_mail('Test', 'body of mail', ['to@example.com',
                                                    'tot@example.com'])

        self.assertTrue(result)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(len(mail.outbox[0].to), 2)
        self.assertEqual(mail.outbox[0].subject, 'Test')
        self.assertEqual(mail.outbox[0].body, 'body of mail')
