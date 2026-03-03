# -*- encoding: utf-8 -*-
from django.urls import re_path
from django.conf import settings

from . import views

urlpatterns = [
    re_path(r'^stylechecker/$', views.packtools_home, name="validator.packtools.stylechecker"),
]

if settings.VALIDATOR_ENABLE_HTML_PREVIEWER:
    urlpatterns += [
        re_path(r'^preview/html/$', views.packtools_preview_html, name="validator.packtools.preview_html"),
    ]
