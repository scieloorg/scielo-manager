# coding: utf-8
"""
The UserObjectManager interface
===============================

Each model object that aims to be contextualized by the current
app user and the visibility rules defined, must provide a
manager called ``userobjects`` following the context protocol:

Custom instance of ``models.Manager``
-------------------------------------

* ``get_query_set`` returns a custom subclass of models.query.QuerySet;
* ``all`` returns all objects the user can access;
* ``active`` returns a subset of ``all``, only with objects from
  the active collection.

Custom instance of ``models.query.QuerySet``
--------------------------------------------

* ``all`` returns all objects the user can access;
* ``active`` returns all objects from the active collection.
* ``startswith`` (optional) returns all objects with the given
  initial char in a meaningful field. this is used for sorting
  and presentation purposes.
* ``simple_search`` (optional) performs a simple search query on one or more
  meaningful fields. accepts only 1 string as search the search term.
* ``available`` returns all objects not marked as trash.
* ``unavailable`` returns all objects marked as trash.

"""
import caching.base

from scielomanager.utils import usercontext
from scielomanager.utils.modelmanagers import UserObjectQuerySet, UserObjectManager

user_request_context = usercontext.get_finder()


class JournalQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(collections__in=get_all_collections())

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(collections=get_active_collection())

    def startswith(self, char):
        return self.filter(title__istartswith=unicode(char))

    def simple_search(self, term):
        return self.filter(title__icontains=unicode(term))

    def available(self):
        return self.filter(is_trashed=False)

    def unavailable(self):
        return self.filter(is_trashed=True)

    def current(self):
        return self.filter(membership__status='current')

    def suspended(self):
        return self.filter(membership__status='suspended')

    def deceased(self):
        return self.filter(membership__status='deceased')

    def inprogress(self):
        return self.filter(membership__status='inprogress')


class JournalManager(UserObjectManager):
    def get_query_set(self):
        return JournalQuerySet(self.model, using=self._db)


class SectionQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            journal__collection__in=get_all_collections())

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            journal__collection=get_active_collection())

    def available(self):
        return self.filter(is_trashed=False)

    def unavailable(self):
        return self.filter(is_trashed=True)


class SectionManager(UserObjectManager):
    def get_query_set(self):
        return SectionQuerySet(self.model, using=self._db)


class SponsorQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            collections__in=get_all_collections()).distinct()

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            collections=get_active_collection())

    def startswith(self, char):
        return self.filter(name__istartswith=unicode(char))

    def simple_search(self, term):
        return self.filter(name__icontains=unicode(term))

    def available(self):
        return self.filter(is_trashed=False)

    def unavailable(self):
        return self.filter(is_trashed=True)


class SponsorManager(UserObjectManager):
    def get_query_set(self):
        return SponsorQuerySet(self.model, using=self._db)


class RegularPressReleaseQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            issue__journal__collection__in=get_all_collections())

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            issue__journal__collection=get_active_collection())

    def journal(self, journal):
        criteria = {'issue__journal__pk': journal} if isinstance(journal, int) else (
            {'issue__journal': journal})
        return self.filter(**criteria)


class RegularPressReleaseManager(UserObjectManager):
    def get_query_set(self):
        return RegularPressReleaseQuerySet(self.model, using=self._db)


class AheadPressReleaseQuerySet(UserObjectQuerySet):
    def all(self, get_all_collections=user_request_context.get_current_user_collections):
        return self.filter(
            journal__collection__in=get_all_collections())

    def active(self, get_active_collection=user_request_context.get_current_user_active_collection):
        return self.filter(
            journal__collection=get_active_collection())

    def journal(self, journal):
        criteria = {'journal__pk': journal} if isinstance(journal, int) else (
            {'journal': journal})
        return self.filter(**criteria)


class AheadPressReleaseManager(UserObjectManager):
    def get_query_set(self):
        return AheadPressReleaseQuerySet(self.model, using=self._db)

