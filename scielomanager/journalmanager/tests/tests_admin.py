# coding:utf-8
"""
Use this module to write functional tests for the admin pages and
screen components, only!
"""
import unittest

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from journalmanager.admin import UserAdmin
from journalmanager.forms import UserChangeForm, UserCreationForm


class MockRequest(object):
    pass


class MockSuperUser(object):
    def has_perm(self, perm):
        return True

request = MockRequest()
request.user = MockSuperUser()


class UserAdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()

    def test_user_model_admin_requires_email_field(self):
        user_model_admin = UserAdmin(User, self.site)
        add_fieldsets = user_model_admin.add_fieldsets
        add_fiels = add_fieldsets[0][1]['fields']
        self.assertIn('email', add_fiels)

    # forms
    def test_user_model_admin_custom_change_form(self):
        user_model_admin = UserAdmin(User, self.site)
        form = user_model_admin.form()
        self.assertEqual(type(form), UserChangeForm)

    def test_user_model_admin_custom_add_form(self):
        user_model_admin = UserAdmin(User, self.site)
        form = user_model_admin.add_form()
        self.assertEqual(type(form), UserCreationForm)

    # fields
    def test_change_form_email_field_is_required(self):
        user_model_admin = UserAdmin(User, self.site)
        form = user_model_admin.form()
        field = form.declared_fields['email']
        self.assertTrue(field.required)

    def test_add_form_email_field_is_required(self):
        user_model_admin = UserAdmin(User, self.site)
        form = user_model_admin.add_form()
        field = form.declared_fields['email']
        self.assertTrue(field.required)
