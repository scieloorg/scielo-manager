# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
    url(r'^$', views.checkin_index, name="checkin_index"),
    url(r'^package/(?P<article_id>\d+)/$', views.checkin_history, name="checkin_history"),
    url(r'^notice/(?P<checkin_id>\d+)/$', views.notice_detail, name="notice_detail"),
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
    	name="get_balaio_api_full_package"
    ),
    url(r'^balaio_api/files_members/(?P<attempt_id>\d+)/(?P<target_name>.+)/$',
        views.get_balaio_api_files_members,
        name="get_balaio_api_files_members"
    ),    
)
