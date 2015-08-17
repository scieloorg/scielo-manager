# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *

from . import views, models


urlpatterns = patterns('',

    # Journal Tools
    url(r'^$', views.journal_index, name="journal.index"),
    url(r'^new/$', views.add_journal, name='journal.add'),
    url(r'^(?P<journal_id>\d+)/dash/$', views.dash_journal, name='journal.dash'),
    url(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    url(r'^(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Journal}, name='journal.toggle_availability'),
    url(r'^(?P<journal_id>\d+)/edit/status/$', views.edit_journal_status, name='journal_status.edit'),
    url(r'^del_pended/(?P<form_hash>\w+)/$', views.del_pended, name='journal.del_pended'),

    # Sponsor Tools
    url(r'^sponsor/$', views.sponsor_index, name='sponsor.index'),
    url(r'^sponsor/new/$', views.add_sponsor, name='sponsor.add'),
    url(r'^sponsor/(?P<sponsor_id>\d+)/edit/$', views.add_sponsor, name='sponsor.edit'),
    url(r'^sponsor/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Sponsor}, name='sponsor.toggle_availability'),

    # Section Tools
    url(r'^(?P<journal_id>\d+)/section/$', views.section_index, name='section.index'),
    url(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add'),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit'),
    url(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/del/$', views.del_section, name='section.del'),

    # Press release Tools
    url(r'^(?P<journal_id>\d+)/prelease/$', views.pressrelease_index, name='prelease.index'),
    url(r'^(?P<journal_id>\d+)/prelease/new/$', views.add_pressrelease, name='prelease.add'),
    url(r'^(?P<journal_id>\d+)/prelease/(?P<prelease_id>\d+)/edit/$', views.add_pressrelease, name='prelease.edit'),
    url(r'^(?P<journal_id>\d+)/aprelease/new/$', views.add_aheadpressrelease, name='aprelease.add'),
    url(r'^(?P<journal_id>\d+)/aprelease/(?P<prelease_id>\d+)/edit/$', views.add_aheadpressrelease, name='aprelease.edit'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issue/$', views.issue_index, name='issue.index'),
    url(r'^(?P<journal_id>\d+)/issue/new/regular/$', views.add_issue, {'issue_type': 'regular'}, name='issue.add_regular'),
    url(r'^(?P<journal_id>\d+)/issue/new/special/$', views.add_issue, {'issue_type': 'special'}, name='issue.add_special'),
    url(r'^(?P<journal_id>\d+)/issue/new/supplement/$', views.add_issue, {'issue_type': 'supplement'}, name='issue.add_supplement'),
    url(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='issue.edit'),
    url(r'^issue/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Issue}, name='issue.toggle_availability'),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/new/$', views.add_user, name="user.add"),
    url(r'^user/add_to_collection/$', views.add_user_to_collection, name="user.add_user_to_collection"),
    url(r'^user/exclude_from_collection/(?P<user_id>\d+)$', views.exclude_user_from_collection, name="user.exclude_user_from_collection"),
    url(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    url(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability'),
    url(r'^user/(?P<user_id>\d+)/toggle_active_collection/(?P<collection_id>\d+)$',
        views.toggle_active_collection, name='usercollection.toggle_active'),

    #Editor
    url(r'^(?P<journal_id>\d+)/editor/$', views.get_editor, name="editor.index"),
    url(r'^(?P<journal_id>\d+)/editor/add/$', views.add_editor, name="editor.add"),

    # Ajax requests
    url(r'^ajx/ajx1/$', views.ajx_list_issues_for_markup_files, name="ajx.list_issues_for_markup_files"),
    url(r'^ajx/ajx2/$', views.ajx_lookup_for_section_translation, name="ajx.lookup_for_section_translation"),
    url(r'^ajx/ajx3/$', views.ajx_search_journal, name="ajx.ajx_search_journal"),
    url(r'^ajx/ajx4/(?P<journal_id>\d+)$', views.ajx_add_journal_to_user_collection, name="ajx.ajx_add_journal_to_user_collection"),
)
