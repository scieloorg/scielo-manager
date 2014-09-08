#coding: utf-8
from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',

    url(r'^$', views.index, name="index"),

    # Journal related urls
    url(r'^journal/detail/$', views.journal_detail, name="editorial.journal.detail"),
    url(r'^journal/(?P<journal_id>\d+)/edit/$', views.journal_edit, name="editorial.journal.edit"),


    # Editorial Manager
    url(r'^board/$', views.board, name="editorial.board"),

    )
