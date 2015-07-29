# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from . import views

urlpatterns = patterns(
    '',
    url(r'^stylechecker/$', views.packtools_home, name="validator.packtools.stylechecker"),
    url(r'^preview/html/$', views.packtools_preview_html, name="validator.packtools.preview_html"),
)
