Sections API
============

List all sections
-----------------

Request:

  **API version 1**

  *GET /api/v1/sections*

  **API version 2**

  *GET /api/v2/sections*


Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **journal ID**

    *Int* of the **journal id** to be used as a filter param.

  **journal_eissn**

    *String* - Eletronic ISSN of the journal used as filter param Ex.: 0034-8910.

  **journal_pissn**

    *String* - Print ISSN of the journal used as filter param Ex.: 1519-6984.


Response:

  **API version 1**::

    {
      "meta": {
        "limit": 20,
        "next": "/api/v1/sections/?offset=20&limit=20&format=json",
        "offset": 0,
        "previous": null,
        "total_count": 6543
      },
      "objects": [
        {
          "code": "BJCE110",
          "created": "2012-07-24T21:47:33.007925",
          "id": "1",
          "is_trashed": false,
          "issues": [
            "/api/v1/issues/7958/",
            "/api/v1/issues/7956/",
            "/api/v1/issues/7954/",
            "/api/v1/issues/7942/"
          ],
          "journal": "/api/v1/journals/35/",
          "resource_uri": "/api/v1/sections/1/",
          "titles": [
            [
              "en",
              "Reactors Engineering and Catalysis"
            ]
          ],
          "updated": "2012-07-24T21:47:33.007958"
        }
      ]
    }

  **API version 2**::

    {
      "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 11
      },
      "objects": [
        {
          "code": "BJOCE-6gfj",
          "created": "2014-04-04T10:33:12.932102",
          "id": 5865,
          "is_trashed": false,
          "issues": [
            "/api/v2/issues/13321/",
            "/api/v2/issues/13332/"
          ],
          "journal": "/api/v2/journals/70/",
          "resource_uri": "/api/v2/sections/5865/",
          "titles": {
            "pt": "Editorial"
            "en": "Editorial"
          },
          "updated": "2014-04-04T10:33:12.932124"
        }
      ]
    }


Get a single section
--------------------

Request::
  **API version 1**

  *GET /api/v1/sections/:id/*

  **API version 2**

  *GET /api/v2/sections/:id/*


Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.


Response:


  **API version 1**::

    {
      "code": "BJCE110",
      "created": "2012-07-24T21:47:33.007925",
      "id": "1",
      "is_trashed": false,
      "issues": [
        "/api/v1/issues/7958/",
        "/api/v1/issues/7956/",
        "/api/v1/issues/7954/",
        "/api/v1/issues/7942/"
      ],
      "journal": "/api/v1/journals/35/",
      "resource_uri": "/api/v1/sections/1/",
      "titles": [
        [
          "en",
          "Reactors Engineering and Catalysis"
        ]
      ],
      "updated": "2012-07-24T21:47:33.007958"
    }

  **API version 2**::

    {
      "code": "CSP-9nc7",
      "created": "2014-04-03T15:07:56.313139",
      "id": 6,
      "is_trashed": false,
      "issues": [
        "/api/v2/issues/669/",
        "/api/v2/issues/718/",
        "/api/v2/issues/778/"
      ],
      "journal": "/api/v2/journals/8/",
      "resource_uri": "/api/v2/sections/6/",
      "titles": {
        "en": "Special Article",
        "pt": "Artigo Especial"
      },
      "updated": "2014-04-03T15:07:56.313161"
    }
