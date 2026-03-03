# coding: utf-8
from django.urls import re_path

from . import views


urlpatterns = [
    re_path(r'^markupfiles/$', views.markup_files, name="export.markupfiles"),
]
