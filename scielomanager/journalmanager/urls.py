# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.views.generic.list_detail import object_detail, object_list
from scielomanager.journalmanager.models import *
from scielomanager.journalmanager.views import *


urlpatterns = patterns('',
    # Journal Tools
    url(r'^$', journal_index, name="journal.index"),
    url(r'^add/$', add_journal, name='journal.add'),
    url(r'^show/(?P<journal_id>\d+)/$', show_journal, name='journal.show'),
    url(r'^edit/(?P<journal_id>\d+)/$', add_journal, name='journal.edit'),
    url(r'^toggle/(?P<journal_id>\d+)/$', toggle_journal, name='journal.toggle'),

    #Search Journal
    url(r'^search/$', search_journal, name='journal.search'),

    # Institution Tools
    url(r'^institution/$', institution_index, name='institution.index' ),
    url(r'^institution/add/$', add_institution, name='institution.add' ),
    url(r'^institution/show/(?P<institution_id>\d+)/$', show_institution, name='institution.show' ),
    url(r'^institution/edit/(?P<institution_id>\d+)/$', add_institution, name='institution.edit' ),
    url(r'^institution/toggle/(?P<institution_id>\d+)/$', toggle_institution, name='institution.toggle' ),

    #Search Institution
    url(r'^institution/search/$', search_institution, name='institution.search'),

    # Section Tools
    #url(r'^section/$', section_index, name='section.index' ),
    #url(r'^section/add/(?P<journal_id>\d+/$', add_section, name='section.add' ),
    #url(r'^section/show/(?P<section_id>\d+)/$', show_section, name='section.show' ),
    #url(r'^section/edit/(?P<section_id>\d+)/$', edit_section, name='section.edit' ),
    #url(r'^section/delete/(?P<section_id>\d+)/$', delete_section, name='section.delete' ),
    #url(r'^section/search/$', search_section, name='section.search'),

    # Issue Tools
    url(r'^(?P<journal_id>\d+)/issues/$', issue_index, name='issue.index' ),
    url(r'^(?P<journal_id>\d+)/issues/new/$', add_issue, name='issue.add' ),
    url(r'^(?P<journal_id>\d+)/issues/(?P<issue_id>\d+)/edit/$', add_issue, name='issue.edit' ),
    url(r'^issue/show/(?P<issue_id>\d+)/$', show_issue, name='issue.show' ),
    url(r'^(?P<journal_id>\d+)/issue/toggle/(?P<issue_id>\d+)/$', toggle_issue, name='issue.toggle' ),
    url(r'^issue/search/(?P<journal_id>\d+)/$', search_issue, name='issue.search'),

    # Users Tools
    url(r'^user/$', user_index, name="user.index"),
    url(r'^user/add/$', add_user, name="user.add"),
    url(r'^user/show/(?P<user_id>\d+)/$', show_user, name="user.show"),
    url(r'^user/edit/(?P<user_id>\d+)/$', edit_user, name="user.edit"),

)
