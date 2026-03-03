# -*- encoding: utf-8 -*-
from django.urls import re_path
from django.contrib.auth import views as auth_views
from django.conf import settings

from . import views
from . import forms


urlpatterns = [
    re_path(
        r'^logout/$',
        auth_views.LogoutView.as_view(next_page=settings.LOGIN_URL),
        name='journalmanager.user_logout',
    ),
    re_path(
        r'^login/$',
        auth_views.LoginView.as_view(),
        name='journalmanager.user_login',
    ),
    re_path(
        r'^password/reset/$',
        auth_views.PasswordResetView.as_view(
            template_name='registration/password_reset_form.html',
            email_template_name='registration/password_reset_email.html',
            success_url='/accounts/password/reset/done/',
            form_class=forms.PasswordResetForm,
        ),
        name='registration.password_reset',
    ),
    re_path(
        r'^password/reset/done/$',
        auth_views.PasswordResetDoneView.as_view(
            template_name='registration/password_reset_done.html',
        ),
        name='registration.password_reset_done',
    ),
    re_path(
        r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='registration/password_reset_confirm.html',
            success_url='/accounts/password/reset/complete/',
        ),
        name='registration.password_reset_confirm',
    ),
    re_path(
        r'^password/reset/complete/$',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='registration/password_reset_complete.html',
        ),
        name='registration.password_reset_complete',
    ),
    re_path(
        r'^myaccount/$',
        views.my_account,
        name='journalmanager.my_account',
    ),
    re_path(
        r'^myaccount/password/$',
        views.password_change,
        name='journalmanager.password_change',
    ),
    re_path(
        r'^unauthorized/$',
        views.unauthorized,
        name='accounts.unauthorized',
    ),
]
