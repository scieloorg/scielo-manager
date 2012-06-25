# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from piston.resource import Resource
from scielomanager.api import handlers

journal_handler = Resource(handlers.Journal)
collection_handler = Resource(handlers.Collection)
issue_handler = Resource(handlers.Issue)
sections_handler = Resource(handlers.Section)

urlpatterns = patterns('',

    # Journals
    url(r'^journals/(?P<collection>\w+)/$', journal_handler, name='api_v1_journal.index'),
    url(r'^journals/(?P<collection>\w+)/(?P<issn>(\d{4})-(\d{3}[0-9X]))/$', journal_handler,
        name='api_v1_journal.getone'),

    #Collections
    url(r'^collections/$', collection_handler),
    url(r'^collections/(?P<name_slug>\w+)/$', collection_handler),

    #Issues
    url(r'^issues/(?P<collection>\w+)/(?P<issn>(\d{4})-(\d{3}[0-9X]))/$', issue_handler),
    url(r'^issues/(?P<collection>\w+)/(?P<issn>(\d{4})-(\d{3}[0-9X]))/(?P<issue_label>\w+)/$', issue_handler),

    #Sections
    url(r'^sections/(?P<collection>\w+)/(?P<issn>(\d{4})-(\d{3}[0-9X]))/$', sections_handler),

)
