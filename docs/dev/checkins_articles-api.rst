Checkins Articles API
=====================

List all Checkins Articles
-------------------------

Request:

  **API version 1**

  *GET /api/v1/checkins_articles*

  **API version 2**

  *GET /api/v2/checkins_articles*

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
        "limit": 200,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
      },
      "objects": [
        {
          "article_title": "teste",
          "articlepkg_ref": "12",
          "eissn": "23",
          "id": 1,
          "issue_label": "23",
          "journal_title": "teste",
          "journals": [
            "/api/v2/journals/18/"
          ],
          "pissn": "23",
          "resource_uri": "/api/v2/checkins_articles/1/"
        },
      ]
    }


Get a single checkins articles
------------------------------

Request:

  **API version 1**

  *GET /api/v1/checkins_articles/:id/*

  **API version 2**

  *GET /api/v2/checkins_articles/:id/*


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
      "article_title": "teste",
      "articlepkg_ref": "12",
      "eissn": "23",
      "id": 1,
      "issue_label": "23",
      "journal_title": "teste",
      "journals": [
        "/api/v2/journals/18/"
      ],
      "pissn": "23",
      "resource_uri": "/api/v2/checkins_articles/1/"
    }
