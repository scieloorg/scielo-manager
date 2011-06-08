# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from scielomanager.title.models import *
from scielomanager.title.views import *


urlpatterns = patterns('',
    url(r'^$', title_index, name="title.index"),
    url(r'^show/(?P<title_id>\d+)/$', show_title, name='title.show' ),
    url(r'^add/$', add_title, name='title.add' ),
    url(r'^open/$', open_title, name='title.open' ),        
    url(r'^publisher/$', publisher_index, name='publisher.index' ),    
    #url(r'^search/$', search, name="title.search"),
    #url(r'^list/$', login_required(object_list), info_dict, name="title.list"),
    #url(r'^history/(?P<object_id>\d+)/$', login_required(object_detail), info_dict, name='title.history' ),
    #url(r'^newiteration/(?P<object_id>\d+)/$', new_iteration, name='title.new_iteration' ),
    #url(r'^meeting/(?P<evaluation_id>\d+)/(?P<meeting_id>\d+)', set_meeting, name='title.set_meeting' ),
)