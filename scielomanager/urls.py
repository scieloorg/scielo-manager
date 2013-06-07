# -*- encoding: utf-8 -*-
from django.conf.urls.defaults import *
from django.contrib import admin
from django.conf import settings
from tastypie.api import Api

from scielomanager.journalmanager import views
from scielomanager.journalmanager import models
from scielomanager.api import resources

admin.autodiscover()

# RESTful API config
v1_api = Api(api_name='v1')
v1_api_resources = [
    resources.JournalResource(),
    resources.UserResource(),
    resources.UseLicenseResource(),
    resources.SponsorResource(),
    resources.CollectionResource(),
    resources.IssueResource(),
    resources.SectionResource(),
    resources.DataChangeEventResource(),
    resources.PressReleaseResource(),
    resources.AheadPressReleaseResource(),
    resources.ArticleTrackResource(),
]
for res in v1_api_resources:
    v1_api.register(res)

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),

    # Journal Manager APP
    url(r'^journal/', include('scielomanager.journalmanager.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),

    # Collection Tools
    url(r'^collection/$', views.collection_index, {'model': models.Collection}, name='collection.index'),
    url(r'^collection/new/$', views.add_collection, name='collection.add'),
    url(r'^collection/(?P<collection_id>\d+)/edit/$', views.add_collection, name='collection.edit'),

    url(r'accounts/', include('scielomanager.accounts.urls')),

    (r'^i18n/', include('django.conf.urls.i18n')),

    # Trash
    url(r'^trash/$', views.trash_listing, name="trash.listing"),
    url(r'^trash/bulk_action/(?P<model_name>\w+)/(?P<action_name>\w+)/(?P<value>\w+)/$',
        views.generic_bulk_action, name='trash.bulk_action'),

    #API version 1
    (r'^api/', include(v1_api.urls)),

    (r'^export/', include('scielomanager.export.urls')),
)

if settings.DEBUG:

    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
        )
