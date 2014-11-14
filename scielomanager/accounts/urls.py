# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.views.generic.base import TemplateView

from . import views
from . import forms


urlpatterns = patterns('',
    url(r'^logout/$',
        auth_views.logout,
        {'next_page': settings.LOGIN_URL},
        name='journalmanager.user_logout'),

    url(r'^login/$',
        auth_views.login,
        name='journalmanager.user_login'),

    url(r'^password/reset/$',
        auth_views.password_reset,
        {
            'template_name': 'registration/password_reset_form.html',
            'email_template_name':  'registration/password_reset_email.html',
            'post_reset_redirect': '/accounts/password/reset/done/',
            'password_reset_form': forms.PasswordResetForm,
        },
        name='registration.password_reset'),

    url(r'^password/reset/done/$',
        auth_views.password_reset_done,
        {
            'template_name': 'registration/password_reset_done.html'
        },
        name='registration.password_reset_done'),

    url(r'^password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth_views.password_reset_confirm,
        {
            'template_name': 'registration/password_reset_confirm.html',
            'post_reset_redirect': '/accounts/password/reset/complete/',
        },
        name='registration.password_reset_confirm'),

    url(r'^password/reset/complete/$',
        auth_views.password_reset_complete,
        {
            'template_name': 'registration/password_reset_complete.html',
        },
        name='registration.password_reset_complete'),

    url(r'^myaccount/$',
        views.my_account,
        name='journalmanager.my_account'),

    url(r'^myaccount/password/$',
        views.password_change,
        name='journalmanager.password_change'),

    url(r'^unauthorized/$',
        views.unauthorized,
        name='accounts.unauthorized'),
)
