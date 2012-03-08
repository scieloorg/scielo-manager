# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from scielomanager.journalmanager import views


urlpatterns = patterns('',
    # Journal Tools
    url(r'^$', views.journal_index, name="journal.index",),
    url(r'^new/$', views.add_journal, name='journal.add'),
    url(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    url(r'^(?P<journal_id>\d+)/toggle_availability/$', views.toggle_journal_availability, name='journal.toggle_availability'),
    url(r'^search/$', views.search_journal, name='journal.search'),

    # Publisher Tools
    url(r'^publisher/$', views.publisher_index, name='publisher.index' ),
    url(r'^publisher/new/$', views.add_publisher, name='publisher.add' ),
    url(r'^publisher/(?P<publisher_id>\d+)/edit/$', views.add_publisher, name='publisher.edit' ),
    url(r'^publisher/(?P<publisher_id>\d+)/toggle_availability/$', views.toggle_publisher_availability, name='publisher.toggle_availability' ),
    url(r'^publisher/search/$', views.search_publisher, name='publisher.search'),

    # Section Tools
    url(r'^(?P<journal_id>\d+)/section/$', views.section_index, name='section.index' ),
    url(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add' ),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit' ),
    #url(r'^section/delete/(?P<section_id>\d+)/$', delete_section, name='section.delete' ),
    #url(r'^section/search/$', search_section, name='section.search'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issue/$', views.issue_index, name='issue.index' ),
    url(r'^(?P<journal_id>\d+)/issue/new/$', views.add_issue, name='issue.add' ),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.add_issue, name='issue.edit' ),
    url(r'^issue/(?P<issue_id>\d+)/toggle_availability/$', views.toggle_issue_availability, name='issue.toggle_availability' ),
    url(r'^(?P<journal_id>\d+)/issue/search/$', views.search_issue, name='issue.search'),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/new/$', views.add_user, name="user.add"),
    url(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    url(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability' ),

    # Center Tools
    url(r'^center/$', views.center_index, name='center.index' ),
    url(r'^center/new/$', views.add_center, name='center.add' ),
    url(r'^center/(?P<center_id>\d+)/edit/$', views.add_center, name='center.edit' ),
    url(r'^center/(?P<center_id>\d+)/toggle_availability/$', views.toggle_center_availability, name='center.toggle_availability' ),
    url(r'^center/search/$', views.search_center, name='center.search'),
)
