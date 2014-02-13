# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^$', views.checkin_index, name="checkin_index"),
    url(r'^package/(?P<articlepkg>\d+)/$', views.checkin_history, name="checkin_history"),
    url(r'^notice/(?P<checkin_id>\d+)/$', views.notice_detail, name="notice_detail"),
    # TICKETS
    url(r'^ticket/add/(?P<checkin_id>\d+)/$', views.ticket_add, name="ticket_add"),
    url(r'^ticket/edit/(?P<ticket_id>\d+)/$', views.ticket_edit, name="ticket_edit"),
    url(r'^ticket/(?P<ticket_id>\d+)/close/$', views.ticket_close, name="ticket_close"),
    url(r'^ticket/(?P<ticket_id>\d+)/$', views.ticket_detail, name="ticket_detail"),
    url(r'^ticket/$', views.ticket_list, name="ticket_list"),
)
