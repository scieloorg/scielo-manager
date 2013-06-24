# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from scielomanager.articletrack import views

urlpatterns = patterns('',
    url(r'^$', views.attempts_index, name="attempts.index"),
)
