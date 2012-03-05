# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.contrib.auth.views import *
from django.conf import settings

from scielomanager.journalmanager import views

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.index, name='index'),

    # Journal Manager APP
    url(r'^journal/', include('scielomanager.journalmanager.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),


    url(r'^accounts/logout/$', views.user_logout, name='journalmanager.user_logout'),
    url(r'^accounts/login/$', views.user_login, name='journalmanager.user_login'),
    url(r'^accounts/password/reset/$', password_reset, {
        'template_name': 'registration/password_reset_form.html',
        'email_template_name': 'registration/password_reset_email.html',
        'post_reset_redirect': '/accounts/password/reset/done/'},
        name='registration.password_reset'),

    url(r'^accounts/password/reset/done/$', password_reset_done, {
        'template_name': 'registration/password_reset_done.html'},
        name='registration.password_reset_done'),

    url(r'^accounts/password/reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$',
        password_reset_confirm, {
        'template_name': 'registration/password_reset_confirm.html',
        'post_reset_redirect': '/accounts/password/reset/complete/'},
        name='registration.password_reset_confirm'),

    url(r'^accounts/password/reset/complete/$', password_reset_complete, {
        'template_name': 'registration/password_reset_complete.html'},
        name='registration.password_reset_complete'),

    url(r'^myaccount/$', views.my_account, name='journalmanager.my_account'),
    url(r'^myaccount/password/$', views.password_change, name='journalmanager.password_change'),

    (r'^i18n/', include('django.conf.urls.i18n')),
)


if settings.DEBUG:
    # serve static files from develpment server
    from django.views import static

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
