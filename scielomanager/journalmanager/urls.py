# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from scielomanager.journalmanager import views
from scielomanager.journalmanager import models


urlpatterns = patterns('',
    # Journal Tools
    url(r'^$', views.generic_index, {'model': models.Journal},  name="journal.index",),
    url(r'^new/$', views.add_journal, name='journal.add'),
    url(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    url(r'^(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Journal}, name='journal.toggle_availability'),
    url(r'^search/$', views.search_journal, name='journal.search'),

    # Publisher Tools
    url(r'^publisher/$', views.generic_index, {'model': models.Publisher}, name='publisher.index' ),
    url(r'^publisher/new/$', views.add_publisher, name='publisher.add' ),
    url(r'^publisher/(?P<publisher_id>\d+)/edit/$', views.add_publisher, name='publisher.edit' ),
    url(r'^publisher/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Publisher}, name='publisher.toggle_availability' ),
    url(r'^publisher/search/$', views.search_publisher, name='publisher.search'),

    # Section Tools
    url(r'^(?P<journal_id>\d+)/section/$', views.generic_index, {'model': models.Section}, name='section.index' ),
    url(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add' ),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit' ),
    #url(r'^section/delete/(?P<section_id>\d+)/$', delete_section, name='section.delete' ),
    #url(r'^section/search/$', search_section, name='section.search'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issue/$', views.generic_index, {'model': models.Issue}, name='issue.index' ),
    url(r'^(?P<journal_id>\d+)/issue/new/$', views.add_issue, name='issue.add' ),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.add_issue, name='issue.edit' ),
    url(r'^issue/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Issue}, name='issue.toggle_availability' ),
    url(r'^(?P<journal_id>\d+)/issue/search/$', views.search_issue, name='issue.search'),

    # Center Tools
    url(r'^center/$', views.generic_index, {'model': models.Center}, name='center.index' ),
    url(r'^center/new/$', views.add_center, name='center.add' ),
    url(r'^center/(?P<center_id>\d+)/edit/$', views.add_center, name='center.edit' ),
    url(r'^center/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Center}, name='center.toggle_availability' ),
    url(r'^center/search/$', views.search_center, name='center.search'),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/new/$', views.add_user, name="user.add"),
    url(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    url(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability' ),


)
