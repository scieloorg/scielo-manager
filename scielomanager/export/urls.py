# coding: utf-8
from django.conf.urls.defaults import *

from scielomanager.export import views


urlpatterns = patterns('',
    url(r'^markupfiles/$', views.markup_files, name="export.markupfiles"),
)
