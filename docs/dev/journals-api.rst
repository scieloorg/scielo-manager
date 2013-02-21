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

  **pubstatus**

    *String* of the pub_status. Options are **current, deceased, suspended or inprogress**. 
    It is important to note that this param can be repeated in the same query in order to perform 
    as an OR query.

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
      "collections": "/api/v1/collections/1/",
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
      "twitter_user": "redescielo",
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

Request::

  GET /api/v1/journals/:id/

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
    "twitter_user": "redescielo",
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
