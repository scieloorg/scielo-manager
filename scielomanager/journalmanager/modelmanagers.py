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

* ``by_user`` returns all objects the user can access;
* ``active`` returns all objects from the active collection.
* ``startswith`` (optional) returns all objects with the given
  initial char in a meaningful field. this is used for sorting
  and presentation purposes.
* ``simple_search`` (optional) performs a simple search query on one or more
  meaningful fields. accepts only 1 string as search the search term.
* ``available`` returns all objects not marked as trash.
* ``unavailable`` returns all objects marked as trash.

"""
from django.db import models

from scielomanager.utils.middlewares import threadlocal


def get_current_user_collections():
    user = threadlocal.get_current_user()
    if user:
        return user.user_collection.all()


def get_current_user_active_collection():
    colls = get_current_user_collections()
    if colls:
        return colls.get(usercollections__is_default=True)


class UserObjectQuerySet(models.query.QuerySet):
    """
    Provides a basic implementation of userobject querysets.
    """
    def available(self):
        return self

    def unavailable(self):
        return self.none()


class UserObjectManager(models.Manager):
    """
    Provides a basic implementation of userobject managers.
    """
    def all(self):
        return self.get_query_set().by_user()

    def active(self):
        return self.get_query_set().active()


class JournalQuerySet(UserObjectQuerySet):
    def by_user(self):
        return self.filter(collection__in=get_current_user_collections())

    def active(self):
        return self.filter(collection=get_current_user_active_collection())

    def startswith(self, char):
        return self.filter(title__istartswith=unicode(char))

    def simple_search(self, term):
        return self.filter(title__icontains=term)

    def available(self):
        return self.filter(is_trashed=False)

    def unavailable(self):
        return self.filter(is_trashed=True)

    def current(self):
        return self.filter(pub_status='current')

    def suspended(self):
        return self.filter(pub_status='suspended')

    def deceased(self):
        return self.filter(pub_status='deceased')

    def inprogress(self):
        return self.filter(pub_status='inprogress')


class JournalManager(UserObjectManager):
    def get_query_set(self):
        return JournalQuerySet(self.model, using=self._db)


class SectionQuerySet(UserObjectQuerySet):
    def by_user(self):
        return self.filter(
            journal__collection__in=get_current_user_collections())

    def active(self):
        return self.filter(
            journal__collection=get_current_user_active_collection())

    def available(self):
        return self.filter(is_trashed=False)

    def unavailable(self):
        return self.filter(is_trashed=True)


class SectionManager(UserObjectManager):
    def get_query_set(self):
        return SectionQuerySet(self.model, using=self._db)
