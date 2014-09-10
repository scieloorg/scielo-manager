from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from django.contrib.admin.util import quote
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from django.utils.safestring import mark_safe

import jsonfield

ADDITION = 1
CHANGE = 2
DELETION = 3


class AuditLogEntryManager(models.Manager):
    def log_action(self, user_id, content_type_id, object_id, object_repr, action_flag, change_message='', old_values='', new_values=''):
        e = self.model(
                None, None, user_id, content_type_id, smart_unicode(object_id),
                object_repr[:200], action_flag, change_message, old_values, new_values)
        e.save()


class AuditLogEntry(models.Model):
    action_time = models.DateTimeField(_('action time'), auto_now=True)
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.PositiveSmallIntegerField(_('action flag'))
    change_message = models.TextField(_('Description'), blank=True)
    old_values = jsonfield.JSONField(_('old values'), blank=True, default={})
    new_values = jsonfield.JSONField(_('new values'), blank=True, default={})

    objects = AuditLogEntryManager()

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-action_time',)

    def __unicode__(self):
        return smart_unicode(self.action_time)

    @property
    def is_addition(self):
        return self.action_flag == ADDITION

    @property
    def is_change(self):
        return self.action_flag == CHANGE

    @property
    def is_deletion(self):
        return self.action_flag == DELETION

    def get_audited_object(self):
        "Returns the audited object pointed by this log entry"
        try:
            return self.content_type.get_object_for_this_type(pk=self.object_id)
        except self.content_type.model_class().DoesNotExist:
            return None

    def get_admin_url(self):
        """
        Returns the admin URL to edit the object represented by this log entry.
        This is relative to the Django admin index page.
        """
        if self.content_type and self.object_id:
            return mark_safe(u"%s/%s/%s/" % (self.content_type.app_label, self.content_type.model, quote(self.object_id)))
        return None


class AuditLogEntryPermission(models.Model):
    """
    If user is asociated with a model (content type),
    then this user can red audit log entries for the module.
    """
    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)

    class Meta:
        verbose_name = _('log entry permission')
        verbose_name_plural = _('log entry permissions')

    def __unicode__(self):
        return smart_unicode('%s can read %s audit log entries' % (self.user, self.content_type))
