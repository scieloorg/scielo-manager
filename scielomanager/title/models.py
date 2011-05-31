# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

import choices

class Publisher (models.Model):
    class Meta:
        ordering = ['name','sponsor']    
    name = models.CharField(_('Publisher Name'), max_length=128, db_index=True,)
    country = models.CharField(_('Country'), max_length=32)
    state = models.CharField(_('State'), max_length=32, null=False,blank=True,)
    city = models.CharField(_('City'), max_length=32, null=False,blank=True,)
    Address = models.TextField(_('Address'), )
    Address_number = models.CharField(_('Number'), max_length=8)
    Address_complement = models.CharField(_('Complement'), max_length=64, null=False,blank=True,)
    zip = models.CharField(_('Zip Code'), max_length=16)
    phone = models.CharField(_('Phone Number'), max_length=16, null=False,blank=True,)
    fax =  models.CharField(_('Fax Number'), max_length=16, null=False,blank=True,)
    cel = models.CharField(_('Cel Number'), max_length=16, null=False,blank=True,)
    mail = models.EmailField(_('Email'),)
    sponsor = models.CharField(_('Sponsor'), max_length=128, null=False,blank=True,)
    validated = models.BooleanField(_('Validated'), default=False, )
    
    def __unicode__(self):
        return u'%s' % (self.name)
        
class Title (models.Model):
    def __unicode__(self):
        return u'%s' % (self.title)
    class Meta:
        ordering = ['title']         
    # PART 1
    creator = models.ForeignKey(User, related_name='enjoy_creator', editable=False)
    created = models.DateTimeField(_('Date of Registration'),default=datetime.now,
        editable=False)
    updated = models.DateTimeField(_('Update Date'),default=datetime.now,
        editable=False)
    publisher = models.ForeignKey(Publisher, related_name='title_publisher')    
    title = models.CharField(_('Publication Title'),max_length=256, db_index=True,)
    abbreviated_title = models.CharField(_('Short Title'),max_length=128)
    iso_title = models.CharField(_('ISO Short Title'),max_length=128)
    acronym = models.CharField(_('Acronym'),max_length=8)
    mission_en = models.TextField(_('Mission (English)'),)
    mission_pt = models.TextField(_('Mission (Portuguese)'),)
    mission_es = models.TextField(_('Mission (Spanish)'),)
    print_issn = models.CharField(_('Print ISSN'),max_length=16)
    eletronic_issn = models.CharField(_('Eletronic ISSN'),max_length=16)
    subject_descriptors = models.CharField(_('Subject / Descriptors'),max_length=64)
    study_area = models.CharField(_('Study Area'),max_length=256,
        choices=choices.SUBJECTS,)
    indexation_range = models.CharField(_('Indexation Range'),max_length=64)
    
    #PART 2
    init_year = models.DateField(_('Initial Date'),max_length=4)
    init_vol = models.CharField(_('Initial Volume'), max_length=4)
    init_num = models.CharField(_('Initial Number'), max_length=4)    
    final_year = models.DateField(_('Final Date'),max_length=4)
    final_vol = models.CharField(_('Final Volume'),max_length=4)
    final_num = models.CharField(_('Final Numbert'),max_length=4)
    frequency = models.CharField(_('Frequency'),max_length=16,
        choices=choices.FREQUENCY,)
    pub_status = models.CharField(_('Publication Status'),max_length=16,
        choices=choices.PUBLICATION_STATUS,)
    alphabet =  models.CharField(_('Alphabet'),max_length=16,
        choices=choices.ALPHABET,)
    classification = models.CharField(_('Initial Number'), max_length=16)
    national_code = models.CharField(_('National Code'), max_length=16)    
    text_language = models.CharField(_('Text Language'), max_length=16)
    abst_language = models.CharField(_('Abstract Number'), max_length=16)
    standard = models.CharField(_('Alphabet'),max_length=64,
        choices=choices.STANDARD,)
    ctrl_vocabulary = models.CharField(_('Controlled Vocabulary'),max_length=64,
        choices=choices.CTRL_VOCABULARY,)
    literature_type = models.CharField(_('Literature Type'),max_length=64,
        choices=choices.LITERATURE_TYPE,)
    treatment_level = models.CharField(_('Treatment Type'),max_length=64,
        choices=choices.TREATMENT_LEVEL,)
    pub_level = models.CharField(_('Publication Level'),max_length=64,
        choices=choices.PUBLICATION_LEVEL,)
    secs_code = models.CharField(_('SECS Code'), max_length=64)
    medline_code = models.CharField(_('Medline Code'), max_length=64)
    medline_short_title = models.CharField(_('Medline Short Title'), max_length=128)
    validated = models.BooleanField(_('Validated'), default=False, )
