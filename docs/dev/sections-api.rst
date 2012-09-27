Sections API
============

List all sections
-----------------

Request::

  GET /api/v1/sections

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **journal**

    *Int* of the **journal id** to be used as a filter param.

Response::

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


Get a single section
--------------------

Request::

  GET /api/v1/sections/:id/

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
