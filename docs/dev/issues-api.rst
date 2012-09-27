Issues API
==========

List all issues
---------------

Request::

  GET /api/v1/issues

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

  **collection**

    *String* of the **name_slug** of the collection to be used as a
    filter param.

Response::

  {
  "meta": {
    "limit": 20,
    "next": "/api/v1/issues/?offset=20&limit=20&format=json",
    "offset": 0,
    "previous": null,
    "total_count": 13202
  },
  "objects": [
    {
      "cover": null,
      "created": "2012-07-24T21:53:23.909378",
      "ctrl_vocabulary": "",
      "editorial_standard": "",
      "id": "1",
      "is_marked_up": false,
      "is_press_release": false,
      "is_trashed": false,
      "journal": "/api/v1/journals/236/",
      "label": "v29n3",
      "number": "3",
      "order": 0,
      "publication_end_month": 0,
      "publication_start_month": 9,
      "publication_year": 1998,
      "resource_uri": "/api/v1/issues/1/",
      "sections": [
        "/api/v1/sections/1266/",
        "/api/v1/sections/1254/",
        "/api/v1/sections/1261/",
        "/api/v1/sections/1253/",
        "/api/v1/sections/1255/",
        "/api/v1/sections/1257/",
        "/api/v1/sections/1264/",
        "/api/v1/sections/1262/"
      ],
      "suppl_number": null,
      "suppl_volume": null,
      "total_documents": 16,
      "updated": "2012-07-24T21:53:23.909404",
      "volume": "29"
    }
  ]


Get a single issue
------------------

Request::

  GET /api/v1/issues/:id/

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
    "cover": null,
    "created": "2012-07-24T21:53:23.909378",
    "ctrl_vocabulary": "",
    "editorial_standard": "",
    "id": "1",
    "is_marked_up": false,
    "is_press_release": false,
    "is_trashed": false,
    "journal": "/api/v1/journals/236/",
    "label": "v29n3",
    "number": "3",
    "order": 0,
    "publication_end_month": 0,
    "publication_start_month": 9,
    "publication_year": 1998,
    "resource_uri": "/api/v1/issues/1/",
    "sections": [
      "/api/v1/sections/1266/",
      "/api/v1/sections/1254/",
      "/api/v1/sections/1261/",
      "/api/v1/sections/1253/",
      "/api/v1/sections/1255/",
      "/api/v1/sections/1257/",
      "/api/v1/sections/1264/",
      "/api/v1/sections/1262/"
    ],
    "suppl_number": null,
    "suppl_volume": null,
    "total_documents": 16,
    "updated": "2012-07-24T21:53:23.909404",
    "volume": "29"
  }