==================
SciELO Manager API
==================

All the catalographic data, managed by SciELO Manager, are made
available by a RESTful API. By now, the API provides a read-only
access, but for future releases more methods will be added.

If you have any problems or requests please contact
`support <http://groups.google.com/group/scielo-discuss/>`_.

**Current version:** API v1


Available endpoints
-------------------

* Collections

  * List all collections
  * Get a single collection

* Issues

  * List all issues
  * Get a single issue

* Journals

  * List all journals
  * Get a single journal

* Sections

  * List all sections
  * Get a single section

* Sponsors

  * List all sponsors
  * Get a single sponsor

* Use Licenses

  * List all use licenses
  * Get a single use license

* Users

  * List all users
  * Get a single user


Collections API
===============

List all collections
--------------------

Request::

  GET /api/v1/collections

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
    "total_count": 1
  },
  "objects": [
    {
      "acronym": "scl",
      "address": "Rua Machado Bitencourt",
      "address_complement": "",
      "address_number": "430",
      "city": "São Paulo",
      "country": "Brasil",
      "email": "scielo@scielo.org",
      "fax": "",
      "id": "1",
      "logo": null,
      "name": "Brasil",
      "name_slug": "brasil",
      "phone": "",
      "resource_uri": "/api/v1/collections/1/",
      "state": "São Paulo",
      "url": "http://www.scielo.br",
      "zip_code": null
    }
  ]


Get a single collection
-----------------------


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


Journals API
============

List all journals
--------------------

Request::

  GET /api/v1/journals

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **is_trashed**

    *Boolean* - Filters by the trashed status.

  **collection**

    *String* of the **name_slug** of the collection to be used as a
    filter param.

Response::

  {
  "meta": {
    "limit": 20,
    "next": "/api/v1/journals/?offset=20&limit=20&format=json",
    "offset": 0,
    "previous": null,
    "total_count": 300
  },
  "objects": [
    {
      "abstract_keyword_languages": null,
      "acronym": "ABCD",
      "collections": [
        "/api/v1/collections/1/"
      ],
      "contact": null,
      "copyrighter": "Colégio Brasileiro de Cirurgia Digestiva - CBCD",
      "cover": null,
      "created": "2010-03-23T00:00:00",
      "creator": "/api/v1/users/1/",
      "ctrl_vocabulary": "decs",
      "editor_address": "",
      "editor_email": "",
      "editorial_standard": "vancouv",
      "eletronic_issn": "",
      "final_num": "",
      "final_vol": "",
      "final_year": null,
      "frequency": "Q",
      "id": "1",
      "index_coverage": "ll - lilacs",
      "init_num": "1",
      "init_vol": "1",
      "init_year": "1986",
      "is_trashed": false,
      "issues": [
        "/api/v1/issues/5674/",
        "/api/v1/issues/5675/",
        "/api/v1/issues/5676/",
        "/api/v1/issues/5677/",
        "/api/v1/issues/5678/",
        "/api/v1/issues/5679/",
        "/api/v1/issues/5680/",
        "/api/v1/issues/5681/",
        "/api/v1/issues/5682/",
        "/api/v1/issues/5683/",
        "/api/v1/issues/5684/",
        "/api/v1/issues/5685/",
        "/api/v1/issues/5686/",
        "/api/v1/issues/5687/",
        "/api/v1/issues/5688/"
      ],
      "languages": [
        "en",
        "pt"
      ],
      "logo": null,
      "medline_code": null,
      "medline_title": null,
      "missions": [
        [
          "en",
          "To publish articles of clinical and experimental studies that foster the advancement of research, teaching and assistance in surgical, clinical, and endoscopic gastroenterology, and related areas."
        ],
        [
          "pt",
          "Publicar  artigos de estudos clínicos e experimentais que contribuam para o desenvolvimento da pesquisa, ensino e assistência na área gastroenterologia cirúrgica, clínica, endoscópica e outras correlatas."
        ],
        [
          "es",
          "Publicar artículos de estudios clínicos y experimentales que aporten para el desarrollo de la pesquisa, enseñanza y asistencia en el área gastroenterología quirúrgica, clínica, endoscópica y otras correlacionadas."
        ]
      ],
      "national_code": "083653-2",
      "notes": "",
      "other_previous_title": "",
      "other_titles": [
        [
          "other",
          "Arquivos Brasileiros de Cirurgia Digestiva"
        ],
        [
          "paralleltitle",
          "Brazilian Archives of Digestive Surgery"
        ]
      ],
      "print_issn": "0102-6720",
      "pub_level": "CT",
      "pub_status": "current",
      "pub_status_history": [
        {
          "date": "2010-05-01T00:00:00",
          "status": "current"
        }
      ],
      "pub_status_reason": "",
      "publication_city": "",
      "publisher_country": "",
      "publisher_name": "",
      "publisher_state": "",
      "resource_uri": "/api/v1/journals/1/",
      "scielo_issn": "print",
      "secs_code": "6633",
      "sections": [
        "/api/v1/sections/5676/",
        "/api/v1/sections/5677/",
        "/api/v1/sections/5678/",
        "/api/v1/sections/5679/",
        "/api/v1/sections/5680/",
        "/api/v1/sections/5681/",
        "/api/v1/sections/5682/",
        "/api/v1/sections/5683/",
        "/api/v1/sections/5684/",
        "/api/v1/sections/5685/"
      ],
      "short_title": "ABCD, arq. bras. cir. dig.",
      "sponsors": [
        "/api/v1/sponsors/2/"
      ],
      "study_areas": [
        "Health Sciences"
      ],
      "subject_descriptors": "medicina\ncirurgia\ngastroenterologia\ngastroenterologia",
      "title": "ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)",
      "title_iso": "ABCD, arq. bras. cir. dig",
      "updated": "2012-09-05T15:41:50.283762",
      "url_journal": null,
      "url_online_submission": null,
      "use_license": {
        "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by-nc/3.0/80x15.png\" /></a> Todo el contenido de esta revista, excepto dónde está identificado, est&#225; bajo una <a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\">Licencia Creative Commons</a>",
        "id": "1",
        "license_code": "BY-NC",
        "reference_url": null,
        "resource_uri": "/api/v1/uselicenses/1/"
      }
    }
  ]

Get a single journal
--------------------


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


Sponsors API
============

List all sponsors
-----------------

Request::

  GET /api/v1/sponsors

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
    "next": "/api/v1/sponsors/?offset=20&limit=20&format=json",
    "offset": 0,
    "previous": null,
    "total_count": 157
  },
  "objects": [
    {
      "acronym": "",
      "address": "",
      "address_complement": "",
      "address_number": "",
      "cel": "",
      "city": "",
      "complement": "",
      "country": "",
      "created": "2012-07-24T21:47:05.463276",
      "email": "",
      "fax": "",
      "id": "264",
      "is_trashed": false,
      "name": "ANPEd, CNPq, UNESCO",
      "phone": "",
      "resource_uri": "/api/v1/sponsors/264/",
      "state": "",
      "updated": "2012-07-24T21:47:05.463312",
      "zip_code": null
    }
  ]

Get a single sponsor
--------------------

Use Licenses API
================

List all use licenses
---------------------

Request::

  GET /api/v1/uselicenses

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

Get a single use license
------------------------


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