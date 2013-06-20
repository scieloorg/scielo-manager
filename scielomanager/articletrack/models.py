from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from articletrack import choices


class Status(models.Model):
    attempt = models.ForeignKey('Attempt')
    phase = models.CharField(choices=sorted(choices.ACCOMPLISHED_TASKS, key=lambda ACCOMPLISHED_TASKS: ACCOMPLISHED_TASKS[1]), max_length=32, default='upload')
    is_accomplished = models.BooleanField(default=False, db_index=True)
    changed_at = models.DateTimeField(auto_now_add=True)


class Attempt(models.Model):
    checkin_id = models.CharField(max_length=32, unique=True)
    articlepkg_id = models.CharField(max_length=32)
    collection_uri = models.URLField()
    article_title = models.CharField(max_length=512)
    journal_title = models.CharField(max_length=256)
    issue_label = models.CharField(max_length=64)
    pkgmeta_filename = models.CharField(max_length=128)
    pkgmeta_md5 = models.CharField(max_length=128)
    pkgmeta_filesize = models.IntegerField()
    pkgmeta_filecount = models.IntegerField()
    pkgmeta_submitter = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True)

    @property
    def last_status(self):
        query = self.status_set.all().order_by('-pk')[0]

        return query

    def all_status(self):
        query = self.status_set.all().order_by('pk')

        return query


@receiver(post_save, sender=Attempt, dispatch_uid='journalmanager.models.attempt_status_post_save')
def attempt_status_post_save(sender, instance, created, **kwargs):
    """
    Register status to an attempt as false
    """
    if not Status.objects.filter(attempt=instance):
        for phase in choices.ACCOMPLISHED_TASKS:
            Status.objects.create(attempt=instance, phase=phase[0])
