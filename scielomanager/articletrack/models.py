import caching.base

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from articletrack import modelmanagers
from journalmanager.models import Journal


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

    journals = models.ManyToManyField(Journal, null=True, related_name='checkins')
    articlepkg_ref = models.CharField(max_length=32)
    attempt_ref = models.CharField(max_length=32)
    article_title = models.CharField(max_length=512)
    journal_title = models.CharField(max_length=256)
    issue_label = models.CharField(max_length=64)
    package_name = models.CharField(max_length=128)
    uploaded_at = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    pissn = models.CharField(max_length=9, default='')
    eissn = models.CharField(max_length=9, default='')

    class Meta:
        ordering = ['-created_at']
        permissions = (("list_checkin", "Can list Checkin"),)

####
# Signals
####
@receiver(post_save, sender=Checkin, dispatch_uid='articletrack.models.journal_pub_status_post_save')
def checkin_journals_fetching_post_save(sender, **kwargs):
    """
    Binds journals to checkin
    """
    if kwargs['created']:
        eissn = kwargs['instance'].eissn
        pissn = kwargs['instance'].pissn
        kwargs['instance'].journals = Journal.objects.by_issn(eissn) | Journal.objects.by_issn(pissn)
        kwargs['instance'].save()


