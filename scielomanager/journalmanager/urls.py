# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list

from scielomanager.journalmanager import views


urlpatterns = patterns('',
    # Journal Tools
    url(r'^$', views.journal_index, name="journal.index",),
    url(r'^add/$', views.add_journal, name='journal.add'),
    url(r'^show/(?P<journal_id>\d+)/$', views.show_journal, name='journal.show'),
    url(r'^edit/(?P<journal_id>\d+)/$', views.add_journal, name='journal.edit'),
    url(r'^toggle_availability/(?P<journal_id>\d+)/$', views.toggle_journal_availability, name='journal.toggle_availability'),

    #Search Journal
    url(r'^search/$', views.search_journal, name='journal.search'),

    # Institution Tools
    url(r'^institution/$', views.institution_index, name='institution.index' ),
    url(r'^institution/add/$', views.add_institution, name='institution.add' ),
    url(r'^institution/show/(?P<institution_id>\d+)/$', views.show_institution, name='institution.show' ),
    url(r'^institution/edit/(?P<institution_id>\d+)/$', views.add_institution, name='institution.edit' ),
    url(r'^institution/toggle_availability/(?P<institution_id>\d+)/$', views.toggle_institution_availability, name='institution.toggle_availability' ),

    #Search Institution
    url(r'^institution/search/$', views.search_institution, name='institution.search'),

    # Section Tools
    #url(r'^section/$', section_index, name='section.index' ),
    #url(r'^section/add/(?P<journal_id>\d+/$', add_section, name='section.add' ),
    #url(r'^section/show/(?P<section_id>\d+)/$', show_section, name='section.show' ),
    #url(r'^section/edit/(?P<section_id>\d+)/$', edit_section, name='section.edit' ),
    #url(r'^section/delete/(?P<section_id>\d+)/$', delete_section, name='section.delete' ),
    #url(r'^section/search/$', search_section, name='section.search'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issues/$', views.issue_index, name='issue.index' ),
    url(r'^(?P<journal_id>\d+)/issues/new/$', views.add_issue, name='issue.add' ),
    url(r'^(?P<journal_id>\d+)/issues/(?P<issue_id>\d+)/edit/$', views.add_issue, name='issue.edit' ),
    url(r'^issue/show/(?P<issue_id>\d+)/$', views.show_issue, name='issue.show' ),
    url(r'^issue/toggle/(?P<issue_id>\d+)/$', views.toggle_issue, name='issue.toggle' ),
    url(r'^issue/search/(?P<journal_id>\d+)/$', views.search_issue, name='issue.search'),

    # Users Tools
    url(r'^user/$', views.user_index, name="user.index"),
    url(r'^user/add/$', views.add_user, name="user.add"),
    url(r'^user/show/(?P<user_id>\d+)/$', views.show_user, name="user.show"),
    url(r'^user/edit/(?P<user_id>\d+)/$', views.edit_user, name="user.edit"),

)
