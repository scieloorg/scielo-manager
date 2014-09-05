#coding: utf-8
from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',

    url(r'^$', views.index, name="index"),

    # Journal related urls
    url(r'^journal/detail/$', views.journal_detail, name="journal.detail"),

    # Editorial Manager
    url(r'^board/$', views.board, name="editorial.board"),

    )
