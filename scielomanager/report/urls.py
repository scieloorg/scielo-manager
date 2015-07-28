# coding: utf-8

from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',

    url(r'^list/$', views.report_index, name="report.index"),

    url(r'^editorialmanager/member/list/$', views.member_list, name="report.member_list"),

    url(r'^editorialmanager/task/status/(?P<task_id>.+)/$', views.task_status, name="report.task_status"),

    url(r'^editorialmanager/task/export_csv/(?P<task_id>.+)/$', views.export_csv, name="report.export_csv"),

)
