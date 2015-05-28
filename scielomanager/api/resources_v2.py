# coding: utf-8

import logging

from tastypie import fields
from django.db.models import Q
from django.contrib.auth.models import User
from tastypie.resources import ModelResource, Resource
from tastypie.authorization import DjangoAuthorization
from tastypie.authentication import ApiKeyAuthentication
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from journalmanager import models
from editorialmanager import models as em_models


logger = logging.getLogger(__name__)


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
    collections = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = User.objects.all()
        resource_name = 'users'
        allowed_methods = ['get', ]
        excludes = [
            'username',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
        ]

    def dehydrate_collections(self, bundle):
        return [{'name': col.collection.name,
                 'is_default': col.is_default,
                 'is_manager': col.is_manager}
                for col in bundle.obj.usercollections_set.all()]

    def dehydrate(self, bundle):
        bundle.data['username'] = bundle.obj.username

        return bundle


class CollectionResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        queryset = models.Collection.objects.all()
        resource_name = 'collections'
        allowed_methods = ['get', ]


class SubjectCategoryResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = models.SubjectCategory.objects.all()
        resource_name = 'subjectcategory'
        allowed_methods = ['get', ]


class SectionResource(ModelResource):
    journal = fields.ForeignKey('api.resources_v2.JournalResource', 'journal')
    issues = fields.OneToManyField('api.resources_v2.IssueResource', 'issue_set')
    titles = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = models.Section.objects.all()
        resource_name = 'sections'
        allowed_methods = ['get']
        excludes = ['legacy_code']
        filtering = {
            "journal": ('exact'),
        }

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by journal eletronic_issn and print_issn.
        """
        if filters is None:
            filters = {}

        orm_filters = super(SectionResource, self).build_filters(filters)

        param_filters = {}

        if 'journal_eissn' in filters:
            param_filters['journal__eletronic_issn'] = filters['journal_eissn']

        if 'journal_pissn' in filters:
            param_filters['journal__print_issn'] = filters['journal_pissn']

        sections = models.Section.objects.filter(**param_filters)

        orm_filters['pk__in'] = sections

        return orm_filters

    def dehydrate_titles(self, bundle):
        return dict([title.language.iso_code, title.title]
            for title in bundle.obj.titles.all())


class IssueResource(ModelResource):
    journal = fields.ForeignKey('api.resources_v2.JournalResource', 'journal')
    sections = fields.ManyToManyField(SectionResource, 'section')
    thematic_titles = fields.CharField(readonly=True)
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
        Custom filter that retrieves data filter by collection_slug, eletronic_issn,
        print_issn, suppl_volume e suppl_number
        """
        if filters is None:
            filters = {}

        orm_filters = super(IssueResource, self).build_filters(filters)

        query_filters = {}

        if 'collection' in filters:
            query_filters['journal__collections__name_slug'] = filters['collection']

        if 'eletronic_issn' in filters:
            query_filters['journal__eletronic_issn'] = filters['eletronic_issn']

        if 'print_issn' in filters:
            query_filters['journal__print_issn'] = filters['print_issn']

        if 'suppl_number' in filters:
            query_filters['type'] = 'supplement'
            query_filters['number'] = filters['suppl_number']

        if 'suppl_volume' in filters:
            query_filters['type'] = 'supplement'
            query_filters['number'] = ''
            query_filters['volume'] = filters['suppl_volume']

        issues = models.Issue.objects.filter(**query_filters)

        orm_filters['pk__in'] = issues

        return orm_filters

    def dehydrate_thematic_titles(self, bundle):
        return dict([title.language.iso_code, title.title] for title in bundle.obj.issuetitle_set.all())

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

    def dehydrate_sections(self, bundle):
        section_list = []

        for section in bundle.obj.section.all():
            section_list.append(
                {'code': section.code,
                 'titles': [{'lang': ti.language.iso_code, 'title': ti.title} for ti in section.titles.all()]
                 }
            )

        return section_list


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

    # Relation fields
    creator = fields.ForeignKey(UserResource, 'creator')
    use_license = fields.ForeignKey(UseLicenseResource, 'use_license', full=True)
    sponsors = fields.ManyToManyField(SponsorResource, 'sponsor')
    collections = fields.ManyToManyField(CollectionResource, 'collections')
    issues = fields.OneToManyField(IssueResource, 'issue_set')
    sections = fields.OneToManyField(SectionResource, 'section_set')
    subject_categories = fields.ManyToManyField(SubjectCategoryResource,
                                                'subject_categories', readonly=True)

    # Recursive field
    previous_title = fields.ForeignKey('self', 'previous_title', null=True)
    succeeding_title = fields.ForeignKey('self', 'succeeding_title', null=True)

    class Meta(ApiKeyAuthMeta):
        queryset = models.Journal.objects.all()
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
        return {mission.language.iso_code: mission.description
                for mission in bundle.obj.missions.all()}

    def dehydrate_other_titles(self, bundle):
        return {title.category: title.title
            for title in bundle.obj.other_titles.all()}

    def dehydrate_languages(self, bundle):
        return [language.iso_code
            for language in bundle.obj.languages.all()]

    def dehydrate_pub_status_history(self, bundle):
        return [{'date': event.since,
                'status': event.status}
            for event in bundle.obj.statuses.order_by('-since').all()]

    def dehydrate_study_areas(self, bundle):
        return [area.study_area for area in bundle.obj.study_areas.all()]

    def dehydrate_pub_status(self, bundle):
        return {col.name: bundle.obj.membership_info(col, 'status')
            for col in bundle.obj.collections.all()}

    def dehydrate_pub_status_reason(self, bundle):
        return {col.name: bundle.obj.membership_info(col, 'reason')
            for col in bundle.obj.collections.all()}

    def dehydrate_collections(self, bundle):
        return [col.name for col in bundle.obj.collections.all()]

    def dehydrate_subject_categories(self, bundle):
        return [subject_category.term
            for subject_category in bundle.obj.subject_categories.all()]


