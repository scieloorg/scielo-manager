# coding: utf-8
import logging

from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from tastypie.resources import ModelResource, Resource
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
)

from articletrack.models import (
    Checkin,
    Notice,
    Article as CheckinArticle,
    Ticket,
    Comment
)

logger = logging.getLogger(__name__)

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
    thematic_titles = fields.CharField(readonly=True)
    is_press_release = fields.BooleanField(readonly=True)

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

        if 'collection' in filters:
            issues = Issue.objects.filter(
                journal__collection__name_slug=filters['collection'])
            orm_filters['pk__in'] = issues

        if 'eletronic_issn' in filters:
            issues = Issue.objects.filter(
                journal__eletronic_issn=filters['eletronic_issn'])
            orm_filters['pk__in'] = issues

        if 'print_issn' in filters:
            issues = Issue.objects.filter(
                journal__print_issn=filters['print_issn'])
            orm_filters['pk__in'] = issues

        return orm_filters

    def dehydrate_thematic_titles(self, bundle):
        return dict([title.language.iso_code, title.title]
            for title in bundle.obj.issuetitle_set.all())

    def dehydrate_is_press_release(self, bundle):
        return False


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
    collections = fields.ManyToManyField(CollectionResource, 'collections')
    issues = fields.OneToManyField(IssueResource, 'issue_set')
    sections = fields.OneToManyField(SectionResource, 'section_set')
    pub_status_history = fields.ListField(readonly=True)
    contact = fields.DictField(readonly=True)
    study_areas = fields.ListField(readonly=True)
    pub_status = fields.CharField(readonly=True)
    pub_status_reason = fields.CharField(readonly=True)

    #recursive field
    previous_title = fields.ForeignKey('self', 'previous_title', null=True)

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
        return [(mission.language.iso_code, mission.description)
            for mission in bundle.obj.missions.all()]

    def dehydrate_other_titles(self, bundle):
        return [(title.category, title.title)
            for title in bundle.obj.other_titles.all()]

    def dehydrate_languages(self, bundle):
        return [language.iso_code
            for language in bundle.obj.languages.all()]

    def dehydrate_pub_status_history(self, bundle):
        return [{'date': event.since,
                'status': event.status}
            for event in bundle.obj.statuses.order_by('-since').all()]

    def dehydrate_study_areas(self, bundle):
        return [area.study_area
            for area in bundle.obj.study_areas.all()]

    def dehydrate_collections(self, bundle):
        """Only works com v1, without multiple collections per journal.
        """
        try:
            return bundle.data['collections'][0]
        except IndexError:
            return ''

    def dehydrate_pub_status(self, bundle):
        col = bundle.obj.collections.get()
        return bundle.obj.membership_info(col, 'status')

    def dehydrate_pub_status_reason(self, bundle):
        col = bundle.obj.collections.get()
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
            'suppl_volume': issue.suppl_volume,
            'suppl_number': issue.suppl_number,
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


class CheckinResource(ModelResource):
    article = fields.ForeignKey('api.resources.CheckinArticleResource', 'article')

    class Meta(ApiKeyAuthMeta):
        queryset = Checkin.objects.all()
        resource_name = 'checkins'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']


class CheckinNoticeResource(ModelResource):
    checkin = fields.ForeignKey(CheckinResource, 'checkin')

    class Meta(ApiKeyAuthMeta):
        queryset = Notice.objects.all()
        resource_name = 'notices'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']


class CheckinArticleResource(ModelResource):
    journals = fields.ToManyField(JournalResource, 'journals', null=True)

    class Meta(ApiKeyAuthMeta):
        queryset = CheckinArticle.objects.all()
        resource_name = 'checkins_articles'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']

    def obj_create(self, bundle, **kwargs):
        bundle = super(CheckinArticleResource, self).obj_create(bundle, **kwargs)

        pissn = bundle.data.get('pissn', '')
        eissn = bundle.data.get('eissn', '')

        try:
            journal = Journal.objects.get(
                Q(print_issn=pissn) | Q(eletronic_issn=eissn)
            )
        except ObjectDoesNotExist:
            message = u"""Could not find the right Journal instance to bind with
                          %s. The Journal instance will stay in an orphan state.""".strip()
            logger.error(message % repr(bundle.obj))
        else:
            bundle.obj.journals.add(journal)

        return bundle

class TicketResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author')
    article = fields.ForeignKey(CheckinArticleResource, 'article')

    class Meta(ApiKeyAuthMeta):
        queryset = Ticket.objects.all()
        resource_name = 'tickets'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']


class CommentResource(ModelResource):
    author = fields.ForeignKey(UserResource, 'author')
    ticket = fields.ForeignKey(TicketResource, 'ticket')

    class Meta(ApiKeyAuthMeta):
        queryset = Comment.objects.all()
        resource_name = 'comments'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']


class ArticleResource(ModelResource):
    issue = fields.ForeignKey(IssueResource, 'issue')

    class Meta(ApiKeyAuthMeta):
        queryset = Article.objects.all()
        resource_name = 'articles'
        default_format = "application/json"
        allowed_methods = ['get', 'post', 'put']
