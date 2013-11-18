import caching.base

from django.db import models

from articletrack import modelmanagers
from journalmanager.models import Collection


class Notice(caching.base.CachingMixin, models.Model):

    checkin = models.ForeignKey('Checkin')

    stage = models.CharField(max_length=64)
    checkpoint = models.CharField(max_length=64)
    message = models.CharField(max_length=512, null=False)
    status = models.CharField(max_length=64)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        permissions = (("list_notice", "Can list Notices"),)


class Checkin(caching.base.CachingMixin, models.Model):

    #Custom Managers
    objects = models.Manager()
    userobjects = modelmanagers.CheckinManager()

    collection = models.ForeignKey(Collection, null=True)
    articlepkg_ref = models.CharField(max_length=32)
    attempt_ref = models.CharField(max_length=32)
    article_title = models.CharField(max_length=512)
    journal_title = models.CharField(max_length=256)
    issue_label = models.CharField(max_length=64)
    package_name = models.CharField(max_length=128)
    uploaded_at = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        permissions = (("list_checkin", "Can list Checkin"),)
