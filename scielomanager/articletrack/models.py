# coding: utf-8
import caching.base
import datetime
import logging

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings

from articletrack import modelmanagers
from journalmanager.models import Journal
from scielomanager.utils import misc

logger = logging.getLogger(__name__)

SERVICE_STATUS_MAX_STAGES = 2  # The count of pairs (SERV_BEGIN, SERV_END) in notice.status at the end of processing

MSG_WORKFLOW_ACCEPTED = 'Checkin Accepted'
MSG_WORKFLOW_REJECTED = 'Checkin Rejected'
MSG_WORKFLOW_REVIEWED_QAL1 = 'Checkin Reviewed - Level 1'
MSG_WORKFLOW_REVIEWED_QAL2 = 'Checkin Reviewed - Level 2 (SciELO)'
MSG_WORKFLOW_SENT_TO_PENDING = 'Checkin Sent to Pending'
MSG_WORKFLOW_SENT_TO_REVIEW = 'Checkin Sent to Review'
MSG_WORKFLOW_EXPIRED = 'Checkin Expired'
MSG_WORKFLOW_CHECKED_OUT = 'Checkin Checked Out'


class Team(caching.base.CachingMixin, models.Model):
    """
    Represents a group of users
    """

    name = models.CharField(_(u"Name of team"), max_length=128, unique=True)
    member = models.ManyToManyField(User, related_name="team")

    class Meta:
        verbose_name = _(u'Team')
        verbose_name_plural = _(u'Teams')
        permissions = (("list_team", "Can list Team"),)


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

    def __unicode__(self):
        return u"%s %s (%s) for checkin: %s" % (self.stage, self.checkpoint, self.status, self.checkin)


CHECKIN_STATUS_CHOICES = (
    ('pending', _('Pending')),
    ('review', _('Review')),
    ('accepted', _('Accepted')),
    ('rejected', _('Rejected')),
    ('expired', _('Expired')),
)


def log_workflow_status(message):
    def decorator(f):
        def decorated(*args, **kwargs):
            ret = f(*args, **kwargs)

            log = CheckinWorkflowLog()
            log.checkin = args[0]
            log.status = args[0].status
            log.created_at = datetime.datetime.now()
            log.user = args[1] if len(args) >= 2 else None
            log.description = message + (" - Reason: %s" % args[0].rejected_cause if getattr(args[0], 'rejected_cause') else '')
            log.save()

            return ret
        return decorated
    return decorator


class Checkin(caching.base.CachingMixin, models.Model):

    # Custom Managers
    objects = models.Manager()
    userobjects = modelmanagers.CheckinManager()

    attempt_ref = models.CharField(max_length=32)
    package_name = models.CharField(max_length=128)
    uploaded_at = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    article = models.ForeignKey('Article', related_name='checkins', null=True)
    status = models.CharField(_(u'Status'), choices=CHECKIN_STATUS_CHOICES, max_length=10, default='pending')

    accepted_by = models.ForeignKey(User, null=True, blank=True)
    accepted_at = models.DateTimeField(null=True, blank=True)
    # QAL1
    reviewed_by = models.ForeignKey(User, related_name='checkins_reviewed', null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    # QAL2
    scielo_reviewed_by = models.ForeignKey(User, related_name='checkins_scielo_reviewed', null=True, blank=True)
    scielo_reviewed_at = models.DateTimeField(null=True, blank=True)

    rejected_by = models.ForeignKey(User, related_name='checkins_rejected', null=True, blank=True)
    rejected_at = models.DateTimeField(null=True, blank=True)
    rejected_cause = models.CharField(_(u'Cause of Rejection'), max_length=128, null=True, blank=True)

    submitted_by = models.ForeignKey(User, related_name='checkins_submitted_by', null=True, blank=True)

    expiration_at = models.DateTimeField(_(u'Expiration Date'), null=True, blank=True)

    checked_out = models.BooleanField(_(u'Checked Out'), default=False)

    class Meta:
        ordering = ['-created_at']
        permissions = (("list_checkin", "Can list Checkin"),)

    @property
    def is_serv_status_completed(self):
        """
        If the checkin's notices sequence is UNCOMPLETED (probably more notices will arrive)
            Return False
        Else:
            if the quantity of SERV_* is ok then
                Return the result of validate the order of SERV_.
            else:
                Return False
        """
        count_serv_end_notices = self.notices.filter(status__iexact="SERV_END").count()
        count_serv_begin_notices = self.notices.filter(status__iexact="SERV_BEGIN").count()
        if (count_serv_end_notices < SERVICE_STATUS_MAX_STAGES) or (count_serv_begin_notices < SERVICE_STATUS_MAX_STAGES):
            return False
        else:
            serv_ocurrs = self.notices.filter(status__istartswith="serv_").order_by('created_at')
            if serv_ocurrs.count() == (2 * SERVICE_STATUS_MAX_STAGES):
                sequence = [sym.status for sym in serv_ocurrs]
                return misc.validate_sequence(sequence)
            else:
                return False

    @property
    def get_error_level(self):
        if self.is_serv_status_completed:
            if self.notices.filter(status__iexact="error").count() > 0:
                return "error"
            elif self.notices.filter(status__iexact="warning").count() > 0:
                return "warning"
            else:
                return "ok"
        else:
            return "in progress"

    @property
    def get_newest_checkin(self):
        """
        Get the newest checkin of article
        """
        return self.article.checkins.order_by('-uploaded_at')[0]

    @property
    def is_newest_checkin(self):
        """
        Checks if instance is the newest checkin
        """
        return self.pk == self.get_newest_checkin.pk

    @property
    def is_expirable(self):
        """
        Return True if the expiration_at's date is equal to datetime.date.today()
        Compared with <= to catch possibly unprocessed checkins
        """
        return self.status == 'pending' and self.expiration_at.date() <= datetime.date.today()

    @property
    def is_accepted(self):
        """
        Checks if this checkin has been accepted

        The condicional is ``status = accepted`` and has been accepted_by and
        has any date in accepted_at
        """
        return self.status == 'accepted' and bool(self.accepted_by and self.accepted_at)

    @property
    def is_level1_reviewed(self):
        """
        Checks if this checkin has been reviewed by a QAL1 user

        The condicional is ``status = review`` and has been ``reviewed_by`` and
        has any date in ``reviewed_at``
        """
        return bool(self.reviewed_by and self.reviewed_at)

    @property
    def is_level2_reviewed(self):
        """
        Checks if this checkin has been reviewed by a QAL2 user

        The condicional is ``status = review`` and has been ``scielo_reviewed_by``  and
        has any date in ``reviewed_at``
        """
        return bool(self.scielo_reviewed_by and self.scielo_reviewed_at)

    @property
    def is_full_reviewed(self):
        """
        Checks if this checkin has been reviewed by both user's roles: QAL1 and QAL2
        """
        return self.status == 'review' and self.is_level1_reviewed and self.is_level2_reviewed

    @property
    def is_rejected(self):
        """
        Checks if this checkin has been rejected

        The condicional is ``status = rejected``
        """
        return self.status == 'rejected'

    @property
    def can_be_send_to_pending(self):
        """
        Check the conditions to enable: 'send to pending'  action.
        Return True if this checkin have status ``rejected``
        does not exist another checkin accepted for the related article.
        """
        return self.status == 'rejected'

    @property
    def can_be_send_to_review(self):
        """
        Check the conditions to enable: 'send to review'  action.
        Return True if this checkin have status ``pending`` and have no errors and
        does not exist another checkin accepted for the related article.
        """
        return self.status == 'pending' and self.get_error_level in ['ok', 'warning']

    @property
    def can_be_reviewed(self):
        """
        Check the conditions to enable the process of 'review' action.
        Return True if this checkin is in status ``pending`` and have no errors and
        does not exist another checkin accepted for the related article.
        """
        return self.status == 'review' and self.get_error_level in ['ok', 'warning']

    @property
    def can_be_accepted(self):
        """
        Check the conditions to enable the process of 'accept' action.
        Return True if this checkin has been reviwed by both (scielo and non scielo parts).
        """
        return self.is_full_reviewed

    @property
    def can_be_send_to_checkout(self):
        """
        Only if status == 'accepted' and self.checked_out == False
        """
        return self.status == 'accepted' and not self.checked_out

    @property
    def can_be_rejected(self):
        """
        Return True if Checkin can be rejected.
        Only checkins with status 'review' can be rejected.
        """
        return self.status == 'review'

    # ########### #
    # VALIDATIONS #
    # ########### #

    def _do_basic_validation(self, responsible, action):
        """
        Do some general validations required to modify a checkin.
        Return a tuple:
            - (True, None) if validation is successful
            - (False, "Error message") if not.

        Will not be valid when:
        - exist any accepted article already, or
        - the user `responsible` is not active or
        - the user `responsible` dont belong to the corresponding auth.group (depends on `action`)
        :param responsible: instance of django.contrib.auth.User
        :param action: could be:
            ['accept', 'reject', 'review_l1', 'review_l2', 'send_to_review', 'send_to_pending']
        """
        if not responsible.is_active:
            return (False, 'User must be active')

        profile = responsible.get_profile()

        if action == 'accept' and not profile.can_accept_checkins:
            return (False, 'User can\'t ACCEPT checkins, because doesn\'t have enough permissions')
        elif action == 'reject' and not profile.can_reject_checkins:
            return (False, 'User can\'t REJECT checkins, because doesn\'t have enough permissions')
        elif action == 'review_l1' and not profile.can_review_l1_checkins:
            return (False, 'User can\'t REVIEW (Level 1) checkins, because doesn\'t have enough permissions')
        elif action == 'review_l2' and not profile.can_review_l2_checkins:
            return (False, 'User can\'t REVIEW (Level 2) checkins, because doesn\'t have enough permissions')
        elif action == 'send_to_review' and not profile.can_send_checkins_to_review:
            return (False, 'User can\'t SEND checkins TO REVIEW, because doesn\'t have enough permissions')
        elif action == 'send_to_pending' and not profile.can_send_checkins_to_pending:
            return (False, 'User can\'t SEND checkins TO PENDING, because doesn\'t have enough permissions')

        if self.article.is_accepted():
            return (False, 'Can\'t  accept more than one checkin per article')

        return (True, None)

    def _do_review_validation(self, responsible, action):
        """
        Do some validations required to do a checkin review.
        Return a tuple:
            - (True, None) if validation is successful
            - (False, "Error message") if not: 

        if the user `responsible` is not active or if exist any accepted article already, or
        :param responsible: instance of django.contrib.auth.User
        :param action: could be:
            ['review_l1', 'review_l2']
        """

        if not self.can_be_reviewed:
            return (False, 'This checkin does not comply with the conditions to be reviewed')

        return self._do_basic_validation(responsible, action)

    # ####### #
    # ACTIONS #
    # ####### #

    @log_workflow_status(MSG_WORKFLOW_ACCEPTED)
    def accept(self, responsible):
        """
        Accept the checkin as ready to be part of the collection.
        Change status of this checkin from 'review' to 'accepted'.

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_basic_validation(responsible, 'accept')

        if not is_valid:
            raise ValueError(errors)
        elif self.can_be_accepted:
            self.accepted_by = responsible
            self.accepted_at = datetime.datetime.now()
            self.status = 'accepted'
            self.save()
        else:
            raise ValueError('This checkin do not comply with the conditions to be accepted')

    @log_workflow_status(MSG_WORKFLOW_SENT_TO_PENDING)
    def send_to_pending(self, responsible):
        """
        Send to pending list (change the status to 'pending').

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_basic_validation(responsible, 'send_to_pending')
        if not is_valid:
            raise ValueError(errors)
        elif self.can_be_send_to_pending:
            self.status = 'pending'
            self.save()
        else:
            raise ValueError('This checkin do not comply with the conditions to be moved to pending list')

    @log_workflow_status(MSG_WORKFLOW_SENT_TO_REVIEW)
    def send_to_review(self, responsible):
        """
        Send to review list (change the status to 'review')

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_basic_validation(responsible, 'send_to_review')
        if not is_valid:
            raise ValueError(errors)
        elif self.can_be_send_to_review:
            self.status = 'review'
            self.save()
        else:
            raise ValueError('This checkin does not comply with the conditions to be moved to review list')

    @log_workflow_status(MSG_WORKFLOW_REVIEWED_QAL1)
    def do_review_by_level_1(self, responsible):
        """
        Checkin with status review, are filled with review information (reviewed_by and reviewed_at)

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_review_validation(responsible, 'review_l1')
        if is_valid:
            self.status = 'review'
            self.reviewed_by = responsible
            self.reviewed_at = datetime.datetime.now()
            self.save()
        else:
            raise ValueError(errors)

    @log_workflow_status(MSG_WORKFLOW_REVIEWED_QAL2)
    def do_review_by_level_2(self, responsible):
        """
        Checkin with status review, are filled with review information (scielo_reviewed_by and scielo_reviewed_at)

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_review_validation(responsible, 'review_l2')
        if is_valid:
            self.status = 'review'
            self.scielo_reviewed_by = responsible
            self.scielo_reviewed_at = datetime.datetime.now()
            self.save()
        else:
            raise ValueError(errors)

    @log_workflow_status(MSG_WORKFLOW_REJECTED)
    def do_reject(self, responsible, reason):
        """
        Reject the checkin.  (change the status to 'rejected')
        If can be rejected must be saved the date, the responsible of the action and a reason of rejection.

        Raises ValueError if don't comply with required validations.
        :param responsible: instance of django.contrib.auth.User
        """
        is_valid, errors = self._do_basic_validation(responsible, 'reject')
        if not is_valid:
            raise ValueError(errors)
        elif self.can_be_rejected:
            self.status = 'rejected'
            self.rejected_by = responsible
            self.rejected_at = datetime.datetime.now()
            self.rejected_cause = reason
            self.save()
        else:
            raise ValueError('This checkin does not comply with the conditions to be rejected')

    @log_workflow_status(MSG_WORKFLOW_EXPIRED)
    def do_expires(self, responsible=None):
        """
        Change self.status to 'expired'.
        Change self.expiration_at to now()
        This action generates a ``CheckinWorkflowLog`` entry.
        """
        if self.status != 'expired':
            self.status = 'expired'
            self.expiration_at = datetime.datetime.now()
            self.save()

    @log_workflow_status(MSG_WORKFLOW_CHECKED_OUT)
    def do_mark_as_checked_out(self, responsible=None):
        """
        This method will be call before successfully checked out via BalaioRPC api.
        Will change to True self.checked_out field only with self.status == accepted.
        """
        if self.can_be_send_to_checkout:
            self.checked_out = True
            self.save()

    def clean(self):
        # validation for status "accepted"
        if self.status == 'accepted' and not bool(self.accepted_by and self.accepted_at and self.reviewed_by and self.reviewed_at):
            raise ValidationError('Checkin with "accepted" status must have filled: "accepted_by", \
                "accepted_at", "reviewed_by" and "reviewed_at" fields.')

        # validation for status "rejected"
        if self.status == 'rejected' and not bool(self.rejected_by and self.rejected_at and self.rejected_cause):
            raise ValidationError('Checkin with "rejected" status must have filled: "rejected_by", \
                "rejected_at" and "reviewed_cause" fields.')

    def save(self, *args, **kwargs):
        if self.status == 'pending':
            if self.expiration_at is None:
                # update expiration info
                now = datetime.datetime.now()
                time_span = settings.CHECKIN_EXPIRATION_TIME_SPAN
                delta_next = datetime.timedelta(days=time_span)
                self.expiration_at = now + delta_next
            # clear 'review' fields
            self.reviewed_by = None
            self.reviewed_at = None
            self.scielo_reviewed_by = None
            self.scielo_reviewed_at = None
            # clear 'accepted' fields
            self.accepted_by = None
            self.accepted_at = None
            # clear 'rejected' fields
            self.rejected_by = None
            self.rejected_at = None
            self.rejected_cause = None
        elif self.status == 'review':
            # update expiration info
            self.expiration_at = None
            # clear 'accepted' fields
            self.accepted_by = None
            self.accepted_at = None
            # clear 'rejected' fields
            self.rejected_by = None
            self.rejected_at = None
            self.rejected_cause = None
        elif self.status == 'rejected':
            # update expiration info
            self.expiration_at = None
            # clear 'review' fields
            self.reviewed_by = None
            self.reviewed_at = None
            self.scielo_reviewed_by = None
            self.scielo_reviewed_at = None
            # clear 'accepted' fields
            self.accepted_by = None
            self.accepted_at = None
        else:
            # update expiration info
            self.expiration_at = None
        super(Checkin, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s [attept ref: %s]' % (self.package_name, self.attempt_ref)


class CheckinWorkflowLog(caching.base.CachingMixin, models.Model):
    created_at = models.DateTimeField(_(u'Created at'), default=datetime.datetime.now)
    # nullable in case of (Celery's task) processing
    user = models.ForeignKey(User, related_name='checkin_log_responsible', null=True, blank=True)
    status = models.CharField(_(u'Status'), choices=CHECKIN_STATUS_CHOICES, max_length=10, default='pending')
    description = models.TextField(_(u'Description'), null=True, blank=True)
    checkin = models.ForeignKey(Checkin, related_name='submission_log')

    def __unicode__(self):
        return "%s - %s (%s)" % (self.checkin, self.status, self.user)

    class Meta:
        verbose_name = _(u'Checkin workflow Log')
        verbose_name_plural = _(u'Checkin workflow Logs')
        ordering = ['created_at']


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

    def is_accepted(self):
        """
        Checks if there is any checkin accepted for this article.
        """
        return self.checkins.filter(status='accepted').exists()

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
