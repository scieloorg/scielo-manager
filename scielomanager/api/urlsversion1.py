# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from scielomanager.api import handlers

journal_handler = Resource(handlers.Journal)
collection_handler = Resource(handlers.Collection)

urlpatterns = patterns('',

    url(r'^journals/(?P<collection>\w+)/$', journal_handler),
    url(r'^journals/(?P<collection>\w+)/(?P<issn>(\d{4})-(\d{3}[0-9X]))/$', journal_handler),
    url(r'^collections/$', collection_handler),
    url(r'^collections/(?P<name_slug>\w+)/$', collection_handler),
)
