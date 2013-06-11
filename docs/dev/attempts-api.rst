Attempts API
===========

The main idea behind the Attempts API is to provide ways for `Balaio <https://github.com/scieloorg/balaio>`_. 
to register and retrieve the "changes status" when validating the submission of an **Article Package** .

.. note::

  It is important to notice that by now SciELO Manager is not responsible
  for managing Articles.
  This feature is currently `under development <https://github.com/scieloorg/SciELO-Manager/tree/articles>`_.


:Available data:


article_title
  The article title extracted from the SciELO Publishing XML.

articlepkg_id 
  A number that identifies the article package at **Balaio**.

checkin_id
  A number that identifies an attempt of submission from a specific article.

collection_uri
  The collection who the attempt relates to.

created_at
  Date when the attempt was registered.

issue_label
  The issue label extracted from the SciELO Publishing XML.

journal_title
  The journal title extracted from the SciELO Publishing XML.

pkgmeta_filecount
  A number representing that files count inside found inside the article package

pkgmeta_filename
  The zipfile name related to the article package.

pkgmeta_filesize
  A number that represents the file size in bytes.

pkgmeta_md5
  An MD5 representation of the zipfile.

pkgmeta_submitter
  The string that identifies an authorized submitter

resource_uri
  A reference to the attempt in the attempts API.

status
  A list of status references


List all attempts
-----------------

Request::

  GET /api/v1/attempts

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

Response::

  { 
    "meta": { 
      "limit": 20, 
      "next": null,
      "offset": 0,
      "previous": null,
      "total_count": 2
    }, 
    "objects": [
      {
      "article_title": "Article Title1",
      "articlepkg_id": "3",
      "checkin_id": "1",
      "collection_uri": "http://www.scielo.br",
      "created_at": "2013-06-10T17:27:20.828551",
      "id": 1,
      "issue_label": "2013 v1 n2",
      "journal_title": "Journal Title",
      "pkgmeta_filecount": 12,
      "pkgmeta_filename": "file.zip",
      "pkgmeta_filesize": 213,
      "pkgmeta_md5": "1212jk1h21h2k1jh2kj11",
      "pkgmeta_submitter": "caboverdeee",
      "resource_uri": "/api/v1/attempts/1/",
      "status": []
    }
  }

Get a simple attempt
--------------------

Request::

  GET /api/v1/attempts/:id/

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

Response::

  { 
    "article_title": "Article Title1",
    "articlepkg_id": "3",
    "checkin_id": "1",
    "collection_uri": "http://www.scielo.br",
    "created_at": "2013-06-10T17:27:20.828551",
    "id": 1,
    "issue_label": "2013 v1 n2",
    "journal_title": "Journal Title",
    "pkgmeta_filecount": 12,
    "pkgmeta_filename": "file.zip",
    "pkgmeta_filesize": 213,
    "pkgmeta_md5": "1212jk1h21h2k1jh2kj11",
    "pkgmeta_submitter": "caboverdeee",
    "resource_uri": "/api/v1/attempts/1/",
    "status": []
  }

Register a attempt
------------------

Request::

  POST /api/v1/attempts

warning::
  
  Not all users with valid api token will be able to fetch a POST request, only those with the
  apropriate privileges.

Parameters:

  {
    "checkin_id":"1",
    "article_title": "Article Title1",
    "articlepkg_id": "3",
    "collection_uri": "http://www.scielo.br",
    "issue_label": "2013 v1 n2",
    "journal_title": "Journal Title",
    "pkgmeta_filecount": 12,
    "pkgmeta_filename": "file.zip",
    "pkgmeta_filesize": 213,
    "pkgmeta_md5": "1212jk1h21h2k1jh2kj11",
    "pkgmeta_submitter": "caboverdeee"
  }
