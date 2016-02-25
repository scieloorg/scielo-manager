Notices API
===============

List all notices
----------------

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
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 1
      },
      "objects": [
        {
        checkin: "/api/v1/checkins/1/",
        checkpoint: "validation",
        created_at: "2014-07-30T15:09:50.720126",
        id: 34,
        message: "",
        resource_uri: "/api/v2/notices/34/",
        stage: "",
        status: "SERV_END"
        }
      ]
    }


Get a single notices
-----------------------

Request::

  GET /api/v1/notices/:id/

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
      checkin: "/api/v2/checkins/2/",
      checkpoint: "validation",
      created_at: "2014-07-30T15:09:50.720126",
      id: 34,
      message: "",
      resource_uri: "/api/v2/notices/34/",
      stage: "",
      status: "SERV_END"
    }
