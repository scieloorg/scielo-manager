# -*- encoding: utf-8 -*-
import urllib
import hashlib
import logging
import choices
import caching.base
import tools

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from django.db import (
    models,
    transaction,
    IntegrityError,
    DatabaseError,
    )
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.template.defaultfilters import slugify
from scielo_extensions import modelfields
from tastypie.models import create_api_key

from scielomanager.utils import base28
from scielomanager.journalmanager import modelmanagers

User.__bases__ = (caching.base.CachingMixin, models.Model)
User.add_to_class('objects', caching.base.CachingManager())

logger = logging.getLogger(__name__)

EVENT_TYPES = [(ev_type, ev_type) for ev_type in ['added', 'deleted', 'updated']]


def get_user_collections(user_id):
    """
    Return all the collections of a given user, The returned collections are the collections where the
    user could have access by the collections bar.
    """
    user_collections = User.objects.get(pk=user_id).usercollections_set.all().order_by(
        'collection__name')

    return user_collections


class AppCustomManager(caching.base.CachingManager):
    """
    Domain specific model managers.
    """

    def available(self, is_available=True):
        """
        Filter the queryset based on its availability.
        """
        data_queryset = self.get_query_set()

        if not isinstance(is_available, bool):
            try:
                if int(is_available) == 0:
                    is_available = False
                else:
                    is_available = True
            except (ValueError, TypeError):
                is_available = True

        data_queryset = data_queryset.filter(is_trashed=not is_available)

        return data_queryset


class JournalCustomManager(AppCustomManager):

    def all_by_user(self, user, is_available=True, pub_status=None):
        """
        Retrieves all the user's journals, contextualized by
        their default collection.
        """
        default_collection = Collection.objects.get_default_by_user(user)

        objects_all = self.available(is_available).filter(
            collection=default_collection).distinct()

        if pub_status:
            if pub_status in [stat[0] for stat in choices.JOURNAL_PUBLICATION_STATUS]:
                objects_all = objects_all.filter(pub_status=pub_status)

        return objects_all

    def recents_by_user(self, user):
        """
        Retrieves the recently modified objects related to the given user.
        """
        default_collection = Collection.objects.get_default_by_user(user)

        recents = self.filter(
            collection=default_collection).distinct().order_by('-updated')[:5]

        return recents

    def all_by_collection(self, collection, is_available=True):
        objects_all = self.available(is_available).filter(
            collection=collection)
        return objects_all


class SectionCustomManager(AppCustomManager):

    def all_by_user(self, user, is_available=True):
        default_collection = Collection.objects.get_default_by_user(user)

        objects_all = self.available(is_available).filter(
            journal__collection=default_collection).distinct()

        return objects_all


class IssueCustomManager(AppCustomManager):

    def all_by_collection(self, collection, is_available=True):
        objects_all = self.available(is_available).filter(
            journal__collection=collection)

        return objects_all


class InstitutionCustomManager(AppCustomManager):
    """
    Add capabilities to Institution subclasses to retrieve querysets
    based on user's collections.
    """
    def all_by_user(self, user, is_available=True):
        default_collection = Collection.objects.get_default_by_user(user)

        objects_all = self.available(is_available).filter(
            collections__in=[default_collection]).distinct()

        return objects_all


class CollectionCustomManager(AppCustomManager):

    def all_by_user(self, user):
        """
        Returns all the Collections related to the given
        user.
        """
        collections = self.filter(usercollections__user=user).order_by(
            'name')

        return collections

    def get_default_by_user(self, user):
        """
        Returns the Collection marked as default by the given user.
        If none satisfies this condition, the first
        instance is then returned.

        Like any manager method that does not return Querysets,
        `get_default_by_user` raises DoesNotExist if there is no
        result for the given parameter.
        """
        collections = self.filter(usercollections__user=user,
            usercollections__is_default=True).order_by('name')

        if not collections.count():
            try:
                collection = self.all_by_user(user)[0]
            except IndexError:
                raise Collection.DoesNotExist()
            else:
                collection.make_default_to_user(user)
                return collection

        return collections[0]

    def get_managed_by_user(self, user):
        """
        Returns all collections managed by a given user.
        """
        collections = self.filter(usercollections__user=user,
            usercollections__is_manager=True).order_by('name')

        return collections


