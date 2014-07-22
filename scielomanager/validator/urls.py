# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns('',
	url(r'^stylechecker/$', views.packtools_home, name="validator.packtools.stylechecker"),
)