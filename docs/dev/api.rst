=============================================================
Journal Manager API
=============================================================

API to allow access to Journals, Issues and collections data.

**Current version:** API v1

Get Collections List
====================

Request::

  GET /api/v1/collections

Parameters:

  **parameters not necessary**

Optional Parameters:

  **callback**
    
    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/collections?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/collections?format=xml

Response Example::

  "http://journalmanager.scielo.org/api/v1/collections?format=xml"

Get a Collection Metadata
=========================

Request::

  GET /api/v1/collections/:<collection_name>

Parameters:

  **collection_name**

    *String* of the name of a collection, for example: Brasil, Chile, Cuba. If you doesn't know the 
    available collections you can fetch it with the "Get Collections List"

Optional Parameters:

  **callback**
    
    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/collections/Brasil/?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/collections/Brasil/?format=xml

Response Example::

  "http://journalmanager.scielo.org/api/v1/collections/Brasil/?format=xml"

Get Journals List
=================

Request::

  GET /api/v1/journals/collections/:<collection_name>

Parameters:

  **collection_name**

    *String* of the name of a collection, for example: Brasil, Chile, Cuba. If you doesn't know the 
    available collections you can fetch it with the "Get Collections List"

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/collections/Brasil?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/collections/Brasil?format=xml

Response Example::

  "http://journalmanager.scielo.org/api/v1/journals/collections/Brasil"

Get a Journal Metadata
======================

Request::

  GET /api/v1/journal/:<journal_issn>

Parameters:

  **issn**

    *String* of the ISSN. The ISSN could be the print or electronic ISSN.

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when
    using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/0102-6720?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/0102-6720?format=xml

Response Example::

  "http://journalmanager.scielo.org/api/v1/journals/0102-6720"

Get Journal Issues List
=========================

Request:

Parameters:

Optional Parameters:

Request Example:

Response Example:

Get a Journal Issue
====================

Request:

Parameters:

Optional Parameters:

Request Example:

Response Example: