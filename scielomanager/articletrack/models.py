from django.db import models
from articletrack import choices


class Attempt(models.Model):
    checkin_id = models.CharField(max_length=32)
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

    @property
    def last_status(self):
        query = self.status_set.all().order_by('-created_at')[0]

        return query

    def all_status(self):
        query = self.status_set.all().order_by('-created_at')

        return query


class Status(models.Model):
    attempt = models.ForeignKey(Attempt)
    accomplished = models.CharField(choices=sorted(choices.ACCOMPLISHED_TASKS, key=lambda ACCOMPLISHED_TASKS: ACCOMPLISHED_TASKS[1]), max_length=32, default='upload')
    created_at = models.DateTimeField(auto_now_add=True)