class DataChangeEventResource(ModelResource):
    collection_uri = fields.ForeignKey(CollectionResource, 'collection')
    seq = fields.IntegerField(attribute='pk', readonly=True)
    object_uri = GenericForeignKeyField({
        models.Journal: JournalResource,
        models.Issue: IssueResource,
    }, 'content_object')

    class Meta(ApiKeyAuthMeta):
        resource_name = 'changes'
        queryset = models.DataChangeEvent.objects.all()
        excludes = [
            'object_id',
            'id',
        ]
        allowed_methods = ['get', ]

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by since.
        """
        if filters is None:
            filters = {}

        query_filters = {}

        orm_filters = super(DataChangeEventResource, self).build_filters(filters)

        if 'since' in filters:
            query_filters['pk__gte'] = int(filters['since'])

        orm_filters['pk__in'] = models.DataChangeEvent.objects.filter(**query_filters)

        return orm_filters


class PressReleaseTranslationResource(ModelResource):
    language = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        resource_name = 'prtranslations'
        queryset = models.PressReleaseTranslation.objects.all()
        allowed_methods = ['get', ]

    def dehydrate_language(self, bundle):
        return bundle.obj.language.iso_code


class PressReleaseResource(ModelResource):
    issue_uri = fields.ForeignKey(IssueResource, 'issue')
    translations = fields.OneToManyField(PressReleaseTranslationResource,
                                         'translations',
                                         full=True)
    articles = fields.CharField(readonly=True)
    issue_meta = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        resource_name = 'pressreleases'
        queryset = models.RegularPressRelease.objects.all()
        allowed_methods = ['get', ]
        ordering = ['id']

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the article PID.
        """
        if filters is None:
            filters = {}

        orm_filters = super(PressReleaseResource, self).build_filters(filters)

        if 'article_pid' in filters:
            preleases = models.RegularPressRelease.objects.filter(
                articles__article_pid=filters['article_pid'])
            orm_filters['pk__in'] = preleases

        elif 'journal_pid' in filters:
            preleases = models.RegularPressRelease.objects.by_journal_pid(
                filters['journal_pid'])
            orm_filters['pk__in'] = preleases

        elif 'issue_pid' in filters:
            preleases = models.RegularPressRelease.objects.by_issue_pid(
                filters['issue_pid'])
            orm_filters['pk__in'] = preleases

        return orm_filters

    def dehydrate_articles(self, bundle):
        return [art.article_pid for art in bundle.obj.articles.all()]

    def dehydrate_issue_meta(self, bundle):
        issue = bundle.obj.issue

        meta_data = {
            'scielo_pid': issue.scielo_pid,
            'short_title': issue.journal.short_title,
            'volume': issue.volume,
            'number': issue.number,
            'suppl_volume': issue.suppl_text if issue.type == 'supplement' and issue.volume else '',
            'suppl_number': issue.suppl_text if issue.type == 'supplement' and issue.number else '',
            'publication_start_month': issue.publication_start_month,
            'publication_end_month': issue.publication_end_month,
            'publication_city': issue.journal.publication_city,
            'publication_year': issue.publication_year,
        }

        return meta_data


