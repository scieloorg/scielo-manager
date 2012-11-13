from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _

import caching.base


class Event(caching.base.CachingMixin, models.Model):
    title = models.CharField(_('Title'), max_length=128, null=False, blank=False)
    begin_at = models.DateTimeField(_('Begin at'), null=False, blank=False)
    end_at = models.DateTimeField(_('End at'), null=False, blank=False)
    description = models.TextField(_('Description'), null=False, blank=False)
    is_blocking_users = models.BooleanField(_('is blocking users'), default=False)
    is_finished = models.BooleanField(_('Is finished'), default=False)
    event_report = models.TextField(_('Report'))

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['begin_at', 'title']

    @classmethod
    def on_maintenance(cls):
        """
        Indicates if the system is on maintenance according to a given datetime object.
        """

        return True if cls.objects.filter(is_blocking_users=True).count() else False

    @classmethod
    def scheduled_events(cls, actual_date=date.today()):
        """
        Returns a list of scheduled events with the end_date greater than a given date.
        """

        return cls.objects.filter(end_at__gte=actual_date)
