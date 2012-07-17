# coding: utf-8
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie import fields

from journalmanager.models import (
    Journal,
    UseLicense,
    Sponsor,
    Publisher,
    Collection,
    Issue,
    Section,
)


class SectionResource(ModelResource):
    journal = fields.ForeignKey('api.resources.JournalResource',
        'journal')
    issues = fields.OneToManyField('api.resources.IssueResource',
        'issue_set')
    titles = fields.CharField(readonly=True)

    class Meta:
        queryset = Section.objects.all()
        resource_name = 'sections'
        allowed_methods = ['get',]

    def dehydrate_titles(self, bundle):
        return [(title.language.iso_code, title.title)
            for title in bundle.obj.sectiontitle_set.all()]


class IssueResource(ModelResource):
    journal = fields.ForeignKey('api.resources.JournalResource',
        'journal')
    sections = fields.ManyToManyField(SectionResource, 'section')

    class Meta:
        queryset = Issue.objects.all()
        resource_name = 'issues'
        allowed_methods = ['get',]


class CollectionResource(ModelResource):
    class Meta:
        queryset = Collection.objects.all()
        resource_name = 'collections'
        allowed_methods = ['get',]


class PublisherResource(ModelResource):
    class Meta:
        queryset = Publisher.objects.all()
        resource_name = 'publishers'
        allowed_methods = ['get',]


class SponsorResource(ModelResource):
    class Meta:
        queryset = Sponsor.objects.all()
        resource_name = 'sponsors'
        allowed_methods = ['get',]


class UseLicenseResource(ModelResource):
    class Meta:
        queryset = UseLicense.objects.all()
        resource_name = 'uselicenses'
        allowed_methods = ['get',]


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'users'
        allowed_methods = ['get',]
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
    publishers = fields.ForeignKey(PublisherResource, 'publisher')
    collections = fields.ManyToManyField(CollectionResource, 'collections')
    issues = fields.OneToManyField(IssueResource, 'issue_set')
    pub_status_history = fields.ListField(readonly=True)
    contact = fields.DictField(readonly=True)

    class Meta:
        queryset = Journal.objects.all().filter()
        resource_name = 'journals'
        allowed_methods = ['get',]
        filtering = {
            'is_trashed': ('exact',),
        }

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

    def dehydrate_contact(self, bundle):
        return {
            'name': bundle.obj.publisher.name,
            'email': bundle.obj.publisher.email,
        }