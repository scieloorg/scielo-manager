# -*- encoding: utf-8 -*-
from datetime import datetime
import urllib
import hashlib

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext as __
from django.contrib.contenttypes import generic
from django.conf.global_settings import LANGUAGES
from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

import caching.base

import choices
import helptexts


class AppCustomManager(caching.base.CachingManager):
    """
    Domain specific model managers.
    """

    def available(self, availability=None):
        """
        Filter the queryset based on its availability.
        """
        data_queryset = self.get_query_set()
        if availability is not None:
            if not isinstance(availability, bool):
                data_queryset = data_queryset.filter(is_available=availability)

        return data_queryset

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
    email = models.EmailField(_('Email'), blank=False, unique=True, null=False)

    @property
    def gravatar_id(self):
        return hashlib.md5(self.email.lower().strip()).hexdigest()

    @property
    def avatar_url(self):
        params = urllib.urlencode({'s': 25, 'd': 'mm'})
        return '{0}/avatar/{1}?{2}'.format(getattr(settings, 'GRAVATAR_BASE_URL',
            'https://secure.gravatar.com'), self.gravatar_id, params)

    def save(self, force_insert=False, force_update=False):
        self.user.email = self.email
        self.user.save()
        return super(UserProfile,self).save(force_insert,force_update)

