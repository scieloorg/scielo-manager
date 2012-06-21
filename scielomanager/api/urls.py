# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from scielomanager.api import handlers

journal_handler = Resource(handlers.Journal)

urlpatterns = patterns('',

    url(r'^v1/journals/(?P<collection>\w+)/(?P<issn>[0-9-]+)$', journal_handler),

)
