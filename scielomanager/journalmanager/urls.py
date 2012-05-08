# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from scielomanager.journalmanager import views
from scielomanager.journalmanager import models


urlpatterns = patterns('',

    # Journal Tools
    url(r'^$', views.generic_index_search, {'model': models.Journal},  name="journal.index",),
    url(r'^new/$', views.add_journal, name='journal.add'),
    url(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    url(r'^(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Journal}, name='journal.toggle_availability'),
    url(r'^bulk_action/(?P<action_name>\w+)/(?P<value>\w+)/$', views.generic_bulk_action, {'model': models.Journal}, name='journal.bulk_action'),

    # Publisher Tools
    url(r'^publisher/$', views.generic_index_search, {'model': models.Publisher}, name='publisher.index' ),
    url(r'^publisher/new/$', views.add_publisher, name='publisher.add' ),
    url(r'^publisher/(?P<publisher_id>\d+)/edit/$', views.add_publisher, name='publisher.edit' ),
    url(r'^publisher/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Publisher}, name='publisher.toggle_availability' ),

    # Section Tools
    url(r'^(?P<journal_id>\d+)/section/$', views.generic_index_search, {'model': models.Section}, name='section.index' ),
    url(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add' ),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit' ),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issue/$', views.issue_index, name='issue.index' ),
    url(r'^(?P<journal_id>\d+)/issue/new/$', views.add_issue, name='issue.add' ),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.add_issue, name='issue.edit' ),
    url(r'^issue/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability, {'model': models.Issue}, name='issue.toggle_availability' ),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/new/$', views.add_user, name="user.add"),
    url(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    url(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability' ),


)
