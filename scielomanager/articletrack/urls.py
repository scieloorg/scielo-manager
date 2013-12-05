# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from scielomanager.articletrack import views

urlpatterns = patterns('',
    url(r'^$', views.checkin_index, name="checkin_index"),
    url(r'^package/(?P<articlepkg>\w+)/$', views.checkin_history, name="checkin_history"),
    url(r'^notice/(?P<checkin_id>\d+)/$', views.notice_detail, name="notice_detail"),
)
