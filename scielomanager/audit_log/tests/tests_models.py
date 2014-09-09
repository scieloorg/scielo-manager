# coding: utf-8
from django.test import TestCase
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.utils.encoding import force_unicode
from django.forms import model_to_dict
from audit_log import models


class AuditLogEntryTests(TestCase):

    def setUp(self):
        self.dummy_user = User.objects.create(first_name='foo', last_name='bar', username='baz', email='foo@bar.org', password='123', is_active=True)
        self.dummy_content_type = ContentType.objects.get_for_model(self.dummy_user)

    def test_audit_log_entry_ordering(self):
        ordering = models.AuditLogEntry._meta.ordering
        self.assertEqual(ordering, ('-action_time',))

    def test_is_addition(self):
        # with:
        log_data = {
            'user': self.dummy_user,
            'content_type': self.dummy_content_type,
            'object_id': self.dummy_user.pk,
            'object_repr': force_unicode(self.dummy_user),
            'action_flag': models.ADDITION,
            'change_message': 'dummy user created',
            'old_values': None,
            'new_values': model_to_dict(self.dummy_user),
        }
        # when: audit the addition of a dummy user
        entry = models.AuditLogEntry.objects.create(**log_data)
        # then:
        self.assertTrue(entry.is_addition)
        self.assertFalse(entry.is_change)
        self.assertFalse(entry.is_deletion)
        self.assertEqual(entry.get_audited_object(), self.dummy_user)

    def test_is_change(self):
        # with:
        log_data = {
            'user': self.dummy_user,
            'content_type': self.dummy_content_type,
            'object_id': self.dummy_user.pk,
            'object_repr': force_unicode(self.dummy_user),
            'action_flag': models.CHANGE,
            'change_message': 'dummy user changed',
            'old_values': model_to_dict(self.dummy_user),
            'new_values': model_to_dict(self.dummy_user),
        }
        # when: audit the addition of a dummy user
        entry = models.AuditLogEntry.objects.create(**log_data)
        # then:
        self.assertTrue(entry.is_change)
        self.assertFalse(entry.is_addition)
        self.assertFalse(entry.is_deletion)
        self.assertEqual(entry.get_audited_object(), self.dummy_user)

    def test_is_deletion(self):
        # with:
        log_data = {
            'user': self.dummy_user,
            'content_type': self.dummy_content_type,
            'object_id': self.dummy_user.pk,
            'object_repr': force_unicode(self.dummy_user),
            'action_flag': models.DELETION,
            'change_message': 'dummy user deleted',
            'old_values': None,
            'new_values': None,
        }
        # when: audit the addition of a dummy user
        entry = models.AuditLogEntry.objects.create(**log_data)
        # then:
        self.assertTrue(entry.is_deletion)
        self.assertFalse(entry.is_addition)
        self.assertFalse(entry.is_change)
        self.assertEqual(entry.get_audited_object(), self.dummy_user)
