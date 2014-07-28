# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.checkin_index, name="checkin_index"),
    # url(r'^package/(?P<article_id>\d+)/$', views.checkin_history, name="checkin_history"),
    # notice:
    url(r'^notice/(?P<checkin_id>\d+)/$', views.notice_detail, name="notice_detail"),
    url(r'^checkin/(?P<checkin_id>\d+)/reject/$', views.checkin_reject, name="checkin_reject"),
    url(r'^checkin/(?P<checkin_id>\d+)/review/(?P<level>\d)$', views.checkin_review, name="checkin_review"),
    url(r'^checkin/(?P<checkin_id>\d+)/accept/$', views.checkin_accept, name="checkin_accept"),
    url(r'^checkin/(?P<checkin_id>\d+)/send_to/pending/$', views.checkin_send_to_pending, name="checkin_send_to_pending"),
    url(r'^checkin/(?P<checkin_id>\d+)/send_to/review/$', views.checkin_send_to_review, name="checkin_send_to_review"),
    url(r'^checkin/(?P<checkin_id>\d+)/send_to/checkout/$', views.checkin_send_to_checkout, name="checkin_send_to_checkout"),
    url(r'^checkin/(?P<checkin_id>\d+)/history/$', views.checkin_history, name="checkin_history"),

    # TICKETS
    url(r'^ticket/add/(?P<checkin_id>\d+)/$', views.ticket_add, name="ticket_add"),
    url(r'^ticket/edit/(?P<ticket_id>\d+)/$', views.ticket_edit, name="ticket_edit"),
    url(r'^ticket/(?P<ticket_id>\d+)/close/$', views.ticket_close, name="ticket_close"),
    url(r'^ticket/(?P<ticket_id>\d+)/$', views.ticket_detail, name="ticket_detail"),
    url(r'^ticket/$', views.ticket_list, name="ticket_list"),
    url(r'^comment/edit/(?P<comment_id>\d+)/$', views.comment_edit, name="comment_edit"),

    # BALAIO API
    url(r'^balaio_api/is_up/$', views.get_balaio_api_is_up, name="get_balaio_api_is_up"),
    url(r'^balaio_api/full_package/(?P<attempt_id>\d+)/(?P<target_name>.+)/$',
        views.get_balaio_api_full_package,
        name="get_balaio_api_full_package"),
    url(r'^balaio_api/files_members/(?P<attempt_id>\d+)/(?P<target_name>.+)/$',
        views.get_balaio_api_files_members,
        name="get_balaio_api_files_members"),
)
