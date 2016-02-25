Users API
=========

List all users
--------------

Request:

  **API version 1**

  *GET /api/v1/users*

  **API version 2**

  *GET /api/v2/users*

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
    }

  **API version 2**::

    {
      "meta": {
        "limit": 20,
        "next": null,
        "offset": 0,
        "previous": null,
        "total_count": 2
      },
      "objects": [
        {
          "collections": [
            {
              "is_default": true,
              "is_manager": false,
              "name": "Saude Publica"
            },
            {
              "is_default": true,
              "is_manager": false,
              "name": "Brasil"
            }
          ],
          "date_joined": "2014-08-19T10:51:34",
          "first_name": "Usu\u00c3\u00a1rio de teste",
          "id": 13,
          "last_login": "2014-08-19T10:54:46",
          "last_name": "test",
          "resource_uri": "/api/v2/users/13/",
          "username": "teste"
        },
      ]
    }

Get a single user
-----------------

Request:

  **API version 1**

  *GET /api/v1/users/:id/*

  **API version 2**

  *GET /api/v2/users/:id/*

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
      "date_joined": "2012-08-21T14:40:43",
      "first_name": "",
      "id": "14",
      "last_login": "2012-09-26T11:10:55.216742",
      "last_name": "",
      "resource_uri": "/api/v1/users/14/",
      "username": "gustavofonseca"
    }

  **API version 2**::

    {
      "collections": [
        {
          "is_default": true,
          "is_manager": false,
          "name": "Saude Publica"
        },
        {
          "is_default": true,
          "is_manager": false,
          "name": "Brasil"
        }
      ],
      "date_joined": "2014-08-19T10:51:34",
      "first_name": "Usu\u00c3\u00a1rio de teste",
      "id": 13,
      "last_login": "2014-08-19T10:54:46",
      "last_name": "test",
      "resource_uri": "/api/v2/users/13/",
      "username": "teste"
    }
