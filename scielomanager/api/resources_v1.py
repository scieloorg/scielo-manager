# coding: utf-8
import logging

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie.resources import ModelResource
from tastypie import fields
from tastypie.contrib.contenttypes.fields import GenericForeignKeyField
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.authorization import Authorization

from journalmanager.models import (
    Journal,
    UseLicense,
    Sponsor,
    Collection,
    Issue,
    Section,
    DataChangeEvent,
    RegularPressRelease,
    AheadPressRelease,
    PressReleaseTranslation,
    PressReleaseArticle,
    Article,
    SubjectCategory,
)

from scielomanager.utils import usercontext


logger = logging.getLogger(__name__)


def current_user_active_collection():
    return usercontext.get_finder().get_current_user_active_collection()


def current_user_collections():
    return usercontext.get_finder().get_current_user_collections()


class ApiKeyAuthMeta:
    authentication = ApiKeyAuthentication()
    authorization = DjangoAuthorization()


class SectionResource(ModelResource):
    journal = fields.ForeignKey('api.resources_v1.JournalResource',
        'journal')
    issues = fields.OneToManyField('api.resources_v1.IssueResource',
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
    """
    IMPORTANT: is_press_release was removed on V2
    """
    journal = fields.ForeignKey('api.resources_v1.JournalResource',
        'journal')
    sections = fields.ManyToManyField(SectionResource, 'section')
    thematic_titles = fields.CharField(readonly=True)
    is_press_release = fields.BooleanField(readonly=True)
    suppl_volume = fields.CharField(attribute='volume', readonly=True)
    suppl_number = fields.CharField(attribute='number', readonly=True)

    class Meta(ApiKeyAuthMeta):
        queryset = Issue.objects.all()
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

        issues = Issue.objects.filter(**param_filters)

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


class CollectionResource(ModelResource):

    class Meta(ApiKeyAuthMeta):
        queryset = Collection.objects.all()
        resource_name = 'collections'
        allowed_methods = ['get', ]

class SubjectCategoryResource(ModelResource):
    class Meta(ApiKeyAuthMeta):
        queryset = SubjectCategory.objects.all()
        resource_name = 'subjectcategory'
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
    collections = fields.ManyToManyField(CollectionResource, 'collections')
    issues = fields.OneToManyField(IssueResource, 'issue_set')
    sections = fields.OneToManyField(SectionResource, 'section_set')
    subject_categories = fields.ManyToManyField(SubjectCategoryResource, 'subject_categories', readonly=True)
    pub_status_history = fields.ListField(readonly=True)
    contact = fields.DictField(readonly=True)
    study_areas = fields.ListField(readonly=True)
    pub_status = fields.CharField(readonly=True)
    pub_status_reason = fields.CharField(readonly=True)

    #recursive field
    previous_title = fields.ForeignKey('self', 'previous_title', null=True)
    succeeding_title = fields.ForeignKey('self', 'succeeding_title', null=True)

    class Meta(ApiKeyAuthMeta):
        queryset = Journal.objects.all().filter()
        resource_name = 'journals'
        allowed_methods = ['get', ]
        filtering = {
            'is_trashed': ('exact',),
            'eletronic_issn': ('exact',),
            'print_issn': ('exact',),
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
                collections__name_slug=filters['collection'])
            orm_filters['pk__in'] = journals

        if 'pubstatus' in filters:
            # keep the previous filtering
            try:
                j = orm_filters['pk__in']
            except KeyError:
                j = Journal.objects

            statuses = filters.getlist('pubstatus')
            journals = j.filter(
                membership__status__in=statuses)
            orm_filters['pk__in'] = journals

        return orm_filters

    def dehydrate_missions(self, bundle):
        """
        IMPORTANT: Changed to dict on V2
            missions: {
                en: "To publish articles of clinical and experimental...",
                es: "Publicar artÃ­culos de estudios clÃ­nicos y experim...",
                pt: "Publicar artigos de estudos clÃ­nicos e experiment..."
            },
        """
        return [(mission.language.iso_code, mission.description)
            for mission in bundle.obj.missions.all()]

    def dehydrate_other_titles(self, bundle):
        """
        IMPORTANT: Changed to dict on V2
            other_titles: {
                other: "Arquivos Brasileiros de Cirurgia Digestiva",
                paralleltitle: "Brazilian Archives of Digestive Surgery"
            },
        """
        return [(title.category, title.title)
            for title in bundle.obj.other_titles.all()]

    def dehydrate_languages(self, bundle):
        return [language.iso_code
            for language in bundle.obj.languages.all()]

    def dehydrate_subject_categories(self, bundle):
        return [subject_category.term
            for subject_category in bundle.obj.subject_categories.all()]

    def dehydrate_pub_status_history(self, bundle):
        return [{'date': event.since,
                'status': event.status}
            for event in bundle.obj.statuses.order_by('-since').all()]

    def dehydrate_study_areas(self, bundle):
        return [area.study_area
            for area in bundle.obj.study_areas.all()]

    def dehydrate_collections(self, bundle):
        """
        Only works with v1, without multiple collections per journal.
        IMPORTANT: This prepare function was removed from V2
        """
        try:
            return bundle.data['collections'][0]
        except IndexError:
            return ''

    def dehydrate_pub_status(self, bundle):
        try:
            col = bundle.obj.collections.get()
        except MultipleObjectsReturned:
            col = current_user_active_collection()

        return bundle.obj.membership_info(col, 'status')

    def dehydrate_pub_status_reason(self, bundle):
        try:
            col = bundle.obj.collections.get()
        except MultipleObjectsReturned:
            col = current_user_active_collection()

        return bundle.obj.membership_info(col, 'reason')


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


class PressReleaseTranslationResource(ModelResource):
    language = fields.CharField(readonly=True)

    class Meta(ApiKeyAuthMeta):
        resource_name = 'prtranslations'
        queryset = PressReleaseTranslation.objects.all()
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
        queryset = RegularPressRelease.objects.all()
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
            preleases = RegularPressRelease.objects.filter(
                articles__article_pid=filters['article_pid'])
            orm_filters['pk__in'] = preleases

        elif 'journal_pid' in filters:
            preleases = RegularPressRelease.objects.by_journal_pid(
                filters['journal_pid'])
            orm_filters['pk__in'] = preleases
        elif 'issue_pid' in filters:
            preleases = RegularPressRelease.objects.by_issue_pid(
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
        queryset = AheadPressRelease.objects.all()
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
            preleases = AheadPressRelease.objects.filter(
                articles__article_pid=filters['article_pid'])
            orm_filters['pk__in'] = preleases

        elif 'journal_pid' in filters:
            preleases = AheadPressRelease.objects.by_journal_pid(
                filters['journal_pid'])
            orm_filters['pk__in'] = preleases

        return orm_filters


class ArticleResource(ModelResource):
    issue = fields.ForeignKey(IssueResource, 'issue')

    class Meta(ApiKeyAuthMeta):
        queryset = Article.objects.all()
        resource_name = 'articles'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']
