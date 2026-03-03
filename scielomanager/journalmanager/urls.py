# -*- encoding: utf-8 -*-
from django.urls import re_path

from . import views, models

urlpatterns = [

    # Journal Tools
    re_path(r'^$', views.journal_index, name="journal.index"),
    re_path(r'^new/$', views.add_journal, name='journal.add'),
    re_path(r'^(?P<journal_id>\d+)/dash/$', views.dash_journal, name='journal.dash'),
    re_path(r'^(?P<journal_id>\d+)/edit/$', views.add_journal, name='journal.edit'),
    re_path(r'^(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Journal}, name='journal.toggle_availability'),
    re_path(r'^(?P<journal_id>\d+)/edit/status/$', views.edit_journal_status, name='journal_status.edit'),
    re_path(r'^del_pended/(?P<form_hash>\w+)/$', views.del_pended, name='journal.del_pended'),

    # Sponsor Tools
    re_path(r'^sponsor/$', views.sponsor_index, name='sponsor.index'),
    re_path(r'^sponsor/new/$', views.add_sponsor, name='sponsor.add'),
    re_path(r'^sponsor/(?P<sponsor_id>\d+)/edit/$', views.add_sponsor, name='sponsor.edit'),
    re_path(r'^sponsor/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Sponsor}, name='sponsor.toggle_availability'),

    # Section Tools
    re_path(r'^(?P<journal_id>\d+)/section/$', views.section_index, name='section.index'),
    re_path(r'^(?P<journal_id>\d+)/section/new/$', views.add_section, name='section.add'),
    re_path(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/edit/$', views.add_section, name='section.edit'),
    re_path(r'^(?P<journal_id>\d+)/section/(?P<section_id>\d+)/del/$', views.del_section, name='section.del'),

    # Press release Tools
    re_path(r'^(?P<journal_id>\d+)/prelease/$', views.pressrelease_index, name='prelease.index'),
    re_path(r'^(?P<journal_id>\d+)/prelease/new/$', views.add_pressrelease, name='prelease.add'),
    re_path(r'^(?P<journal_id>\d+)/prelease/(?P<prelease_id>\d+)/edit/$', views.add_pressrelease, name='prelease.edit'),
    re_path(r'^(?P<journal_id>\d+)/aprelease/new/$', views.add_aheadpressrelease, name='aprelease.add'),
    re_path(r'^(?P<journal_id>\d+)/aprelease/(?P<prelease_id>\d+)/edit/$', views.add_aheadpressrelease, name='aprelease.edit'),

    # Issue Tools
    re_path(r'^(?P<journal_id>\d+)/issue/$', views.issue_index, name='issue.index'),
    re_path(r'^(?P<journal_id>\d+)/issue/new/regular/$', views.add_issue, {'issue_type': 'regular'}, name='issue.add_regular'),
    re_path(r'^(?P<journal_id>\d+)/issue/new/special/$', views.add_issue, {'issue_type': 'special'}, name='issue.add_special'),
    re_path(r'^(?P<journal_id>\d+)/issue/new/supplement/$', views.add_issue, {'issue_type': 'supplement'}, name='issue.add_supplement'),
    re_path(r'^(?P<journal_id>\d+)/issue/(?P<issue_id>\d+)/edit/$', views.edit_issue, name='issue.edit'),
    re_path(r'^issue/(?P<object_id>\d+)/toggle_availability/$', views.generic_toggle_availability,
        {'model': models.Issue}, name='issue.toggle_availability'),

    # Users Tools
    re_path(r'^user/$', views.user_index, name="user.index"),
    re_path(r'^user/new/$', views.add_user, name="user.add"),
    re_path(r'^user/add_to_collection/$', views.add_user_to_collection, name="user.add_user_to_collection"),
    re_path(r'^user/exclude_from_collection/(?P<user_id>\d+)$', views.exclude_user_from_collection, name="user.exclude_user_from_collection"),
    re_path(r'^user/(?P<user_id>\d+)/edit/$', views.add_user, name="user.edit"),
    re_path(r'^user/(?P<user_id>\d+)/toggle_availability/$', views.toggle_user_availability, name='user.toggle_availability'),
    re_path(r'^user/(?P<user_id>\d+)/toggle_active_collection/(?P<collection_id>\d+)$',
        views.toggle_active_collection, name='usercollection.toggle_active'),

    #Editor
    re_path(r'^(?P<journal_id>\d+)/editor/$', views.get_editor, name="editor.index"),
    re_path(r'^(?P<journal_id>\d+)/editor/add/$', views.add_editor, name="editor.add"),

    # Ajax requests
    re_path(r'^ajx/ajx1/$', views.ajx_list_issues_for_markup_files, name="ajx.list_issues_for_markup_files"),
    re_path(r'^ajx/ajx2/$', views.ajx_lookup_for_section_translation, name="ajx.lookup_for_section_translation"),
    re_path(r'^ajx/ajx3/$', views.ajx_search_journal, name="ajx.ajx_search_journal"),
    re_path(r'^ajx/ajx4/(?P<journal_id>\d+)$', views.ajx_add_journal_to_user_collection, name="ajx.ajx_add_journal_to_user_collection"),
]
