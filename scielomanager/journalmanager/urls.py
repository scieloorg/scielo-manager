# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from scielomanager.journalmanager import views
from scielomanager.journalmanager import models

urlpatterns = patterns('',

    # Journal Tools
    url(r'^$', views.journal_index, {'model': models.Journal}, name="journal.index"),
    url(r'^new/$', views.add_journal, name='journal.add'),
    url(r'^(?P<journal_id>\d+)/dash/$', views.dash_journal, name='journal.dash'),
    url(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    url(r'^(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Journal}, name='journal.toggle_availability'),
    url(r'^(?P<journal_id>\d+)/edit/status/$', views.edit_journal_status, name='journal_status.edit'),
    url(r'^del_pended/(?P<form_hash>\w+)/$', views.del_pended, name='journal.del_pended'),

    # Sponsor Tools
    url(r'^sponsor/$', views.sponsor_index, {'model': models.Sponsor}, name='sponsor.index'),
    url(r'^sponsor/new/$', views.add_sponsor, name='sponsor.add'),
    url(r'^sponsor/(?P<sponsor_id>\d+)/edit/$', views.add_sponsor, name='sponsor.edit'),
    url(r'^sponsor/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Sponsor}, name='sponsor.toggle_availability'),

    # Section Tools
    url(r'^(?P<journal_id>\d+)/section/$', views.section_index, {'model': models.Section}, name='section.index'),
    url(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add'),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit'),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/del/$', views.del_section, name='section.del'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issue/$', views.issue_index, name='issue.index'),
    url(r'^(?P<journal_id>\d+)/issue/new/$', views.add_issue, name='issue.add'),
    url(r'^(?P<journal_id>\d+)/issue/reorder/$', views.issue_reorder, name='issue.reorder.ajax'),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.add_issue, name='issue.edit'),
    url(r'^issue/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Issue}, name='issue.toggle_availability'),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/new/$', views.add_user, name="user.add"),
    url(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    url(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability'),
    url(r'^user/(?P<user_id>\d+)/toggle_active_collection/(?P<collection_id>\d+)$',
        views.toggle_active_collection, name='usercollection.toggle_active'),

    # Ajax requests
    url(r'^ajx/ajx1/$', views.ajx_list_issues_for_markup_files, name="ajx.list_issues_for_markup_files"),
)