class AheadPressReleaseResource(ModelResource):
    journal_uri = fields.ForeignKey(JournalResource, 'journal')
    translations = fields.OneToManyField(PressReleaseTranslationResource,
                                         'translations',
                                         full=True)
    articles = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        resource_name = 'apressreleases'
        queryset = models.AheadPressRelease.objects.all()
        allowed_methods = ['get', ]

    def dehydrate_articles(self, bundle):
        return [art.article_pid for art in bundle.obj.articles.all()]

    def build_filters(self, filters=None):
        """
        Custom filter that retrieves data by the article PID.
        """
        if filters is None:
            filters = {}

        orm_filters = super(AheadPressReleaseResource, self).build_filters(filters)

        if 'article_pid' in filters:
            preleases = models.AheadPressRelease.objects.filter(
                articles__article_pid=filters['article_pid'])
            orm_filters['pk__in'] = preleases

        elif 'journal_pid' in filters:
            preleases = models.AheadPressRelease.objects.by_journal_pid(
                filters['journal_pid'])
            orm_filters['pk__in'] = preleases

        return orm_filters


class EditorialBoardResource(ModelResource):
    issue = fields.ToOneField(IssueResource, 'issue')

    class Meta(ApiKeyAuthMeta):
        resource_name = 'editorialboard'
        queryset = em_models.EditorialBoard.objects.all()
        allowed_methods = ['get', ]


class RoleTypeResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        resource_name = 'roletype'
        queryset = em_models.RoleType.objects.all()
        allowed_methods = ['get', ]
        ordering = ('name', )


class EditorialMemberResource(ModelResource):
    role = fields.ForeignKey(RoleTypeResource, 'role')
    board = fields.ForeignKey(EditorialBoardResource, 'board')

    class Meta(ApiKeyAuthMeta):
        resource_name = 'editorialmember'
        queryset = em_models.EditorialMember.objects.all()
        allowed_methods = ['get', ]
        ordering = ('board', 'order', 'pk')


class LanguageResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        resource_name = 'language'
        queryset = models.Language.objects.all()
        allowed_methods = ['get', ]
        ordering = ('name', )


class RoleTypeTranslationResource(ModelResource):
    role = fields.ForeignKey(RoleTypeResource, 'role')
    language = fields.ForeignKey(LanguageResource, 'language')

    class Meta(ApiKeyAuthMeta):
        resource_name = 'roletypetranslation'
        queryset = em_models.RoleTypeTranslation.objects.all()
        allowed_methods = ['get', ]
