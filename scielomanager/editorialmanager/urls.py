#coding: utf-8
from django.conf.urls.defaults import *

from . import views

urlpatterns = patterns('',

    url(r'^$', views.editorial_index, name="editorial.index"),

    )
