# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from scielomanager.title.models import *
from scielomanager.title.views import *


urlpatterns = patterns('',
    url(r'^$', title_index, name="title.index"),
    url(r'^user/$', user_index, name="user.index"),
    url(r'^user/add/$', add_user, name="user.add"),        
    url(r'^show/(?P<title_id>\d+)/$', show_title, name='title.show'),
    url(r'^add/$', add_title, name='title.add'),
    url(r'^open/$', open_title, name='title.open'),
    url(r'^publisher/$', publisher_index, name='publisher.index' ),
    url(r'^publisher/add/$', add_publisher, name='publisher.add' ),    
)