class Collection(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    collection = models.ManyToManyField(User, related_name='user_collection',
        through='UserCollections', )
    name = models.CharField(_('Collection Name'), max_length=128, db_index=True,)
    url = models.URLField(_('Instance URL'), )
    validated = models.BooleanField(_('Validated'), default=False, )

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        ordering = ['name']

class UserCollections(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection, help_text=helptexts.USERCOLLECTIONS_COLLECTION)
    is_default = models.BooleanField(_('Is default'), default=False, null=False, blank=False)
    is_manager = models.BooleanField(_('Is manager of the collection?'), default=False, null=False,
        blank=False)

class Institution(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = AppCustomManager()
    nocacheobjects = models.Manager()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(_('Institution Name'), max_length=256, db_index=True, help_text=helptexts.INSTITUTION__NAME)
    acronym = models.CharField(_('Sigla'), max_length=16, db_index=True, blank=True, help_text=helptexts.INSTITUTION__ACRONYM)
    country = models.CharField(_('Country'), max_length=32, help_text=helptexts.INSTITUTION__COUNTRY)
    state = models.CharField(_('State'), max_length=32, null=False, blank=True, help_text=helptexts.INSTITUTION__STATE)
    city = models.CharField(_('City'), max_length=32, null=False, blank=True, help_text=helptexts.INSTITUTION__CITY)
    address = models.TextField(_('Address'), help_text=helptexts.INSTITUTION__ADDRESS)
    address_number = models.CharField(_('Number'), max_length=8, help_text=helptexts.INSTITUTION__ADDRESS_NUMBER)
    address_complement = models.CharField(_('Complement'), max_length=128, null=False, blank=True, help_text=helptexts.INSTITUTION__ADDRESS_COMPLEMENT)
    zip_code = models.CharField(_('Zip Code'), max_length=16, null=True, blank=True, help_text=helptexts.INSTITUTION__ZIP_CODE)
    phone = models.CharField(_('Phone Number'), max_length=16, null=False, blank=True, help_text=helptexts.INSTITUTION__PHONE)
    fax = models.CharField(_('Fax Number'), max_length=16, null=False, blank=True, help_text=helptexts.INSTITUTION__FAX)
    cel = models.CharField(_('Cel Number'), max_length=16, null=False, blank=True, help_text=helptexts.INSTITUTION__CEL)
    mail = models.EmailField(_('Email'), help_text=helptexts.INSTITUTION__MAIL)
    validated = models.BooleanField(_('Validated'), default=False, help_text=helptexts.INSTITUTION__VALIDATED)
    is_available = models.BooleanField(_('Is Available?'), default=True, null=False, blank=True, help_text=helptexts.INSTITUTION__IS_AVAILABLE)

    def __unicode__(self):
        return u'%s' % (self.name)

    class Meta:
        ordering = ['name']

class Publisher(Institution):
    objects = AppCustomManager()
    nocacheobjects = models.Manager()
    collections = models.ManyToManyField(Collection)

class Sponsor(Institution):
    objects = AppCustomManager()
    nocacheobjects = models.Manager()
    collections = models.ManyToManyField(Collection)

class Journal(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    #Relation fields
    creator = models.ForeignKey(User, related_name='enjoy_creator', editable=False)
    publisher = models.ManyToManyField('Publisher', related_name='journal_institution',null=False, help_text=helptexts.JOURNAL__PUBLISHER)
    previous_title = models.ForeignKey('Journal',related_name='prev_title', null=True, blank=True, help_text=helptexts.JOURNAL__PREVIOUS_TITLE)
    use_license = models.ForeignKey('UseLicense', help_text=helptexts.JOURNAL__USE_LICENSE)
    collections = models.ManyToManyField('Collection', help_text=helptexts.JOURNAL__COLLECTIONS)
    languages = models.ManyToManyField('Language')

    #Fields
    title = models.CharField(_('Journal Title'), max_length=256, db_index=True, help_text=helptexts.JOURNAL__TITLE)
    title_iso = models.CharField(_('Title ISO'), max_length=256, db_index=True)
    short_title = models.CharField(_('Short Title'), max_length=256, db_index=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    acronym = models.CharField(_('Acronym'), max_length=8, blank=False, help_text=helptexts.JOURNAL__ACRONYM)
    scielo_issn = models.CharField(_('The ISSN used to build the Journal PID.'), max_length=16,
        choices=choices.SCIELO_ISSN, help_text=helptexts.JOURNAL__SCIELO_ISSN)
    print_issn = models.CharField(_('Print ISSN'), max_length=9, help_text=helptexts.JOURNAL__PRINT_ISSN)
    eletronic_issn = models.CharField(_('Eletronic ISSN'), max_length=9, help_text=helptexts.JOURNAL__ELETRONIC_ISSN)
    subject_descriptors = models.CharField(_('Subject / Descriptors'), max_length=512,
        help_text=helptexts.JOURNAL__SUBJECT_DESCRIPTORS)
    init_year = models.CharField(_('Initial Date'), max_length=10, help_text=helptexts.JOURNAL__INIT_YEAR)
    init_vol = models.CharField(_('Initial Volume'), max_length=4, help_text=helptexts.JOURNAL__INIT_VOL)
    init_num = models.CharField(_('Initial Number'), max_length=4, help_text=helptexts.JOURNAL__INIT_NUM)
    final_year = models.CharField(_('Final Date'), max_length=10, null=True, blank=True, help_text=helptexts.JOURNAL__FINAL_YEAR)
    final_vol = models.CharField(_('Final Volume'),max_length=4,null=False,blank=True, help_text=helptexts.JOURNAL__FINAL_VOL)
    final_num = models.CharField(_('Final Number'),max_length=4,null=False,blank=True, help_text=helptexts.JOURNAL__FINAL_NUM)
    frequency = models.CharField(_('Frequency'),max_length=16,
        choices=choices.FREQUENCY, help_text=helptexts.JOURNAL__FREQUENCY)
    pub_status = models.CharField(_('Publication Status'), max_length=16,
        choices=choices.PUBLICATION_STATUS, help_text=helptexts.JOURNAL__PUB_STATUS)
    sponsor = models.CharField(_('Sponsor'), max_length=256, help_text=helptexts.JOURNAL__SPONSOR)
    editorial_standard = models.CharField(_('Editorial Standard'), max_length=64,
        choices=choices.STANDARD, help_text=helptexts.JOURNAL__EDITORIAL_STANDARD)
    ctrl_vocabulary = models.CharField(_('Controlled Vocabulary'), max_length=64,
        choices=choices.CTRL_VOCABULARY, help_text=helptexts.JOURNAL__CTRL_VOCABULARY)
    pub_level = models.CharField(_('Publication Level'),max_length=64,
        choices=choices.PUBLICATION_LEVEL, help_text=helptexts.JOURNAL__PUB_LEVEL)
    secs_code = models.CharField(_('SECS Code'), max_length=64,null=False,blank=True)
    copyrighter = models.CharField(_('Copyrighter'), max_length=254, help_text=helptexts.JOURNAL__COPYRIGHTER)
    url_online_submission = models.CharField(_('URL of online submission'), max_length=64,null=True,blank=True, help_text=helptexts.JOURNAL__SUBJECT_DESCRIPTORS)
    url_journal = models.CharField(_('URL of the journal'), max_length=64,null=True, blank=True, help_text=helptexts.JOURNAL__URL_JOURNAL)
    notes = models.TextField(_('Notes'), max_length=254, null=True, blank=True, help_text=helptexts.JOURNAL__NOTES)
    index_coverage = models.TextField(_('Index Coverage'), null=True, blank=True, help_text=helptexts.JOURNALINDEXCOVERAGE__DATABASE)
    validated = models.BooleanField(_('Validated'), default=False, null=False, blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['title']

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

    journal = models.ForeignKey(Journal)
    status = models.CharField(max_length=16)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.status

    class Meta:
        verbose_name = 'journal publication event'
        verbose_name_plural = 'Journal Publication Events'

class JournalStudyArea(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    journal = models.ForeignKey(Journal)
    study_area = models.CharField(_('Study Area'), max_length=256,
        choices=choices.SUBJECTS, help_text=helptexts.JOURNALSTUDYAREA__STUDYAREA)

class JournalTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    journal = models.ForeignKey(Journal)
    title = models.CharField(_('Title'), null=False, max_length=128, help_text=helptexts.JOURNALTITLE__TITLE)
    category = models.CharField(_('Title Category'), null=False, max_length=128, choices=choices.TITLE_CATEGORY)

class JournalMission(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    journal = models.ForeignKey(Journal, null=False)
    description = models.TextField(_('Mission'), help_text=helptexts.JOURNALMISSION_DESCRIPTION)
    language = models.ForeignKey('Language', blank=False, null=True)

class UseLicense(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    license_code = models.CharField(_('License Code'), unique=True, null=False, blank=False, max_length=64)
    reference_url = models.URLField(_('License Reference URL'), null=True, blank=True)
    disclaimer = models.TextField(_('Disclaimer'), null=True, blank=True, max_length=512)

    def __unicode__(self):
        return self.license_code

class TranslatedData(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    translation = models.CharField(_('Translation'), null=True, blank=True, max_length=512)
    language = models.CharField(_('Language'), choices=choices.LANGUAGE, null=False, blank=False, max_length=32)
    model = models.CharField(_('Model'), null=False, blank=False, max_length=32)
    field = models.CharField(_('Field'), null=False, blank=False, max_length=32)

    def __unicode__(self):
        return self.translation if self.translation is not None else 'Missing trans: {0}.{1}'.format(self.model, self.field)

class SectionTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()

    section = models.ForeignKey('Section')
    title = models.CharField(_('Title'), max_length=256, null=False)
    language = models.ForeignKey('Language')

class Section(caching.base.CachingMixin, models.Model):
    #Custom manager
    objects = AppCustomManager()
    nocacheobjects = models.Manager()

    journal = models.ForeignKey(Journal)

    code = models.CharField(_('Code'), null=True, blank=True, max_length=16)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_available = models.BooleanField(_('Is Available?'), default=True, blank=True)

    def __unicode__(self):
        try:
            return self.sectiontitle_set.all()[0].title
        except IndexError:
            return '##TITLE MISSING##' if not self.code else self.code

class Issue(caching.base.CachingMixin, models.Model):

    #Custom manager
    objects = AppCustomManager()
    nocacheobjects = models.Manager()

    section = models.ManyToManyField(Section, help_text=helptexts.ISSUE__SECTION)
    journal = models.ForeignKey(Journal, null=True, blank=False)
    volume = models.CharField(_('Volume'), null=True, blank=True, max_length=16, help_text=helptexts.ISSUE__VOLUME)
    number = models.CharField(_('Number'), null=True, blank=True, max_length=16, help_text=helptexts.ISSUE__NUMBER)
    is_press_release = models.BooleanField(_('Is Press Release?'), default=False, null=False, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    publication_date = models.DateField(null=False, blank=False, help_text=helptexts.ISSUE__PUBLICATION_DATE)
    is_available = models.BooleanField(_('Is Available?'), default=True, null=False, blank=True) #status v42
    is_marked_up = models.BooleanField(_('Is Marked Up?'), default=False, null=False, blank=True) #v200
    use_license = models.ForeignKey(UseLicense, null=True, help_text=helptexts.ISSUE__USE_LICENSE)
    publisher_fullname = models.CharField(_('Publisher Full Name'), null=True, blank=True, max_length=128, help_text=helptexts.ISSUE__PUBLISHER_FULLNAME)
    total_documents = models.IntegerField(_('Total of Documents'), null=False, blank=False, default=0, help_text=helptexts.ISSUE__TOTAL_DOCUMENTS)
    ctrl_vocabulary = models.CharField(_('Controlled Vocabulary'), max_length=64,
        choices=choices.CTRL_VOCABULARY, null=False, blank=True, help_text=helptexts.ISSUE__CTRL_VOCABULARY)
    editorial_standard = models.CharField(_('Editorial Standard'), max_length=64,
        choices=choices.STANDARD, null=False, blank=True, help_text=helptexts.ISSUE__EDITORIAL_STANDARD)

    def identification(self):

        if self.number is not None:
            n = self.number
            if n != 'ahead' and n != 'review':
                n ='(' + self.number + ')'
            else:
                n = self.number

            return self.volume + ' ' + n
        else:
            return ''

    def __unicode__(self):
        return self.identification()

class IssueTitle(caching.base.CachingMixin, models.Model):
    objects = caching.base.CachingManager()
    nocacheobjects = models.Manager()
    issue = models.ForeignKey(Issue)
    language = models.ForeignKey('Language', blank=False, null=True)
    title = models.CharField(_('Title'), null=False, max_length=128)

class Supplement(Issue):
    suppl_label = models.CharField(_('Supplement Label'), null=True, blank=True, max_length=256)

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
        status=instance.pub_status)
