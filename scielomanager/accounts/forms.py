# coding: utf-8
from django import forms
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import get_current_site
from django.utils.http import int_to_base36
from django.template import loader
from django.conf import settings

from scielomanager.tasks import send_mail


class PasswordChangeForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
    new_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))
    new_password_again = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'span3'}))


class PasswordResetForm(PasswordResetForm):
    """
    Customization of django.contrib.auth.forms:PasswordResetForm
    to send emails via celery task
    """

    def save(self, domain_override=None,
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             use_https=False, token_generator=default_token_generator,
             from_email=None, request=None):
        """
        Generates a one-use only link for resetting password and sends to the
        user.
        """
        for user in self.users_cache:
            if not domain_override:
                current_site = get_current_site(request)
                site_name = current_site.name
                domain = current_site.domain
            else:
                site_name = domain = domain_override
            c = {
                'email': user.email,
                'domain': domain,
                'site_name': site_name,
                'uid': int_to_base36(user.id),
                'user': user,
                'token': token_generator.make_token(user),
                'protocol': use_https and 'https' or 'http',
            }
            subject = loader.render_to_string(subject_template_name, c)
            # Email subject *must not* contain newlines
            subject = ''.join(subject.splitlines())
            email = loader.render_to_string(email_template_name, c)
            if settings.EMAIL_SENT_THROUGH_CELERY:
                send_mail.delay(subject, email, [user.email])
            else:
                send_mail(subject, email, [user.email])
