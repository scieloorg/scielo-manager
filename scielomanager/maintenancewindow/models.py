from datetime import date
from django.db import models
from django.utils.translation import ugettext_lazy as _

import caching.base


class EventManager(models.Manager):

    def scheduled_events(self, actual_date=date.today()):
        """
        Returns a list of scheduled events with the end_date greater than a given date.
        """

        return self.filter(end_at__gte=actual_date, is_finished=False)

    def blocking_users_scheduled_event(self):
        """
        Returns a list of scheduled events blocking users access
        with the end_date greater than a given date.
        """
        try:
            return self.get(is_blocking_users=True)
        except Event.DoesNotExist:
            return None

    def set_blocking_users_events_to_false(self):
        self.filter(is_blocking_users=True).update(is_blocking_users=False)


class Event(caching.base.CachingMixin, models.Model):

    objects = EventManager()
    title = models.CharField(_('Title'), max_length=128, null=False, blank=False)
    begin_at = models.DateTimeField(_('Begin at'), null=False, blank=False)
    end_at = models.DateTimeField(_('End at'), null=False, blank=False, db_index=True)
    description = models.TextField(_('Description'), null=False, blank=False)
    is_blocking_users = models.BooleanField(_('is blocking users'),
                        default=False,
                        db_index=True,
                        help_text=_('once it is checked, it will set up the other events to false')
                        )
    is_finished = models.BooleanField(_('Is finished'), default=False)
    event_report = models.TextField(_('Report'), blank=True)

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