class RegularPressReleaseCustomManager(caching.base.CachingManager):

    def by_journal_pid(self, journal_pid):
        """
        Returns all PressReleases related to a Journal, given its
        PID.
        """
        try:
            journal = Journal.objects.get(
                models.Q(print_issn=journal_pid) | models.Q(eletronic_issn=journal_pid))
            issues_pks = [iss.pk for iss in journal.issue_set.all()]
        except Journal.DoesNotExist:
            # little hack to act as .filter, returning an empty
            # queryset bound to the model.
            issues_pks = [None]

        preleases = self.filter(issue__pk__in=issues_pks)
        return preleases

    def all_by_journal(self, journal):
        """
        Returns all PressReleases related to a Journal
        """
        preleases = self.filter(issue__journal=journal)
        return preleases

    def by_issue_pid(self, issue_pid):
        """
        Returns all PressReleases related to an Issue, given its
        PID.
        """
        issn_slice = slice(0, 9)
        year_slice = slice(9, 13)
        order_slice = slice(13, None)

        issn = issue_pid[issn_slice]
        year = issue_pid[year_slice]
        order = int(issue_pid[order_slice])

        preleases_qset = self.by_journal_pid(issn)
        return preleases_qset.filter(issue__publication_year=year).filter(issue__order=order)


class AheadPressReleaseCustomManager(caching.base.CachingManager):

    def by_journal_pid(self, journal_pid):
        """
        Returns all PressReleases related to a Journal, given its
        PID.
        """
        preleases = self.filter(models.Q(journal__print_issn=journal_pid) | models.Q(journal__eletronic_issn=journal_pid))
        return preleases


class Language(caching.base.CachingMixin, models.Model):
    """
    Represents ISO 639-1 Language Code and its language name in English. Django
    automaticaly translates language names, if you write them right.

    http://en.wikipedia.org/wiki/ISO_639-1_language_matrix
    """
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    iso_code = models.CharField(_('ISO 639-1 Language Code'), max_length=2)
    name = models.CharField(_('Language Name (in English)'), max_length=64)

    def __unicode__(self):
        return __(self.name)

    class Meta:
        ordering = ['name']


