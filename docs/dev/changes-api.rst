Changes API
===========

The main idea behind the Changes API is to provide ways for a
consumer application to keep track of changes of its interest.
By now, it is possible to keep track of Collections, Journals
and Issues.

By "keep track of" we mean to know if any of the above mentioned
objects have been added, updated or deleted, but without paying
attention on the actual modified data, i.e. it is impossible to
have a diff of 2 versions of a given Journal in a straightforward
way.

First of all, the Changes API aims to solve the following use cases:

1. We are writing an OPAC application for one or many collections,
   containing all its Journals, Issues and Articles.
#. We are writing an OPAC application with a subset of Journals of
   one or many collection.
#. We are writing an OPAC application with a subset of Issues of
   one or many Journal.
#. A mix of the cases above.

The taken approach consists on delegation to the client apps the task
of mining for relevant events. This way the Changes API can be
implemented in a more simple and generic way. Similar to Couchdb
_changes API, we provide a sequential number to be used as a reference
to already mined events.


.. note::

  It is important to notice that by now SciELO Manager is not responsible
  for managing Articles.
  This feature is currently `under development <https://github.com/scieloorg/SciELO-Manager/tree/articles>`_.


:Available data:

seq
  A sequential number that identifies the data change event.

changed_at
  The date and time where the event was registered.

collection_uri
  The collection who the object relates to.

object_uri
  The object that triggered the event.

event_type
  The nature of the event. Can be: ``added``, ``updated`` or ``deleted``.

resource_uri
  A reference to the event in the Changes API.



List all events
---------------

Request::

  GET /api/v1/changes

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **since**

    *Int* of the ``seq`` number used as a starting point to the query.
