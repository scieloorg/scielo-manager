# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.translation import ugettext_lazy as _

import choices

class Title (models.Model):
    creator = models.ForeignKey(User, related_name='enjoy_creator', editable=False)
    created = models.DateTimeField(_('Date of Registration'),default=datetime.now,
        editable=False)
    updated = models.DateTimeField(_('Update Date'),default=datetime.now,
        editable=False)
    title = models.CharField(_('Title'),max_length=256)
    abbreviated_title = models.CharField(_('Abbreviated Title'),max_length=128)
    acronym = models.CharField(_('Acronym'),max_length=8)
    about_en = models.TextField(_('About (English)'),)
    about_pt = models.TextField(_('About (Portuguese)'),)
    about_es = models.TextField(_('About (Spanish)'),)
    print_issn = models.CharField(_('Print ISSN'),max_length=16)
    eletronic_issn = models.CharField(_('Eletronic ISSN'),max_length=16)
    publisher = models.CharField(_('Publisher'),max_length=256)
    begin_year = models.DateField(_('begin at'),max_length=4)
    end_year = models.DateField(_('end at'),max_length=4)
    subjects = models.DateField(_('Subjects'),max_length=256,
        choices=choices.SUBJECTS,)
    