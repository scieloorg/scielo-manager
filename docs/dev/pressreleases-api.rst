Press Releases API
============

List all press releases
-----------------------

Request::

  GET /api/v1/pressreleases

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **journal_pid**

    *String* of the **journal pid** as used by SciELO catalogs.

  **article_pid**

    *String* of the **journal pid** as used by SciELO catalogs.


Response::

  {

    "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 0
    },
    "objects": [
      {
        "articles": ["S0021-25712012000100001"],
        "id": 1,
        "issue_uri": "/api/v1/issues/1420/",
        "resource_uri": "/api/v1/pressreleases/1/",
        "translations": [
          "content": "Era uma vez...",
          "id": 1,
          "language": "pt",
          "resource_uri": "/api/v1/prtranslations/1/",
          "title": "Como a descoberta do XYZ mudou a humanidade",
        ],
        "issue_meta": {
          "short_title": "Ann. Ist. Super. Sanità",
          "volume": "45",
          "number": "4",
          "suppl_volume": null,
          "suppl_number": null,
          "publication_start_month": 10,
          "publication_end_month": 12,
          "publication_city": "Roma",
          "publication_year": 2009,
        },
        "doi": "http://dx.doi.org/10.4415/ANN_12_01_01"
      }
    ]

}


Get a single section
--------------------

Request::

  GET /api/v1/pressreleases/:id/

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.


Response::

  {
    "articles": ["S0021-25712012000100001"],
    "id": 1,
    "issue_uri": "/api/v1/issues/1420/",
    "resource_uri": "/api/v1/pressreleases/1/",
    "translations": [
      "content": "Era uma vez...",
      "id": 1,
      "language": "pt",
      "resource_uri": "/api/v1/prtranslations/1/",
      "title": "Como a descoberta do XYZ mudou a humanidade",
    ],
    "issue_meta": {
      "short_title": "Ann. Ist. Super. Sanità",
      "volume": "45",
      "number": "4",
      "suppl_volume": null,
      "suppl_number": null,
      "publication_start_month": 10,
      "publication_end_month": 12,
      "publication_city": "Roma",
      "publication_year": 2009,
    },
    "doi": "http://dx.doi.org/10.4415/ANN_12_01_01"
  }