class UserProfile(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    user = models.OneToOneField(User)
    email = models.EmailField(_('E-mail'), blank=False, unique=True, null=False)

    @property
    def gravatar_id(self):
        return hashlib.md5(self.email.lower().strip()).hexdigest()

    @property
    def avatar_url(self):
        params = urllib.urlencode({'s': 18, 'd': 'mm'})
        return '{0}/avatar/{1}?{2}'.format(getattr(settings, 'GRAVATAR_BASE_URL',
            'https://secure.gravatar.com'), self.gravatar_id, params)

    def save(self, force_insert=False, force_update=False):
        self.user.email = self.email
        self.user.save()
        return super(UserProfile, self).save(force_insert, force_update)


class Collection(caching.base.CachingMixin, models.Model):
    objects = CollectionCustomManager()
    nocacheobjects = models.Manager()
    collection = models.ManyToManyField(User, related_name='user_collection',
        through='UserCollections', null=True, blank=True, )
    name = models.CharField(_('Collection Name'), max_length=128, db_index=True, )
    name_slug = models.SlugField(unique=True, db_index=True, blank=True, null=True)
    url = models.URLField(_('Instance URL'), )
    logo = models.ImageField(_('Logo'), upload_to='img/collections_logos', null=True, blank=True, )
    acronym = models.CharField(_('Sigla'), max_length=16, db_index=True, blank=True, )
    country = models.CharField(_('Country'), max_length=32,)
    state = models.CharField(_('State'), max_length=32, null=False, blank=True,)
    city = models.CharField(_('City'), max_length=32, null=False, blank=True,)
    address = models.TextField(_('Address'),)
    address_number = models.CharField(_('Number'), max_length=8,)
    address_complement = models.CharField(_('Complement'), max_length=128, null=False, blank=True,)
    zip_code = models.CharField(_('Zip Code'), max_length=16, null=True, blank=True, )
    phone = models.CharField(_('Phone Number'), max_length=16, null=False, blank=True, )
    fax = models.CharField(_('Fax Number'), max_length=16, null=False, blank=True, )
    email = models.EmailField(_('Email'), )

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']
        permissions = (("list_collection", "Can list Collections"),)

    def save(self, *args, **kwargs):
        self.name_slug = slugify(self.name)
        super(Collection, self).save(*args, **kwargs)

    def add_user(self, user, is_default=False, is_manager=False):
        """
        Add the user to the current collection.
        """
        UserCollections.objects.create(collection=self,
                                       user=user,
                                       is_default=is_default,
                                       is_manager=is_manager)

    def remove_user(self, user):
        """
        Removes the user from the current collection.
        If the user isn't already related to the given collection,
        it will do nothing, silently.
        """
        try:
            uc = UserCollections.objects.get(collection=self, user=user)
        except UserCollections.DoesNotExist:
            return None
        else:
            uc.delete()

    def make_default_to_user(self, user):
        """
        Makes the current collection, the user's default.
        """
        UserCollections.objects.filter(user=user).update(is_default=False)
        uc, created = UserCollections.objects.get_or_create(
            collection=self, user=user)
        uc.is_default = True
        uc.save()

    def is_default_to_user(self, user):
        """
        Returns a boolean value depending if the current collection
        is set as default to the given user.
        """
        try:
            uc = UserCollections.objects.get(collection=self, user=user)
            return uc.is_default
        except UserCollections.DoesNotExist:
            return False

    def is_managed_by_user(self, user):
        """
        Returns a boolean value depending if the current collection
        is managed by the given user.
        """
        try:
            uc = UserCollections.objects.get(collection=self, user=user)
            return uc.is_manager
        except UserCollections.DoesNotExist:
            return False


class UserCollections(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection)
    is_default = models.BooleanField(_('Is default'), default=False, null=False, blank=False)
    is_manager = models.BooleanField(_('Is manager of the collection?'), default=False, null=False,
        blank=False)

    class Meta:
        unique_together = ("user", "collection", )


class Institution(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = AppCustomManager()
    nocacheobjects = models.Manager()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(_('Institution Name'), max_length=256, db_index=True)
    complement = models.TextField(_('Institution Complements'), blank=True, default="")
    acronym = models.CharField(_('Sigla'), max_length=16, db_index=True, blank=True)
    country = models.CharField(_('Country'), max_length=32)
    state = models.CharField(_('State'), max_length=32, null=False, blank=True)
    city = models.CharField(_('City'), max_length=32, null=False, blank=True)
    address = models.TextField(_('Address'))
    address_number = models.CharField(_('Number'), max_length=8)
    address_complement = models.CharField(_('Address Complement'), max_length=128, null=False, blank=True)
    zip_code = models.CharField(_('Zip Code'), max_length=16, null=True, blank=True)
    phone = models.CharField(_('Phone Number'), max_length=16, null=False, blank=True)
    fax = models.CharField(_('Fax Number'), max_length=16, null=False, blank=True)
    cel = models.CharField(_('Cel Number'), max_length=16, null=False, blank=True)
    email = models.EmailField(_('E-mail'))
    is_trashed = models.BooleanField(_('Is trashed?'), default=False, db_index=True)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ['name']


class Sponsor(Institution):
    objects = InstitutionCustomManager()
    nocacheobjects = models.Manager()
    userobjects = modelmanagers.SponsorManager()

    collections = models.ManyToManyField(Collection)

    class Meta:
        permissions = (("list_sponsor", "Can list Sponsors"),)


class SubjectCategory(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = JournalCustomManager()
    nocacheobjects = models.Manager()

    term = models.CharField(_('Term'), max_length=256, db_index=True)

    def __unicode__(self):
        return self.term


class StudyArea(caching.base.CachingMixin, models.Model):

    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    study_area = models.CharField(_('Study Area'), max_length=256,
        choices=sorted(choices.SUBJECTS, key=lambda SUBJECTS: SUBJECTS[1]))

    def __unicode__(self):
        return self.study_area


class Journal(caching.base.CachingMixin, models.Model):
    """
    Represents a Journal that is managed by one SciELO Collection.

    `editor_address` references the institution who operates the
    process.
    `publisher_address` references the institution who is responsible
    for the Journal.
    """

    #Custom manager
    objects = JournalCustomManager()
    nocacheobjects = models.Manager()
    userobjects = modelmanagers.JournalManager()

    #Relation fields
    creator = models.ForeignKey(User, related_name='enjoy_creator', editable=False)
    sponsor = models.ManyToManyField('Sponsor', verbose_name=_('Sponsor'), related_name='journal_sponsor', null=True, blank=True)
    previous_title = models.ForeignKey('Journal', verbose_name=_('Previous title'), related_name='prev_title', null=True, blank=True)
    use_license = models.ForeignKey('UseLicense', verbose_name=_('Use license'))
    collection = models.ForeignKey('Collection', verbose_name=_('Collection'), related_name='journals')
    languages = models.ManyToManyField('Language',)
    national_code = models.CharField(_('National Code'), max_length=16, null=True, blank=True)
    abstract_keyword_languages = models.ManyToManyField('Language', related_name="abstract_keyword_languages", )
    subject_categories = models.ManyToManyField(SubjectCategory, verbose_name=_("Subject Categories"), related_name="journals", null=True)
    study_areas = models.ManyToManyField(StudyArea, verbose_name=_("Study Area"), related_name="journals_migration_tmp", null=True)

    #Fields
    current_ahead_documents = models.IntegerField(_('Total of ahead of print documents for the current year'), max_length=3, default=0, blank=True, null=True)
    previous_ahead_documents = models.IntegerField(_('Total of ahead of print documents for the previous year'), max_length=3, default=0, blank=True, null=True)
    twitter_user = models.CharField(_('Twitter User'), max_length=128, null=True, blank=True)
    title = models.CharField(_('Journal Title'), max_length=256, db_index=True)
    title_iso = models.CharField(_('ISO abbreviated title'), max_length=256, db_index=True)
    short_title = models.CharField(_('Short Title'), max_length=256, db_index=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    acronym = models.CharField(_('Acronym'), max_length=16, blank=False)
    scielo_issn = models.CharField(_('The ISSN used to build the Journal PID.'), max_length=16,
        choices=sorted(choices.SCIELO_ISSN, key=lambda SCIELO_ISSN: SCIELO_ISSN[1]))
    print_issn = models.CharField(_('Print ISSN'), max_length=9, db_index=True)
    eletronic_issn = models.CharField(_('Electronic ISSN'), max_length=9, db_index=True)
    subject_descriptors = models.CharField(_('Subject / Descriptors'), max_length=512)
    init_year = models.CharField(_('Initial Year'), max_length=4)
    init_vol = models.CharField(_('Initial Volume'), max_length=16)
    init_num = models.CharField(_('Initial Number'), max_length=16)
    final_year = models.CharField(_('Final Year'), max_length=4, null=True, blank=True)
    final_vol = models.CharField(_('Final Volume'), max_length=16, null=False, blank=True)
    final_num = models.CharField(_('Final Number'), max_length=16, null=False, blank=True)
    medline_title = models.CharField(_('Medline Title'), max_length=256, null=True, blank=True)
    medline_code = models.CharField(_('Medline Code'), max_length=64, null=True, blank=True)
    frequency = models.CharField(_('Frequency'), max_length=16,
        choices=sorted(choices.FREQUENCY, key=lambda FREQUENCY: FREQUENCY[1]))
    pub_status = models.CharField(_('Publication Status'), max_length=16, blank=True, null=True, default="inprogress",
        choices=choices.JOURNAL_PUBLICATION_STATUS)
    pub_status_reason = models.TextField(_('Why the journal status will change?'), blank=True, default="",)
    pub_status_changed_by = models.ForeignKey(User, related_name='pub_status_changed_by', editable=False)
    editorial_standard = models.CharField(_('Editorial Standard'), max_length=64,
        choices=sorted(choices.STANDARD, key=lambda STANDARD: STANDARD[1]))
    ctrl_vocabulary = models.CharField(_('Controlled Vocabulary'), max_length=64,
        choices=choices.CTRL_VOCABULARY)
    pub_level = models.CharField(_('Publication Level'), max_length=64,
        choices=sorted(choices.PUBLICATION_LEVEL, key=lambda PUBLICATION_LEVEL: PUBLICATION_LEVEL[1]))
    secs_code = models.CharField(_('SECS Code'), max_length=64, null=False, blank=True)
    copyrighter = models.CharField(_('Copyrighter'), max_length=254)
    url_online_submission = models.CharField(_('URL of online submission'), max_length=64, null=True, blank=True)
    url_journal = models.CharField(_('URL of the journal'), max_length=64, null=True, blank=True)
    notes = models.TextField(_('Notes'), max_length=254, null=True, blank=True)
    index_coverage = models.TextField(_('Index Coverage'), null=True, blank=True)
    cover = models.ImageField(_('Journal Cover'), upload_to='img/journal_cover/', null=True, blank=True)
    logo = models.ImageField(_('Journal Logo'), upload_to='img/journals_logos', null=True, blank=True)
    is_trashed = models.BooleanField(_('Is trashed?'), default=False, db_index=True)
    other_previous_title = models.CharField(_('Other Previous Title'), max_length=255, blank=True)
    editor_name = models.CharField(_('Editor Names'), max_length=512)
    editor_address = models.CharField(_('Editor Address'), max_length=512)
    editor_address_city = models.CharField(_('Editor City'), max_length=256)
    editor_address_state = models.CharField(_('Editor State/Province/Region'), max_length=128)
    editor_address_zip = models.CharField(_('Editor Zip/Postal Code'), max_length=64)
    editor_address_country = modelfields.CountryField(_('Editor Country'))
    editor_phone1 = models.CharField(_('Editor Phone 1'), max_length=32)
    editor_phone2 = models.CharField(_('Editor Phone 2'), null=True, blank=True, max_length=32)
    editor_email = models.EmailField(_('Editor E-mail'))
    publisher_name = models.CharField(_('Publisher Name'), max_length=256)
    publisher_country = modelfields.CountryField(_('Publisher Country'))
    publisher_state = models.CharField(_('Publisher State/Province/Region'), max_length=64)
    publication_city = models.CharField(_('Publication City'), max_length=64)
    is_indexed_scie = models.BooleanField(_('SCIE'), default=False)
    is_indexed_ssci = models.BooleanField(_('SSCI'), default=False)
    is_indexed_aehci = models.BooleanField(_('A&HCI'), default=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']
        permissions = (("list_journal", "Can list Journals"),)

    def change_publication_status(self, status, reason, changed_by):
        """
        Syntatic suggar for changing publication status.
        """
        self.pub_status = status
        self.pub_status_reason = reason
        self.pub_status_changed_by = changed_by
        self.save()

    def issues_as_grid(self, is_available=True):
        objects_all = self.issue_set.available(is_available).order_by(
            '-publication_year')

        grid = OrderedDict()

        for issue in objects_all:
            year_node = grid.setdefault(issue.publication_year, {})
            volume_node = year_node.setdefault(issue.volume, [])
            volume_node.append(issue)

        for year, volume in grid.items():
            for vol, issues in volume.items():
                issues.sort(key=lambda x: x.order)

        return grid

    def has_issues(self, issues):
        """
        Returns ``True`` if all the given issues are bound to the journal.

        ``issues`` is a list of Issue pk.
        """
        issues_to_test = set(int(issue) for issue in issues)
        bound_issues = set(issue.pk for issue in self.issue_set.all())

        return issues_to_test.issubset(bound_issues)

    def reorder_issues(self, new_order, publication_year, volume=None):
        """
        Make persistent the ordering received as a list of ``pk``,
        to all the issues in a given ``publication_year`` and ``volume``.

        The lenght of ``new_order`` must match with the subset of
        issues by ``publication_year`` and ``volume``.
        """
        filters = {'publication_year': publication_year}
        if volume:
            filters['volume'] = volume

        issues = self.issue_set.filter(**filters)

        issues_count = issues.count()
        new_order_count = len(new_order)

        if new_order_count != issues_count:
            raise ValueError('new_order lenght does not match. %s:%s' % (new_order_count, issues_count))

        with transaction.commit_on_success():
            for i, pk in enumerate(new_order):
                order = i + 1
                issue = issues.get(pk=pk)
                issue.order = order
                issue.save()

    @property
    def scielo_pid(self):
        """
        Returns the ISSN used as PID on SciELO public catalogs.
        """

        attr = u'print_issn' if self.scielo_issn == u'print' else u'eletronic_issn'
        return getattr(self, attr)


class JournalPublicationEvents(caching.base.CachingMixin, models.Model):
    """
    Records the status changes for a given Journal.

    Known status:
    * Current
    * Deceased
    * Suspended
    * In progress
    """
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    journal = models.ForeignKey(Journal, editable=False, related_name='status_history')
    status = models.CharField(_('Journal Status'), max_length=16,)
    reason = models.TextField(_('Reason'), blank=True, default="",)
    created_at = models.DateTimeField(_('Changed at'), auto_now_add=True)
    changed_by = models.ForeignKey(User, editable=False)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name = 'journal publication event'
        verbose_name_plural = 'Journal Publication Events'
        ordering = ['created_at']
        permissions = (("list_publication_events", "Can list Publication Events"),)


class JournalTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    journal = models.ForeignKey(Journal, related_name='other_titles')
    title = models.CharField(_('Title'), null=False, max_length=128)
    category = models.CharField(_('Title Category'), null=False, max_length=128, choices=sorted(choices.TITLE_CATEGORY, key=lambda TITLE_CATEGORY: TITLE_CATEGORY[1]))


class JournalMission(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    journal = models.ForeignKey(Journal, related_name='missions')
    description = models.TextField(_('Mission'))
    language = models.ForeignKey('Language', blank=False, null=True)


class UseLicense(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    license_code = models.CharField(_('License Code'), unique=True, null=False, blank=False, max_length=64)
    reference_url = models.URLField(_('License Reference URL'), null=True, blank=True)
    disclaimer = models.TextField(_('Disclaimer'), null=True, blank=True, max_length=512)

    def __unicode__(self):
        return self.license_code

    class Meta:
        ordering = ['license_code']


class TranslatedData(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    translation = models.CharField(_('Translation'), null=True, blank=True, max_length=512)
    language = models.CharField(_('Language'), choices=sorted(choices.LANGUAGE, key=lambda LANGUAGE: LANGUAGE[1]), null=False, blank=False, max_length=32)
    model = models.CharField(_('Model'), null=False, blank=False, max_length=32)
    field = models.CharField(_('Field'), null=False, blank=False, max_length=32)

    def __unicode__(self):
        return self.translation if self.translation is not None else 'Missing trans: {0}.{1}'.format(self.model, self.field)


class SectionTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    section = models.ForeignKey('Section', related_name='titles')
    title = models.CharField(_('Title'), max_length=256, null=False)
    language = models.ForeignKey('Language')

    class Meta:
        ordering = ['title']


class Section(caching.base.CachingMixin, models.Model):
    """
    Represents a multilingual section of one/many Issues of
    a given Journal.

    ``legacy_code`` contains the section code used by the old
    title manager. We've decided to store this value just by
    historical reasons, and we don't know if it will last forever.
    """
    #Custom manager
    objects = SectionCustomManager()
    nocacheobjects = models.Manager()
    userobjects = modelmanagers.SectionManager()

    journal = models.ForeignKey(Journal)

    code = models.CharField(unique=True, max_length=21, blank=True)
    legacy_code = models.CharField(null=True, blank=True, max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_trashed = models.BooleanField(_('Is trashed?'), default=False, db_index=True)

    def __unicode__(self):
        return ' / '.join([sec_title.title for sec_title in self.titles.all().order_by('language')])

    @property
    def actual_code(self):
        if not self.pk or not self.code:
            raise AttributeError('section must be saved in order to have a code')

        return self.code

    def is_used(self):
        try:
            return True if self.issue_set.all().count() else False
        except ValueError:  # raised when the object is not yet saved
            return False

    def add_title(self, title, language):
        """
        Adds a section title in the given language.

        A Language instance must be passed as the language argument.
        """
        SectionTitle.objects.create(section=self,
            title=title, language=language)

    def _suggest_code(self, rand_generator=base28.genbase):
        """
        Suggests a code for the section instance.
        The code is formed by the journal acronym + 4 pseudo-random
        base 28 chars.

        ``rand_generator`` is the callable responsible for the pseudo-random
        chars sequence. It may accept the number of chars as argument.
        """
        num_chars = getattr(settings, 'SECTION_CODE_TOTAL_RANDOM_CHARS', 4)
        fmt = '{0}-{1}'.format(self.journal.acronym, rand_generator(num_chars))
        return fmt

    def _create_code(self, *args, **kwargs):
        if not self.code:
            tries = kwargs.pop('max_tries', 5)
            while tries > 0:
                self.code = self._suggest_code()
                try:
                    super(Section, self).save(*args, **kwargs)
                except IntegrityError:
                    tries -= 1
                    logger.warning('conflict while trying to generate a section code. %i tries remaining.' % tries)
                    continue
                else:
                    logger.info('code created successfully for %s' % unicode(self))
                    break
            else:
                msg = 'max_tries reached while trying to generate a code for the section %s.' % unicode(self)
                logger.error(msg)
                raise DatabaseError(msg)

    class Meta:
        permissions = (("list_section", "Can list Sections"),)

    def save(self, *args, **kwargs):
        """
        If ``code`` already exists, the section is saved. Else,
        the ``code`` will be generated before the save process is
        performed.
        """
        if self.code:
            super(Section, self).save(*args, **kwargs)
        else:
            # the call to super().save is delegated to _create_code
            # because there are needs to control saving max tries.
            self._create_code(*args, **kwargs)


class Issue(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = IssueCustomManager()
    nocacheobjects = models.Manager()

    section = models.ManyToManyField(Section, blank=True)
    journal = models.ForeignKey(Journal)
    volume = models.CharField(_('Volume'), blank=True, max_length=16)
    number = models.CharField(_('Number'), blank=True, max_length=16)
    suppl_volume = models.CharField(_('Volume Supplement'), null=True, blank=True, max_length=16)
    suppl_number = models.CharField(_('Number Supplement'), null=True, blank=True, max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publication_start_month = models.IntegerField(_('Start Month'), choices=choices.MONTHS)
    publication_end_month = models.IntegerField(_('End Month'), choices=choices.MONTHS)
    publication_year = models.IntegerField(_('Year'))
    is_marked_up = models.BooleanField(_('Is Marked Up?'), default=False, null=False, blank=True)
    use_license = models.ForeignKey(UseLicense, null=True)
    total_documents = models.IntegerField(_('Total of Documents'), default=0)
    ctrl_vocabulary = models.CharField(_('Controlled Vocabulary'), max_length=64,
        choices=sorted(choices.CTRL_VOCABULARY, key=lambda CTRL_VOCABULARY: CTRL_VOCABULARY[1]), null=False, blank=True)
    editorial_standard = models.CharField(_('Editorial Standard'), max_length=64,
        choices=sorted(choices.STANDARD, key=lambda STANDARD: STANDARD[1]))
    cover = models.ImageField(_('Issue Cover'), upload_to='img/issue_cover/', null=True, blank=True)
    is_trashed = models.BooleanField(_('Is trashed?'), default=False, db_index=True)
    label = models.CharField(db_index=True, blank=True, null=True, max_length=64)

    order = models.IntegerField(_('Issue Order'), blank=True)

    @property
    def scielo_pid(self):
        """
        Returns the PID used on SciELO public catalogs, in the form:
        ``journal_issn + year + order``
        """
        jissn = self.journal.scielo_pid
        return ''.join(
            [
                jissn,
                unicode(self.publication_year),
                u'%04d' % self.order,
            ]
        )

    @property
    def identification(self):
        suppl_volume = _('suppl.') + self.suppl_volume if self.suppl_volume else ''
        suppl_number = _('suppl.') + self.suppl_number if self.suppl_number else ''

        values = [self.number, suppl_volume, suppl_number]

        return ' '.join([val for val in values if val]).strip().replace(
                'spe', 'special').replace('ahead', 'ahead of print')

    def __unicode__(self):

        return "{0} ({1})".format(self.volume, self.identification).replace('()', '')

    @property
    def publication_date(self):
        return '{0} / {1} - {2}'.format(self.publication_start_month,
                                        self.publication_end_month,
                                        self.publication_year)

    def _suggest_order(self, force=False):
        """
        Based on ``publication_year``, ``volume`` and a pre defined
        ``order``, this method suggests the subsequent ``order`` value.

        If the Issues already has a ``order``, it suggests it. Else,
        a query is made for the given ``publication_year`` and ``volume``
        and the ``order`` attribute of the last instance is used.

        When force ``True`` this method ignore order attribute from the instance
        and return the suggest order.
        """
        if self.order and force == False:
            return self.order

        filters = {
            'publication_year': self.publication_year,
            'journal': self.journal,
        }

        if self.volume:
            filters['volume'] = self.volume

        try:
            last = Issue.objects.filter(**filters).order_by('order').reverse()[0]
            next_order = last.order + 1
        except IndexError:
            next_order = 1

        return next_order

    def save(self, *args, **kwargs):
        self.label = unicode(self)

        if not self.pk:
            self.order = self._suggest_order()
        else:
            if tools.has_changed(self, 'publication_year') or tools.has_changed(self, 'volume'):
                self.order = self._suggest_order(force=True)

        super(Issue, self).save(*args, **kwargs)

    class Meta:
        permissions = (("list_issue", "Can list Issues"),
                      ("reorder_issue", "Can Reorder Issues"))


class IssueTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    issue = models.ForeignKey(Issue)
    language = models.ForeignKey('Language')
    title = models.CharField(_('Title'), max_length=128)


class PendedForm(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    view_name = models.CharField(max_length=128)
    form_hash = models.CharField(max_length=32)
    user = models.ForeignKey(User, related_name='pending_forms')
    created_at = models.DateTimeField(auto_now=True)


class PendedValue(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    form = models.ForeignKey(PendedForm, related_name='data')
    name = models.CharField(max_length=255)
    value = models.TextField()


class DataChangeEvent(models.Model):
    """
    Tracks data changes to make possible for consumer apps to know
    what to sync.
    """
    changed_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    event_type = models.CharField(max_length=16, choices=EVENT_TYPES)
    collection = models.ForeignKey(Collection)


class PressRelease(caching.base.CachingMixin, models.Model):
    """
    Represents a press-release bound to a Journal.
    If ``issue`` is None, the pressrelease is refers to an ahead article.
    It can be available in one or any languages (restricted by the Journal
    publishing policy).
    """
    nocacheobjects = models.Manager()
    objects = models.Manager()
    doi = models.CharField(_("Press release DOI number"),
                           max_length=128, null=True, blank=True)

    def add_article(self, article):
        """
        ``article`` is a string of the article pid.
        """
        PressReleaseArticle.objects.create(press_release=self,
                                           article_pid=article)

    def remove_article(self, article):
        try:
            pra = PressReleaseArticle.objects.get(press_release=self,
                                                  article_pid=article)
        except PressReleaseArticle.DoesNotExist:
            return None
        else:
            pra.delete()

    def add_translation(self, title, content, language):
        """
        Adds a new press-release translation.

        ``language`` is an instance of Language.
        """
        PressReleaseTranslation.objects.create(press_release=self,
                                               language=language,
                                               title=title,
                                               content=content)

    def remove_translation(self, language):
        """
        Removes the translation for the given press-release.
        If the translation doesn't exist, nothing happens silently.
        """
        qry_params = {'press_release': self}
        if isinstance(language, basestring):
            qry_params['language__iso_code'] = language
        else:
            qry_params['language'] = language

        try:
            pr = PressReleaseTranslation.objects.get(**qry_params)
        except PressReleaseTranslation.DoesNotExist:
            return None
        else:
            pr.delete()

    def get_trans(self, language):
        """
        Syntatic suggar for retrieving translations in a given language
        """
        prt = self.translations.get(language__iso_code=language)
        return prt

    def __unicode__(self):
        """
        Try to get the first title of the Press Release.
        The form ensures at least one title.
        """
        try:
            title = PressReleaseTranslation.objects.filter(press_release=self).order_by('language')[0].title
        except IndexError:
            return __('No Title')

        return title

    class Meta:
        abstract = False
        permissions = (("list_pressrelease", "Can list PressReleases"),)


class PressReleaseTranslation(caching.base.CachingMixin, models.Model):
    """
    Represents a press-release in a given language.
    """
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    press_release = models.ForeignKey(PressRelease, related_name='translations')
    language = models.ForeignKey('Language')
    title = models.CharField(_('Title'), max_length=128)
    content = models.TextField(_('Content'))


class PressReleaseArticle(caching.base.CachingMixin, models.Model):
    """
    Represents press-releases bound to Articles.
    """
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    press_release = models.ForeignKey(PressRelease, related_name='articles')
    article_pid = models.CharField(_('PID'), max_length=32, db_index=True)


class RegularPressRelease(PressRelease):
    objects = RegularPressReleaseCustomManager()
    userobjects = modelmanagers.RegularPressReleaseManager()

    issue = models.ForeignKey(Issue, related_name='press_releases')


class AheadPressRelease(PressRelease):
    objects = AheadPressReleaseCustomManager()
    userobjects = modelmanagers.AheadPressReleaseManager()

    journal = models.ForeignKey(Journal, related_name='press_releases')

####
# Pre and Post save to handle `Journal.pub_status` data modification.
####
@receiver(pre_save, sender=Journal, dispatch_uid='journalmanager.models.journal_pub_status_pre_save')
def journal_pub_status_pre_save(sender, **kwargs):
    """
    Fetch the `pub_status` value from the db before the data is modified.
    """
    try:
        kwargs['instance']._pub_status = Journal.nocacheobjects.get(pk=kwargs['instance'].pk).pub_status
    except Journal.DoesNotExist:
        return None


@receiver(post_save, sender=Journal, dispatch_uid='journalmanager.models.journal_pub_status_post_save')
def journal_pub_status_post_save(sender, instance, created, **kwargs):
    """
    Check if the `pub_status` value is new or has been modified.
    """
    if getattr(instance, '_pub_status', None) and instance.pub_status == instance._pub_status:
        return None

    JournalPublicationEvents.objects.create(journal=instance,
        status=instance.pub_status, changed_by=instance.pub_status_changed_by, reason=instance.pub_status_reason)

models.signals.post_save.connect(create_api_key, sender=User)
