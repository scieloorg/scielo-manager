# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from scielomanager.title.models import *
from scielomanager.title.views import *


urlpatterns = patterns('',   
    # Title Tools
    url(r'^$', title_index, name="title.index"),
    url(r'^add/$', add_title, name='title.add'),
    url(r'^show/(?P<title_id>\d+)/$', show_title, name='title.show'),
    url(r'^edit/(?P<title_id>\d+)/$', edit_title, name='title.edit'),    
    
    # Publisher Tools
    url(r'^publisher/$', publisher_index, name='publisher.index' ),
    url(r'^publisher/add/$', add_publisher, name='publisher.add' ),
    url(r'^publisher/show/(?P<publisher_id>\d+)/$', show_publisher, name='publisher.show' ),    
    url(r'^publisher/edit/(?P<publisher_id>\d+)/$', edit_publisher, name='publisher.edit' ),
    
    # Users Tools
    url(r'^user/$', user_index, name="user.index"),
    url(r'^user/add/$', add_user, name="user.add"),
    url(r'^user/show/(?P<user_id>\d+)/$', show_user, name="user.show"),
    url(r'^user/edit/(?P<user_id>\d+)/$', edit_user, name="user.edit"),    

)