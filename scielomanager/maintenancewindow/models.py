from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

import caching.base


class Event(caching.base.CachingMixin, models.Model):
    title = models.CharField(_('Title'), max_length=128, null=False, blank=False)
    begin_at = models.DateTimeField(_('Begin at'), null=False, blank=False)
    end_at = models.DateTimeField(_('End at'), null=False, blank=False)
    description = models.TextField(_('Description'), null=False, blank=False)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['begin_at', 'title']

    @classmethod
    def on_maintenance(cls, date=datetime.now()):
        """
        Indicates if the system is on maintenance according to a given datetime object.
        """

        system_notes = cls.objects.filter(begin_at__lte=date, end_at__gte=date)

        return True if system_notes.count() else False
