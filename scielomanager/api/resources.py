# coding: utf-8
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization

from journalmanager.models import (
    Journal,
    UseLicense,
    Sponsor,
    Collection,
    Issue,
    Section,
    DataChangeEvent,
)


class ApiKeyAuthMeta:
    authentication = ApiKeyAuthentication()
    authorization = DjangoAuthorization()


class SectionResource(ModelResource):
    journal = fields.ForeignKey('api.resources.JournalResource',
        'journal')
    issues = fields.OneToManyField('api.resources.IssueResource',
        'issue_set')
    titles = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = Section.objects.all()
        resource_name = 'sections'
        allowed_methods = ['get']
        excludes = ['legacy_code']
        filtering = {
            "journal": ('exact'),
        }

    def dehydrate_titles(self, bundle):
        return [(title.language.iso_code, title.title)
            for title in bundle.obj.titles.all()]


class IssueResource(ModelResource):
    journal = fields.ForeignKey('api.resources.JournalResource',
        'journal')
    sections = fields.ManyToManyField(SectionResource, 'section')

    class Meta(ApiKeyAuthMeta):
        queryset = Issue.objects.all()
        resource_name = 'issues'
        allowed_methods = ['get', ]
        filtering = {
            "journal": ('exact'),
            "is_marked_up": ('exact'),
        }

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the collection's name_slug.
        """
        if filters is None:
            filters = {}

        orm_filters = super(IssueResource, self).build_filters(filters)

        if 'collection' in filters:
            issues = Issue.objects.filter(
                journal__collection__name_slug=filters['collection'])
            orm_filters['pk__in'] = issues

        return orm_filters


class CollectionResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        queryset = Collection.objects.all()
        resource_name = 'collections'
        allowed_methods = ['get', ]


class SponsorResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = Sponsor.objects.all()
        resource_name = 'sponsors'
        allowed_methods = ['get', ]


class UseLicenseResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = UseLicense.objects.all()
        resource_name = 'uselicenses'
        allowed_methods = ['get', ]


class UserResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = User.objects.all()
        resource_name = 'users'
        allowed_methods = ['get', ]
        excludes = [
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        ]


class JournalResource(ModelResource):
    missions = fields.CharField(readonly=True)
    other_titles = fields.CharField(readonly=True)
    creator = fields.ForeignKey(UserResource, 'creator')
    abstract_keyword_languages = fields.CharField(readonly=True)
    languages = fields.CharField(readonly=True)
    use_license = fields.ForeignKey(UseLicenseResource, 'use_license', full=True)
    sponsors = fields.ManyToManyField(SponsorResource, 'sponsor')
    collections = fields.ForeignKey(CollectionResource, 'collection')
    issues = fields.OneToManyField(IssueResource, 'issue_set')
    sections = fields.OneToManyField(SectionResource, 'section_set')
    pub_status_history = fields.ListField(readonly=True)
    contact = fields.DictField(readonly=True)
    study_areas = fields.ListField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = Journal.objects.all().filter()
        resource_name = 'journals'
        allowed_methods = ['get', ]
        filtering = {
            'is_trashed': ('exact',),
        }

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the collection's name_slug.
        """
        if filters is None:
            filters = {}

        orm_filters = super(JournalResource, self).build_filters(filters)

        if 'collection' in filters:
            journals = Journal.objects.filter(
                collection__name_slug=filters['collection'])
            orm_filters['pk__in'] = journals

        return orm_filters

    def dehydrate_missions(self, bundle):
        return [(mission.language.iso_code, mission.description)
            for mission in bundle.obj.missions.all()]

    def dehydrate_other_titles(self, bundle):
        return [(title.category, title.title)
            for title in bundle.obj.other_titles.all()]

    def dehydrate_languages(self, bundle):
        return [language.iso_code
            for language in bundle.obj.languages.all()]

    def dehydrate_pub_status_history(self, bundle):
        return [{'date': event.created_at,
                'status': event.status}
            for event in bundle.obj.status_history.order_by('-created_at').all()]

    def dehydrate_study_areas(self, bundle):
        return [area.study_area
            for area in bundle.obj.study_areas.all()]


class DataChangeEventResource(ModelResource):
    collection_uri = fields.ForeignKey(CollectionResource, 'collection')
    seq = fields.IntegerField(attribute='pk', readonly=True)
    object_uri = GenericForeignKeyField({
        Journal: JournalResource,
        Issue: IssueResource,
    }, 'content_object')

    class Meta(ApiKeyAuthMeta):
        resource_name = 'changes'
        queryset = DataChangeEvent.objects.all()
        excludes = [
            'object_id',
            'id',
        ]
        allowed_methods = ['get', ]

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the collection's name_slug.
        """
        if filters is None:
            filters = {}

        orm_filters = super(DataChangeEventResource, self).build_filters(filters)

        if 'since' in filters:
            events = DataChangeEvent.objects.filter(
                pk__gte=int(filters['since']))
            orm_filters['pk__in'] = events

        return orm_filters
