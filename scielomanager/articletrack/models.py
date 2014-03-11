import caching.base
import datetime
import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from articletrack import modelmanagers
from journalmanager.models import Journal

logger = logging.getLogger(__name__)


class Notice(caching.base.CachingMixin, models.Model):

    checkin = models.ForeignKey('Checkin', related_name='notices')

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

    attempt_ref = models.CharField(max_length=32)
    package_name = models.CharField(max_length=128)
    uploaded_at = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)

    article = models.ForeignKey('Article', related_name='checkins', null=True)

    class Meta:
        ordering = ['-created_at']
        permissions = (("list_checkin", "Can list Checkin"),)

    @property
    def get_error_level(self):
        if self.notices.filter(status__iexact="error").count() > 0:
            return "error"
        elif self.notices.filter(status__iexact="warning").count() > 0:
            return "warning"
        else:
            return "ok"


class Article(caching.base.CachingMixin, models.Model):
    # Custom Managers
    objects = models.Manager()
    userobjects = modelmanagers.ArticleManager()

    journals = models.ManyToManyField(Journal, null=True, related_name='checkin_articles')
    article_title = models.CharField(max_length=512)
    articlepkg_ref = models.CharField(max_length=32)
    journal_title = models.CharField(max_length=256)
    issue_label = models.CharField(max_length=64)
    pissn = models.CharField(max_length=9, default='')
    eissn = models.CharField(max_length=9, default='')

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')
        permissions = (("list_article", "Can list Article"),)

    def __unicode__(self):
        return "%s (ref: %s)" % (self.article_title, self.articlepkg_ref)


class Ticket(caching.base.CachingMixin, models.Model):
    # Custom Managers
    objects = models.Manager()
    userobjects = modelmanagers.TicketManager()

    started_at = models.DateTimeField(_("Started at"), auto_now=True)
    finished_at = models.DateTimeField(_("Finished at"), null=True, blank=True)
    author = models.ForeignKey(User, related_name='tickets')
    title = models.CharField(_("Title"), max_length=256)
    message = models.TextField(_("Message"))
    article = models.ForeignKey(Article, related_name='tickets')

    class Meta:
        verbose_name = _(u'Ticket')
        verbose_name_plural = _(u'Tickets')
        permissions = (("list_ticket", "Can list Ticket"),)
        ordering = ['started_at']

    def __unicode__(self):
        return u"%s - %s" % (self.pk, self.title)

    @property
    def is_open(self):
        return self.finished_at is None


class Comment(caching.base.CachingMixin, models.Model):
    """
        Represents a comment related to a Ticket
    """
    # Custom Managers
    objects = models.Manager()
    userobjects = modelmanagers.CommentManager()

    created_at = models.DateTimeField(_(u"Creation date"), auto_now_add=True)
    updated_at = models.DateTimeField(_(u"Updated date"), auto_now=True)
    author = models.ForeignKey(User, related_name='comments_author')
    ticket = models.ForeignKey(Ticket, related_name='comments')
    message = models.TextField(_(u"Message"))

    class Meta:
        verbose_name = _(u'Comment')
        verbose_name_plural = _(u'Comments')
        ordering = ['created_at']
        permissions = (("list_comment", "Can list Comment"),)

    def __unicode__(self):
        return u"%s (ticket: %s)" % (self.pk, self.ticket)
