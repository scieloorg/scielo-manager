Issues API
==========

List all issues
---------------

Request:

  **API version 1**

  *GET /api/v1/issues*

  **API version 2**

  *GET /api/v2/issues*

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

  **eletronic_issn**

    *String* of the Electronic ISSN of the journal. Format ``1234-1234``

  **print_issn**

    *String* of the Print ISSN of the journal. Format ``1234-1234``

Response:

  **API version 1**::

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
          "use_license": {
            "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
            "id": ​5033,
            "is_default": false,
            "license_code": "BY/4.0",
            "reference_url": "http://creativecommons.org/licenses/by/4.0/",
            "resource_uri": "/api/v1/uselicenses/5033/"
          },
          "suppl_number": null,
          "suppl_volume": null,
          "total_documents": 16,
          "updated": "2012-07-24T21:53:23.909404",
          "volume": "29"
        }
      ]
    }

  **API version 2**::

    {
      "meta": {
        "limit": 20,
        "next": "/api/v2/issues/?username=admin&api_key=XXXX&limit=20&offset=20&format=json",
        "offset": 0,
        "previous": null,
        "total_count": 14052
      },
      "objects": [
        {
          "cover": null,
          "created": "1998-08-01T01:01:01",
          "ctrl_vocabulary": "",
          "editorial_standard": "",
          "id": 3273,
          "is_marked_up": false,
          "is_trashed": false,
          "journal": "/api/v2/journals/291/",
          "label": "39 (1)",
          "number": "1",
          "order": 1,
          "publication_end_month": 1,
          "publication_start_month": 1,
          "publication_year": 1997,
          "resource_uri": "/api/v2/issues/3273/",
          "sections": [
            {
              "code": "RIMTSP-3x88",
              "titles": [
                {
                  "lang": "en",
                  "title": "Invited review"
                }
              ]
            },
            {
              "code": "RIMTSP-4p5n",
              "titles": [
                {
                  "lang": "en",
                  "title": "Summaries of thesis"
                }
              ]
            },
            {
              "code": "RIMTSP-rk2c",
              "titles": [
                {
                  "lang": "en",
                  "title": "Mycology"
                }
              ]
            },
            {
              "code": "RIMTSP-n2f4",
              "titles": [
                {
                  "lang": "en",
                  "title": "Schistosomiasis"
                }
              ]
            },
            {
              "code": "RIMTSP-pp75",
              "titles": [
                {
                  "lang": "en",
                  "title": "Case Report"
                }
              ]
            },
            {
              "code": "RIMTSP-snc3",
              "titles": [
                {
                  "lang": "en",
                  "title": "Serodiagnosis"
                }
              ]
            },
            {
              "code": "RIMTSP-gw8j",
              "titles": [
                {
                  "lang": "en",
                  "title": "Vaccine studies"
                }
              ]
            },
            {
              "code": "RIMTSP-k87t",
              "titles": [
                {
                  "lang": "en",
                  "title": "Brief communication"
                }
              ]
            },
            {
              "code": "RIMTSP-xw5t",
              "titles": [
                {
                  "lang": "en",
                  "title": "Preliminary report"
                }
              ]
            },
            {
              "code": "RIMTSP-jhwj",
              "titles": [
                {
                  "lang": "en",
                  "title": "Technical essay"
                }
              ]
            },
            {
              "code": "RIMTSP-3bkm",
              "titles": [
                {
                  "lang": "en",
                  "title": "Entomology"
                }
              ]
            }
          ],
          "use_license": {
            "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
            "id": ​5033,
            "is_default": false,
            "license_code": "BY/4.0",
            "reference_url": "http://creativecommons.org/licenses/by/4.0/",
            "resource_uri": "/api/v2/uselicenses/5033/"
          },
          "spe_text": null,
          "suppl_number": "",
          "suppl_text": null,
          "suppl_volume": "",
          "thematic_titles": {

          },
          "total_documents": 12,
          "type": "regular",
          "updated": "2014-04-04T10:35:20.449578",
          "volume": "39"
        },
      ]
    }

Get a single issue
------------------

Request:

  **API version 1**

  *GET /api/v1/issues/:id*

  **API version 2**

  *GET /api/v2/issues/:id*

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
      "use_license": {
        "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
        "id": ​5033,
        "is_default": false,
        "license_code": "BY/4.0",
        "reference_url": "http://creativecommons.org/licenses/by/4.0/",
        "resource_uri": "/api/v1/uselicenses/5033/"
      },
      "suppl_number": null,
      "suppl_volume": null,
      "total_documents": 16,
      "updated": "2012-07-24T21:53:23.909404",
      "volume": "29"
    }

  **API version 2**::

    {
      "cover": null,
      "created": "1998-08-01T01:01:01",
      "ctrl_vocabulary": "",
      "editorial_standard": "",
      "id": 3273,
      "is_marked_up": false,
      "is_trashed": false,
      "journal": "/api/v2/journals/291/",
      "label": "39 (1)",
      "number": "1",
      "order": 1,
      "publication_end_month": 1,
      "publication_start_month": 1,
      "publication_year": 1997,
      "resource_uri": "/api/v2/issues/3273/",
      "sections": [
        {
          "code": "RIMTSP-3x88",
          "titles": [
            {
              "lang": "en",
              "title": "Invited review"
            }
          ]
        },
        {
          "code": "RIMTSP-4p5n",
          "titles": [
            {
              "lang": "en",
              "title": "Summaries of thesis"
            }
          ]
        },
        {
          "code": "RIMTSP-rk2c",
          "titles": [
            {
              "lang": "en",
              "title": "Mycology"
            }
          ]
        },
        {
          "code": "RIMTSP-n2f4",
          "titles": [
            {
              "lang": "en",
              "title": "Schistosomiasis"
            }
          ]
        },
        {
          "code": "RIMTSP-pp75",
          "titles": [
            {
              "lang": "en",
              "title": "Case Report"
            }
          ]
        },
        {
          "code": "RIMTSP-snc3",
          "titles": [
            {
              "lang": "en",
              "title": "Serodiagnosis"
            }
          ]
        },
        {
          "code": "RIMTSP-gw8j",
          "titles": [
            {
              "lang": "en",
              "title": "Vaccine studies"
            }
          ]
        },
        {
          "code": "RIMTSP-k87t",
          "titles": [
            {
              "lang": "en",
              "title": "Brief communication"
            }
          ]
        },
        {
          "code": "RIMTSP-xw5t",
          "titles": [
            {
              "lang": "en",
              "title": "Preliminary report"
            }
          ]
        },
        {
          "code": "RIMTSP-jhwj",
          "titles": [
            {
              "lang": "en",
              "title": "Technical essay"
            }
          ]
        },
        {
          "code": "RIMTSP-3bkm",
          "titles": [
            {
              "lang": "en",
              "title": "Entomology"
            }
          ]
        }
      ],
      "use_license": {
        "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"https://i.creativecommons.org/l/by/4.0/80x15.png\" /></a><br />This work is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/4.0/\">Creative Commons Attribution 4.0 International License</a>.",
        "id": ​5033,
        "is_default": false,
        "license_code": "BY/4.0",
        "reference_url": "http://creativecommons.org/licenses/by/4.0/",
        "resource_uri": "/api/v2/uselicenses/5033/"
      },
      "spe_text": null,
      "suppl_number": "",
      "suppl_text": null,
      "suppl_volume": "",
      "thematic_titles": {

      },
      "total_documents": 12,
      "type": "regular",
      "updated": "2014-04-04T10:35:20.449578",
      "volume": "39"
    }

