==================
SciELO Manager API
==================

All the catalographic data, managed by SciELO Manager, are made
available by a RESTful API. By now, the API provides read-only
access, but for future releases more methods will be added.

If you have any problems or requests please contact
`support <http://groups.google.com/group/scielo-discuss/>`_.

**Current version:** API v1


.. note::

  Although all data are available to be consumed by the API, the requesting
  user needs to be authorized by the system.
  This authorization is made by Api Key, sending a request header
  as follows::

    ``Authorization: ApiKey <username>:<api_key>``

  Or as GET params::

    ``?username=<username>&api_key=<api_key>``


Available endpoints
-------------------

.. toctree::
  :maxdepth: 2

  collections-api
  issues-api
  journals-api
  sections-api
  sponsors-api
  uselicenses-api
  users-api
  changes-api


.. note::

  The API uses the ``Accepts`` HTTP headers in order to decide which one is
  the best format to be used. Options are: ``application/xml``,
  ``application/json`` and ``application/yaml``.

  If you try these requests in your browser, you will need to use the
  parameter ``format`` with one of the valid format types (xml, json or yaml).


We strongly recommend you to read `this page
<http://django-tastypie.readthedocs.org/en/v0.9.11/interacting.html>`_ to
know more about interacting with the API.
