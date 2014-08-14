# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api

from journalmanager import views, models
from api import resources_v1, resources_v2

admin.autodiscover()

# RESTful API config
v1_api = Api(api_name='v1')
v1_api_resources = [
    resources_v1.JournalResource(),
    resources_v1.UserResource(),
    resources_v1.UseLicenseResource(),
    resources_v1.SponsorResource(),
    resources_v1.CollectionResource(),
    resources_v1.IssueResource(),
    resources_v1.SectionResource(),
    resources_v1.DataChangeEventResource(),
    resources_v1.PressReleaseResource(),
    resources_v1.AheadPressReleaseResource(),
    resources_v1.CheckinResource(),
    resources_v1.CheckinNoticeResource(),
    resources_v1.ArticleResource(),
    resources_v1.CheckinArticleResource(),
    resources_v1.TicketResource(),
    resources_v1.CommentResource()
]

for res in v1_api_resources:
    v1_api.register(res)

v2_api = Api(api_name='v2')

v2_api_resources = [
    resources_v2.JournalResource(),
    resources_v2.UserResource(),
    resources_v2.UseLicenseResource(),
    resources_v2.SponsorResource(),
    resources_v2.CollectionResource(),
    resources_v1.IssueResource(),
]

for res in v2_api_resources:
    v2_api.register(res)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # Article Tracking
    url(r'^arttrack/', include('articletrack.urls')),

    # Article Tools
    url(r'^issue/(?P<issue_id>\d+)/articles/$', views.article_index, name='article.index'),
    #url(r'^article/(?P<article_id>\d+)/edit/$', views.add_article, name='article.edit'),

    # Journal Manager APP
    url(r'^journal/', include('journalmanager.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Collection Tools
    url(r'^collection/(?P<collection_id>\d+)/edit/$', views.add_collection, name='collection.edit'),

    url(r'accounts/', include('accounts.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),

    # Trash
    url(r'^trash/$', views.trash_listing, name="trash.listing"),
    url(r'^trash/bulk_action/(?P<model_name>\w+)/(?P<action_name>\w+)/(?P<value>\w+)/$',
        views.generic_bulk_action, name='trash.bulk_action'),

    #API version 1
    (r'^api/', include(v1_api.urls)),

    #API version 2
    (r'^api/', include(v2_api.urls)),

    (r'^export/', include('export.urls')),

    #AJAX
    url(r'^ajx/ajx3/$', views.ajx_list_users, name="ajx.ajx_list_users"),

    # Validator URLs:
    url(r'^tools/validators/', include('validator.urls')),
)

if settings.DEBUG:

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )
