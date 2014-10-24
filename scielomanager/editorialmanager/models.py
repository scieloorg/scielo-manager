#coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from journalmanager.models import Issue


class EditorialBoard(models.Model):
    """
    Represents the editorial board for one issue.
    """
    issue = models.OneToOneField(Issue, null=False)

    def __unicode__(self):
        return "Editorial board of issue: %s" % self.issue


class EditorialMember(models.Model):
    """
    Represents members of an editorial board

    Required Fields: First Name, Last Name, E-mail.
    """
    role = models.ForeignKey('RoleType')
    board = models.ForeignKey(EditorialBoard)

    first_name = models.CharField(_('First Name'), max_length=256)
    last_name = models.CharField(_('Last Name'), max_length=256)

    email = models.EmailField(_('E-mail'), null=True, blank=True)
    institution = models.CharField(_('institution'), max_length=256, null=True, blank=True)
    link_cv = models.URLField(_('Link CV'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=256, null=True, blank=True)
    state = models.CharField(_('State'), max_length=256, null=True, blank=True)
    country = models.CharField(_('Country'), max_length=256, null=True, blank=True)
    research_id = models.CharField(_('ResearchID'), max_length=256, null=True, blank=True)
    orcid = models.CharField(_('ORCID'), max_length=256, null=True, blank=True)

    order = models.IntegerField(_('board order'), default=1)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    class Meta:
        ordering = ('board', 'order', 'pk')


class RoleType(models.Model):
    """
    Represents the editor category
    """
    name = models.CharField(_('Role Name'), max_length=256)
    weight = models.PositiveSmallIntegerField(_('role weight'), default=10)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('weight', 'name')

