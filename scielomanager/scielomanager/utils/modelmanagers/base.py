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


class UserObjectQuerySet(caching.base.CachingQuerySet):
    """
    Provides a basic implementation of userobject querysets with
    caching features.
    """
    def available(self):
        return self

    def unavailable(self):
        return self.none()


class UserObjectManager(caching.base.CachingManager):
    """
    Provides a basic implementation of userobject managers with
    caching features.
    """
    def all(self, **kwargs):
        return self.get_query_set().all(**kwargs)

    def active(self, **kwargs):
        return self.get_query_set().active(**kwargs)
