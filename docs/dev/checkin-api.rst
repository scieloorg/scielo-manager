Notices API
===============

List all notices
--------------------

Request:

  **API version 1**

  *GET /api/v1/notices*

  **API version 2**

  *GET /api/v2/notices*

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
        "total_count": 6
      },
      "objects": [
        {
          "checkin": "/api/v2/checkins/5/",
          "checkpoint": "checkin",
          "created_at": "2014-08-11T13:36:41.147189",
          "id": 72,
          "message": "bla",
          "resource_uri": "/api/v2/notices/72/",
          "stage": "Checkin",
          "status": "SERV_END"
        },
      ]
    }


Get a single notice
------------------------------

Request:

  **API version 1**

  *GET /api/v1/notices/:id/*

  **API version 2**

  *GET /api/v2/notices/:id/*


Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.


Response:

  **API version 1 and version 2**::

    {
      checkin: "/api/v2/checkins/5/",
      checkpoint: "checkin",
      created_at: "2014-08-11T13:36:41.147189",
      id: 72,
      message: "bla",
      resource_uri: "/api/v2/notices/72/",
      stage: "Checkin",
      status: "SERV_END"
    }
