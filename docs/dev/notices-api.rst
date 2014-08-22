Notices API
===============

List all notices
----------------

Request:

  **API version 1**

  *GET /api/v1/collections*

  **API version 2**

  *GET /api/v2/collections*

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.


Allowed Method:

  GET, PUT, POST

Response:

  **API version 1 and version 2**::

    {
      "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 1
      },
      "objects": [
        {
          "acronym": "scl",
          "address": "Rua Machado Bitencourt",
          "address_complement": "",
          "address_number": "430",
          "city": "São Paulo",
          "country": "Brasil",
          "email": "scielo@scielo.org",
          "fax": "",
          "id": "1",
          "logo": null,
          "name": "Brasil",
          "name_slug": "brasil",
          "phone": "",
          "resource_uri": "/api/v1/collections/1/",
          "state": "São Paulo",
          "url": "http://www.scielo.br",
          "zip_code": null
        }
      ]
    }


Get a single notices
-----------------------

Request::

  GET /api/v1/collections/:id/

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.


Response:

  **API version 1, version 2**::

    {
      "acronym": "scl",
      "address": "Rua Machado Bitencourt",
      "address_complement": "",
      "address_number": "430",
      "city": "São Paulo",
      "country": "Brasil",
      "email": "scielo@scielo.org",
      "fax": "",
      "id": "1",
      "logo": null,
      "name": "Brasil",
      "name_slug": "brasil",
      "phone": "",
      "resource_uri": "/api/v1/collections/1/",
      "state": "São Paulo",
      "url": "http://www.scielo.br",
      "zip_code": null
    }
