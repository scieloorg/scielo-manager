Use Licenses API
================

List all use licenses
---------------------

Request:

  **API version 1**

  *GET /api/v1/uselicenses*

  **API version 2**

  *GET /api/v2/uselicenses*

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
        "total_count": 4
      },
      "objects": [
        {
          "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> All the contents of the journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\">Creative Commons Attribution License</a>",
          "id": "3",
          "license_code": "",
          "reference_url": null,
          "resource_uri": "/api/v1/uselicenses/3/"
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
        "total_count": 4
      },
      "objects": [
        {
          "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> All the contents of the journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\">Creative Commons Attribution License</a>",
          "id": "3",
          "license_code": "",
          "reference_url": null,
          "resource_uri": "/api/v1/uselicenses/3/"
        }
      ]
    }

Get a single use license
------------------------

Request:

  **API version 1**

  *GET /api/v1/uselicenses/:id/*

  **API version 2**

  *GET /api/v2/uselicenses/:id/*

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
      "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> All the contents of the journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\">Creative Commons Attribution License</a>",
      "id": "3",
      "license_code": "",
      "reference_url": null,
      "resource_uri": "/api/v1/uselicenses/3/"
    }

  **API version 2**::

    {
      "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> All the contents of the journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\">Creative Commons Attribution License</a>",
      "id": "3",
      "license_code": "",
      "reference_url": null,
      "resource_uri": "/api/v1/uselicenses/3/"
    }
