# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from django_countries.fields import CountryField

from journalmanager.models import Issue, Language


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
    institution = models.CharField(_('institution'), max_length=256, default='')
    link_cv = models.URLField(_('Link CV'), null=True, blank=True)
    city = models.CharField(_('City'), max_length=256, null=True, blank=True)
    state = models.CharField(_('State'), max_length=256, null=True, blank=True)
    country = CountryField(_('Country'), blank_label="----------")
    research_id = models.CharField(_('ResearcherID'), max_length=256, null=True, blank=True)
    orcid = models.CharField(_('ORCID'), max_length=256, null=True, blank=True)

    order = models.IntegerField(_('board order'), default=1)

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    class Meta:
        ordering = ('board', 'order', 'first_name')


class RoleType(models.Model):
    """
    Represents the board member's roles
    """
    name = models.CharField(_('Role Name'), max_length=256, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class RoleTypeTranslation(models.Model):
    """
    Represents the role's translations
    """
    role = models.ForeignKey(RoleType, related_name='translations')
    name = models.CharField(_('Role Name'), max_length=256, default='')
    language = models.ForeignKey(Language)

    def __unicode__(self):
        return u"%s [%s]" % (self.name, self.language.iso_code)

    class Meta:
        unique_together = ("role", "language")
