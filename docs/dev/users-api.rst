Users API
=========

List all users
--------------

Request::

  GET /api/v1/users

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
  "meta": {
    "limit": 20,
    "next": null,
    "offset": 0,
    "previous": null,
    "total_count": 11
  },
  "objects": [
    {
      "date_joined": "2012-08-21T14:40:43",
      "first_name": "",
      "id": "14",
      "last_login": "2012-09-26T11:10:55.216742",
      "last_name": "",
      "resource_uri": "/api/v1/users/14/",
      "username": "gustavofonseca"
    }
  ]

Get a single user
-----------------

Request::

  GET /api/v1/users/:id/

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
    "date_joined": "2012-08-21T14:40:43",
    "first_name": "",
    "id": "14",
    "last_login": "2012-09-26T11:10:55.216742",
    "last_name": "",
    "resource_uri": "/api/v1/users/14/",
    "username": "gustavofonseca"
  }