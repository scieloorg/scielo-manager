
from tastypie import fields
from django.contrib.auth.models import User
from tastypie.resources import ModelResource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication

from journalmanager import models


class ApiKeyAuthMeta:
    authentication = ApiKeyAuthentication()
    authorization = DjangoAuthorization()


class UseLicenseResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = models.UseLicense.objects.all()
        resource_name = 'uselicenses'
        allowed_methods = ['get', ]


class SponsorResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = models.Sponsor.objects.all()
        resource_name = 'sponsors'
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


class CollectionResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        queryset = models.Collection.objects.all()
        resource_name = 'collections'
        allowed_methods = ['get', ]


class SectionResource(ModelResource):
    journal = fields.ForeignKey('api.resources.JournalResource',
        'journal')
    issues = fields.OneToManyField('api.resources.IssueResource',
        'issue_set')
    titles = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = models.Section.objects.all()
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
    thematic_titles = fields.CharField(readonly=True)
    is_press_release = fields.BooleanField(readonly=True)
    suppl_volume = fields.CharField(attribute='volume', readonly=True)
    suppl_number = fields.CharField(attribute='number', readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = models.Issue.objects.all()
        resource_name = 'issues'
        allowed_methods = ['get', ]
        filtering = {
            "journal": ('exact'),
            "is_marked_up": ('exact'),
            "volume": ('exact'),
            "number": ('exact'),
            "publication_year": ('exact'),
            "suppl_number": ('exact'),
            "suppl_volume": ('exact')
        }

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the collection's name_slug.
        """
        if filters is None:
            filters = {}
        orm_filters = super(IssueResource, self).build_filters(filters)

        param_filters = {}

        if 'collection' in filters:
            param_filters['journal__collections__name_slug'] = filters['collection']

        if 'eletronic_issn' in filters:
            param_filters['journal__eletronic_issn'] = filters['eletronic_issn']

        if 'print_issn' in filters:
            param_filters['journal__print_issn'] = filters['print_issn']

        if 'suppl_number' in filters:
            param_filters['type'] = 'supplement'
            param_filters['number'] = filters['suppl_number']

        if 'suppl_volume' in filters:
            param_filters['type'] = 'supplement'
            param_filters['number'] = ''
            param_filters['volume'] = filters['suppl_volume']

        issues = models.Issue.objects.filter(**param_filters)

        orm_filters['pk__in'] = issues

        return orm_filters

    def dehydrate_thematic_titles(self, bundle):
        return dict([title.language.iso_code, title.title]
            for title in bundle.obj.issuetitle_set.all())

    def dehydrate_is_press_release(self, bundle):
        return False

    def dehydrate_suppl_volume(self, bundle):
        if bundle.obj.type == 'supplement':
            return bundle.obj.suppl_text if bundle.obj.volume else ''
        else:
            return ''

    def dehydrate_suppl_number(self, bundle):
        if bundle.obj.type == 'supplement':
            return bundle.obj.suppl_text if bundle.obj.number else ''
        else:
            return ''


class JournalResource(ModelResource):
    missions = fields.CharField(readonly=True)
    other_titles = fields.CharField(readonly=True)
    abstract_keyword_languages = fields.CharField(readonly=True)
    languages = fields.CharField(readonly=True)
    pub_status_history = fields.ListField(readonly=True)
    contact = fields.DictField(readonly=True)
    study_areas = fields.ListField(readonly=True)
    pub_status = fields.CharField(readonly=True)
    pub_status_reason = fields.CharField(readonly=True)

    creator = fields.ForeignKey(UserResource, 'creator')
    use_license = fields.ForeignKey(UseLicenseResource, 'use_license', full=True)
    sponsors = fields.ManyToManyField(SponsorResource, 'sponsor')
    collections = fields.ManyToManyField(CollectionResource, 'collections')
    issues = fields.OneToManyField(IssueResource, 'issue_set')

    #recursive field
    previous_title = fields.ForeignKey('self', 'previous_title', null=True)
    succeeding_title = fields.ForeignKey('self', 'succeeding_title', null=True)

    class Meta(ApiKeyAuthMeta):
        queryset = models.Journal.objects.all().filter()
        resource_name = 'journals'
        allowed_methods = ['get', ]
        filtering = {
            'is_trashed': ('exact',),
            'eletronic_issn': ('exact',),
            'print_issn': ('exact',),
        }

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data filter by collection and pubstatus.
        """
        if filters is None:
            filters = {}
        else:
            query_filters = {}

        orm_filters = super(JournalResource, self).build_filters(filters)

        if 'collection' in filters:
            query_filters['collections__name_slug'] = filters['collection']

        if 'pubstatus' in filters:
            query_filters['membership__status__in'] = filters.getlist('pubstatus')

        journals = models.Journal.objects.filter(**query_filters)

        orm_filters['pk__in'] = journals

        return orm_filters

    def dehydrate_missions(self, bundle):
        return [(mission.language.iso_code, mission.description)
            for mission in bundle.obj.missions.all()]



