Journals API
============

List all journals
--------------------

Request:

  **API version 1**

  *GET /api/v1/journals*

  **API version 2**

  *GET /api/v2/journals*

Parameters:

  **--**

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json,
    yml**.

  **collection**

    *String* of the **name_slug** of the collection to be used as a
    filter param.

  **is_trashed**

    *Boolean* - Filters by the trashed status.

  **eletronic_issn**

    *String* - Eletronic ISSN of the journal used as filter param Ex.: 0034-8910.

  **print_issn**

    *String* - Print ISSN of the journal used as filter param Ex.: 1519-6984.

  **pubstatus**

    *String* of the pub_status. Options are **current, deceased, suspended or inprogress**.
    It is important to note that this param can be repeated in the same query in order to perform
    as an OR query.

Response:

  **API version 1**::

    {
      "meta": {
        "limit": 20,
        "next": "/api/v1/journals/?username=jamil.atta&api_key=XXXX&limit=20&offset=20&format=json",
        "offset": 0,
        "previous": null,
        "total_count": 192
      },
      "objects": [
        {
          "abstract_keyword_languages": null,
          "acronym": "ABM",
          "collections": "/api/v1/collections/7/",
          "contact": null,
          "copyrighter": "Instituto de Ecolog\u00c3\u00ada, A.C. Centro Regional del Baj\u00c3\u00ado",
          "cover": null,
          "created": "2009-11-03T00:00:00",
          "creator": "/api/v1/users/1/",
          "ctrl_vocabulary": "nd",
          "current_ahead_documents": 0,
          "editor_address": "Av. L\u00c3\u00a1zaro C\u00c3\u00a1rdenas 253,, P\u00c3\u00a1tzcuaro, Michoac\u00c3\u00a1n, M\u00c3\u00a9xico, A.P. 386        C.P.  61600 ",
          "editor_address_city": "",
          "editor_address_country": "",
          "editor_address_state": "",
          "editor_address_zip": "",
          "editor_email": "",
          "editor_name": "",
          "editor_phone1": "",
          "editor_phone2": null,
          "editorial_standard": "other",
          "eletronic_issn": "",
          "final_num": "",
          "final_vol": "",
          "final_year": null,
          "frequency": "Q",
          "id": 83,
          "index_coverage": "agricola, biological abstracts, cab abstracts, conacyt (indice de revistas mexicanas de investigaci\u00c3\u00b3n cient\u00c3\u00adfica y tecnol\u00c3\u00b3gica), forestry abstracts, grasslands and forage abstracts, peri\u00c3\u00b3dica (indice de revistas latinoamericanas en ciencias), plant breeding abstracts, protozoological abstracts, review of medical and veterinary mycology, review of plant pathology, rice abstracts, rural development abstracts, science citation index, seed abstracts, weed abstracts, nutrition abstracts and reviews. serie b: livestock and feeding, science citation index expanded, red alyc, dialnet, directory of open access journals (doaj), fuente acad\u00c3\u00a9mica",
          "init_num": "1",
          "init_vol": null,
          "init_year": "1988",
          "is_indexed_aehci": false,
          "is_indexed_scie": true,
          "is_indexed_ssci": false,
          "is_trashed": false,
          "issues": [
            "/api/v1/issues/4079/",
            "/api/v1/issues/4080/",
            "/api/v1/issues/4082/",
            "/api/v1/issues/4083/",
            "/api/v1/issues/4085/",
            "/api/v1/issues/4086/",
            "/api/v1/issues/4087/",
            "/api/v1/issues/4084/",
            "/api/v1/issues/4081/",
            "/api/v1/issues/4088/",
            "/api/v1/issues/4077/",
            "/api/v1/issues/4078/",
            "/api/v1/issues/4089/",
            "/api/v1/issues/4090/",
            "/api/v1/issues/4091/",
            "/api/v1/issues/4092/",
            "/api/v1/issues/4094/",
            "/api/v1/issues/4093/",
            "/api/v1/issues/4096/",
            "/api/v1/issues/4095/",
            "/api/v1/issues/4098/",
            "/api/v1/issues/4097/",
            "/api/v1/issues/4099/",
            "/api/v1/issues/4100/",
            "/api/v1/issues/4101/",
            "/api/v1/issues/5526/",
            "/api/v1/issues/5683/"
          ],
          "languages": [
            "en",
            "es"
          ],
          "logo": null,
          "medline_code": null,
          "medline_title": null,
          "missions": [
            [
              "en",
              "Acta bot\u00c3\u00a1nica mexicana is a publication of the Institute of Ecology A.C. that publishes original and unpublished works on botanical topics particularly those related to Mexican plants. Acta bot\u00c3\u00a1nica mexicana publishes articles written mainly in Spanish language, although certain documents written in English, French and Portuguese are also accepted."
            ],
            [
              "pt",
              "Acta bot\u00c3\u00a1nica mexicana, \u00c3\u00a9 uma publica\u00c3\u00a7\u00c3\u00a3o do Instituto de Ecologia A.C. que publica trabalhos originais e in\u00c3\u00a9ditos sobre temas bot\u00c3\u00a2nicos e em particular os relacionados com plantas mexicanas. Acta bot\u00c3\u00a1nica mexicana publica artigos escritos principalmente em idioma espanhol, aceitando-se certa propor\u00c3\u00a7\u00c3\u00a3o de trabalhos redigidos em ingl\u00c3\u00aas, franc\u00c3\u00aas e portugu\u00c3\u00aas."
            ],
            [
              "es",
              "Acta bot\u00c3\u00a1nica mexicana, es una publicaci\u00c3\u00b3n del Instituto de Ecolog\u00c3\u00ada A.C. que publica trabajos originales e in\u00c3\u00a9ditos sobre temas bot\u00c3\u00a1nicos y en particular los relacionados con plantas mexicanas. Acta bot\u00c3\u00a1nica mexicana publica art\u00c3\u00adculos escritos principalmente en idioma espa\u00c3\u00b1ol, acept\u00c3\u00a1ndose cierta proporci\u00c3\u00b3n de trabajos redactados en ingl\u00c3\u00a9s, franc\u00c3\u00a9s y portugu\u00c3\u00a9s."
            ]
          ],
          "national_code": null,
          "notes": "",
          "other_previous_title": "",
          "other_titles": [

          ],
          "previous_ahead_documents": 0,
          "previous_title": null,
          "print_issn": "0187-7151",
          "pub_level": "CT",
          "pub_status": "current",
          "pub_status_history": [
            {
              "date": "2008-10-01T00:00:00",
              "status": "current"
            }
          ],
          "pub_status_reason": "",
          "publication_city": "P\u00c3\u00a1tzcuaro",
          "publisher_country": "MX",
          "publisher_name": "Instituto de Ecolog\u00c3\u00ada A.C., Centro Regional del Baj\u00c3\u00ado",
          "publisher_state": "Michoac\u00c3\u00a1n",
          "resource_uri": "/api/v1/journals/83/",
          "scielo_issn": "print",
          "secs_code": "",
          "sections": [
            "/api/v1/sections/2194/",
            "/api/v1/sections/2195/",
            "/api/v1/sections/2196/"
          ],
          "short_title": "Act. Bot. Mex",
          "sponsors": [

          ],
          "study_areas": [
            "Biological Sciences"
          ],
          "subject_descriptors": "biologia\nbotanica",
          "succeeding_title": null,
          "title": "Acta bot\u00c3\u00a1nica mexicana",
          "title_iso": "Act. Bot. Mex",
          "twitter_user": null,
          "updated": "2014-06-18T13:38:05.742274",
          "url_journal": "http://www1.inecol.edu.mx/abm",
          "url_online_submission": null,
          "use_license": {
            "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by-nc/3.0/80x15.png\" /></a> Todo el contenido de esta revista, excepto d\u00c3\u00b3nde est\u00c3\u00a1 identificado, est&#225; bajo una <a rel=\"license\" href=\"http://creativecommons.org/licenses/by-nc/3.0/\">Licencia Creative Commons</a>",
            "id": 1042,
            "is_default": true,
            "license_code": "BY-NC",
            "reference_url": "",
            "resource_uri": "/api/v1/uselicenses/1042/"
          }
        },
      ]
    }

  **API version 2**::

    {
      "meta": {
        "limit": 20,
        "next": "/api/v2/journals/?username=admin&api_key=XXXX&limit=20&offset=20&format=json",
        "offset": 0,
        "previous": null,
        "total_count": 327
      },
      "objects": [
        {
            "abstract_keyword_languages": null,
            "acronym": "ASAGR",
            "collections": [
              "Brasil"
            ],
            "contact": null,
            "copyrighter": "Editora da Universidade Estadual de Maring\u00c3\u00a1 - EDUEM",
            "cover": null,
            "created": "2011-02-16T00:00:00",
            "creator": "/api/v2/users/1/",
            "ctrl_vocabulary": "nd",
            "current_ahead_documents": 0,
            "editor_address": "Av. Colombo, 5790, bloco 40, 87020-900 - Maring\u00c3\u00a1 PR/ Brasil, Tel.: (55 44) 3011-4253, Fax: (55 44) 3011-1392",
            "editor_address_city": "",
            "editor_address_country": "",
            "editor_address_state": "",
            "editor_address_zip": "",
            "editor_email": "",
            "editor_name": "",
            "editor_phone1": "",
            "editor_phone2": null,
            "editorial_standard": "nbr6023",
            "eletronic_issn": "1807-8621",
            "final_num": "",
            "final_vol": "",
            "final_year": null,
            "frequency": "Q",
            "id": 33,
            "index_coverage": "isi\nscopus\nabstract journal\nbiosis (u. k.)\nagris - international information system for the agricultural sciences and technology\nagrobase - base de dados bibliogr\u00c3\u00a1fica de literatura agr\u00c3\u00adcola brasileira\nbiological abstracts\ncab abstracts\nchemical abstracts\nelsevier biobase-cabs-current awareness in biological sciences\nebsco - fonte acad\u00c3\u00aamica\nebsco - toc premier\nebsco - academic search premier\nperiodica\ntropag - royal tropical institute\nulrich\u00c2\u00b4s international periodicals directory\ngale cengage learning - academic one file\ngale cengage learning - informe acad\u00c3\u00aamico\ndoaj\nlatindex\nbase bielefeld\noaister",
            "init_num": "1",
            "init_vol": "1",
            "init_year": "1998",
            "is_indexed_aehci": false,
            "is_indexed_scie": false,
            "is_indexed_ssci": false,
            "is_trashed": false,
            "issues": [
              "/api/v2/issues/13692/",
              "/api/v2/issues/13693/",
              "/api/v2/issues/13694/",
              "/api/v2/issues/13695/",
              "/api/v2/issues/13696/",
              "/api/v2/issues/13690/",
              "/api/v2/issues/13697/",
              "/api/v2/issues/13691/",
              "/api/v2/issues/13688/",
              "/api/v2/issues/13698/",
              "/api/v2/issues/13689/",
              "/api/v2/issues/13699/",
              "/api/v2/issues/13700/"
            ],
            "languages": [
              "en"
            ],
            "logo": null,
            "medline_code": null,
            "medline_title": null,
            "missions": {
              "en": "To establish the public inscription of knowledge and its preservation; To publish results of research comprising ideas and new scientific suggestions; To publicize worldwide information and knowledge produced by the scientific community; To speech the process of scientific communication in Agronomy.",
              "es": "Habilitar el registro p\u00c3\u00bablico del conocimiento y su conservaci\u00c3\u00b3n; Publicar los resultados de investigaciones con nuevas ideas y propuestas cient\u00c3\u00adficas, difundir informaci\u00c3\u00b3n y conocimientos generados por la comunidad cient\u00c3\u00adfica; acelerar el proceso de comunicaci\u00c3\u00b3n cient\u00c3\u00adfica en el campo de la Agronom\u00c3\u00ada.",
              "pt": "Viabilizar o registro p\u00c3\u00bablico do conhecimento e sua preserva\u00c3\u00a7\u00c3\u00a3o; Publicar resultados de pesquisas envolvendo id\u00c3\u00a9ias e novas propostas cient\u00c3\u00adficas; Disseminar a informa\u00c3\u00a7\u00c3\u00a3o e o conhecimento gerados pela comunidade cient\u00c3\u00adfica; Agilizar o processo de comunica\u00c3\u00a7\u00c3\u00a3o cient\u00c3\u00adfica na \u00c3\u00a1rea de Agronomia."
            },
            "national_code": "098378-0",
            "notes": "",
            "other_previous_title": "",
            "other_titles": {

            },
            "previous_ahead_documents": 0,
            "previous_title": null,
            "print_issn": "",
            "pub_level": "CT",
            "pub_status": {
              "Brasil": "current"
            },
            "pub_status_history": [
              {
                "date": "2014-04-23T10:30:32.777749",
                "status": "current"
              }
            ],
            "pub_status_reason": {
              "Brasil": ""
            },
            "publication_city": "Maring\u00c3\u00a1",
            "publisher_country": "BR",
            "publisher_name": "Editora da Universidade Estadual de Maring\u00c3\u00a1 - EDUEM",
            "publisher_state": "PR",
            "resource_uri": "/api/v2/journals/33/",
            "scielo_issn": "electronic",
            "secs_code": "",
            "sections": [
              "/api/v2/sections/6629/",
              "/api/v2/sections/6630/",
              "/api/v2/sections/6631/",
              "/api/v2/sections/6632/",
              "/api/v2/sections/6633/",
              "/api/v2/sections/6634/",
              "/api/v2/sections/6635/",
              "/api/v2/sections/6636/"
            ],
            "short_title": "Acta Sci., Agron.",
            "sponsors": [
              "/api/v2/sponsors/11/"
            ],
            "study_areas": [

            ],
            "subject_descriptors": "agronomia",
            "succeeding_title": null,
            "title": "Acta Scientiarum. Agronomy",
            "title_iso": "Acta Sci., Agron",
            "twitter_user": null,
            "updated": "2014-04-04T10:31:37.996109",
            "url_journal": null,
            "url_online_submission": null,
            "use_license": {
              "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/deed.es\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> Todo el contenido de la revista, excepto d\u00c3\u00b3nde est\u00c3\u00a1 identificado, est\u00c3\u00a1 bajo una <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/deed.es\">Licencia Creative Commons</a>",
              "id": 3,
              "is_default": false,
              "license_code": "BY",
              "reference_url": null,
              "resource_uri": "/api/v2/uselicenses/3/"
            }
          },
        ]
    }

Get a single journal
--------------------

Request:

    **API version 1**

    *GET /api/v1/journals/:id/*

    **API version 2**

    *GET /api/v2/journals/:id/*

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

  **API version 2**::

    {
      "abstract_keyword_languages": null,
      "acronym": "AISS",
      "collections": [
        "Saude Publica"
      ],
      "contact": null,
      "copyrighter": "Istituto Superiore di Sanit\u00c3 ",
      "cover": null,
      "created": "2010-04-09T00:00:00",
      "creator": "/api/v2/users/1/",
      "ctrl_vocabulary": "nd",
      "current_ahead_documents": 0,
      "editor_address": "Viale Regina Elena 299, 00161 Italy Rome, Tel.: 0039 06 4990 2945, Fax: 0039 06 4990 2253",
      "editor_address_city": "",
      "editor_address_country": "",
      "editor_address_state": "",
      "editor_address_zip": "",
      "editor_email": "",
      "editor_name": "",
      "editor_phone1": "",
      "editor_phone2": null,
      "editorial_standard": "vancouv",
      "eletronic_issn": "",
      "final_num": "",
      "final_vol": "",
      "final_year": null,
      "frequency": "Q",
      "id": 1,
      "index_coverage": "chemabs\nembase\nmedline\npascal\nzoological records",
      "init_num": "1",
      "init_vol": "1",
      "init_year": "1965",
      "is_indexed_aehci": false,
      "is_indexed_scie": false,
      "is_indexed_ssci": false,
      "is_trashed": false,
      "issues": [
        "/api/v2/issues/1/",
        "/api/v2/issues/4/",
        "/api/v2/issues/5/",
        "/api/v2/issues/6/",
        "/api/v2/issues/7/",
        "/api/v2/issues/8/",
        "/api/v2/issues/9/",
        "/api/v2/issues/10/",
        "/api/v2/issues/11/",
        "/api/v2/issues/12/",
        "/api/v2/issues/2/",
        "/api/v2/issues/3/"
      ],
      "languages": [
        "en",
        "it"
      ],
      "logo": null,
      "medline_code": null,
      "medline_title": null,
      "missions": {
        "en": "To disseminate information on researches in public health."
      },
      "national_code": null,
      "notes": "",
      "other_previous_title": "",
      "other_titles": {

      },
      "previous_ahead_documents": 0,
      "previous_title": null,
      "print_issn": "0021-2571",
      "pub_level": "CT",
      "pub_status": {
        "Saude Publica": "current"
      },
      "pub_status_history": [
        {
          "date": "2014-04-23T10:30:32.478306",
          "status": "current"
        }
      ],
      "pub_status_reason": {
        "Saude Publica": ""
      },
      "publication_city": "Roma",
      "publisher_country": "IT",
      "publisher_name": "Istituto Superiore di Sanit\u00c3 ",
      "publisher_state": "",
      "resource_uri": "/api/v2/journals/1/",
      "scielo_issn": "print",
      "secs_code": "",
      "sections": [
        "/api/v2/sections/526/",
        "/api/v2/sections/527/",
        "/api/v2/sections/528/",
        "/api/v2/sections/529/",
        "/api/v2/sections/530/",
        "/api/v2/sections/531/",
        "/api/v2/sections/532/",
        "/api/v2/sections/533/",
        "/api/v2/sections/534/",
        "/api/v2/sections/535/",
        "/api/v2/sections/536/",
        "/api/v2/sections/537/",
        "/api/v2/sections/538/",
        "/api/v2/sections/539/",
        "/api/v2/sections/540/",
        "/api/v2/sections/541/"
      ],
      "short_title": "Ann. Ist. Super. Sanit\u00c3 ",
      "sponsors": [
        "/api/v2/sponsors/1/"
      ],
      "study_areas": [

      ],
      "subject_descriptors": "public health",
      "succeeding_title": null,
      "title": "Annali dell'Istituto Superiore di Sanit\u00c3 ",
      "title_iso": "Ann. Ist. Super. Sanit\u00c3 ",
      "twitter_user": null,
      "updated": "2014-04-03T15:07:53.455149",
      "url_journal": null,
      "url_online_submission": null,
      "use_license": {
        "disclaimer": "<a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\"><img alt=\"Creative Commons License\" style=\"border-width:0\" src=\"http://i.creativecommons.org/l/by/3.0/80x15.png\" /></a> All the contents of the journal, except where otherwise noted, is licensed under a <a rel=\"license\" href=\"http://creativecommons.org/licenses/by/3.0/\">Creative Commons Attribution License</a>",
        "id": 1,
        "is_default": true,
        "license_code": "",
        "reference_url": null,
        "resource_uri": "/api/v2/uselicenses/1/"
      }
    }

  **Example of version 2 with multiple collections**::

        {
          "abstract_keyword_languages": null,
          "acronym": "RSP",
          "collections": [
            "Saude Publica"
          ],
          "contact": null,
          "copyrighter": "Faculdade de Sa\u00c3\u00bade P\u00c3\u00bablica da Universidade de S\u00c3\u00a3o Paulo",
          "cover": null,
          "created": "1998-04-30T00:00:00",
          "creator": "/api/v2/users/1/",
          "ctrl_vocabulary": "decs",
          "current_ahead_documents": 0,
          "editor_address": "Avenida Dr. Arnaldo, 715, 01246-904 S\u00c3\u00a3o Paulo SP Brazil, Tel./Fax: +55 11 3068-0539",
          "editor_address_city": "",
          "editor_address_country": "",
          "editor_address_state": "",
          "editor_address_zip": "",
          "editor_email": "",
          "editor_name": "",
          "editor_phone1": "",
          "editor_phone2": null,
          "editorial_standard": "vancouv",
          "eletronic_issn": "",
          "final_num": "",
          "final_vol": "",
          "final_year": null,
          "frequency": "B",
          "id": 20,
          "index_coverage": "cab-health\nembase\npopline\nlilacs\nadsa\u00c3\u00bade\ndocpal\nabstracts on hygiene and communicable diseases\nabstracts on zooparasitology\nbiological abstracts\ncurrent contents/social & behavioral science\nentomology abstracts\nexcerpta medica\nindex medicus\nmicrobiology abstracts\nnutrition abstracts and reviews-seriesb\nreview medical veterinary entomology\nsafety science abstracts journal\nsocial science citation index\ntropical diseases bulletin\nveterinary bulletin\nvirology abstracts\nisi \npubmed",
          "init_num": "1",
          "init_vol": "1",
          "init_year": "1967",
          "is_indexed_aehci": false,
          "is_indexed_scie": false,
          "is_indexed_ssci": false,
          "is_trashed": false,
          "issues": [
            "/api/v2/issues/184/",
            "/api/v2/issues/186/",
            "/api/v2/issues/187/",
            "/api/v2/issues/188/",
          ],
          "languages": [
            "en",
            "pt",
            "es"
          ],
          "logo": null,
          "medline_code": null,
          "medline_title": null,
          "missions": {
            "en": "To publish and divulge scientific production on subjects of relevance to Public Health",
            "es": "Publicar y diseminar productos del trabajo cient\u00c3\u00adfico relevantes para la Salud P\u00c3\u00bablica",
            "pt": "Publicar e disseminar produtos do trabalho cient\u00c3\u00adfico que sejam relevantes para a Sa\u00c3\u00bade P\u00c3\u00bablica"
          },
          "national_code": "068227-6",
          "notes": "",
          "other_previous_title": "",
          "other_titles": {
            "other": "Rev Saude Publica",
            "paralleltitle": "Journal of Public Health"
          },
          "previous_ahead_documents": 0,
          "previous_title": null,
          "print_issn": "0034-8910",
          "pub_level": "CT",
          "pub_status": {
            "Saude Publica": "deceased"
          },
          "pub_status_history": [
            {
              "date": "2014-08-14T14:57:05.940893",
              "status": "deceased"
            },
            {
              "date": "2014-04-23T10:30:29.470427",
              "status": "current"
            }
          ],
          "pub_status_reason": {
            "Saude Publica": "teste"
          },
          "publication_city": "S\u00c3\u00a3o Paulo",
          "publisher_country": "BR",
          "publisher_name": "Faculdade de Sa\u00c3\u00bade P\u00c3\u00bablica da Universidade de S\u00c3\u00a3o Paulo",
          "publisher_state": "SP",
          "resource_uri": "/api/v2/journals/20/",
          "scielo_issn": "print",
          "secs_code": "",
          "sections": [
            "/api/v2/sections/44/",
            "/api/v2/sections/45/",
            "/api/v2/sections/46/",
            "/api/v2/sections/47/",
            "/api/v2/sections/48/",
            "/api/v2/sections/49/",
            "/api/v2/sections/50/",
            "/api/v2/sections/51/",
            "/api/v2/sections/52/",
            "/api/v2/sections/53/",
            "/api/v2/sections/54/",
            "/api/v2/sections/55/",
          ],
          "short_title": "Rev. Sa\u00c3\u00bade P\u00c3\u00bablica",
          "sponsors": [

          ],
          "study_areas": [

          ],
          "subject_descriptors": "saude coletiva\nsaude publica\nmicrobiologia",
          "succeeding_title": null,
          "title": "Revista de Sa\u00c3\u00bade P\u00c3\u00bablica",
          "title_iso": "Rev. sa\u00c3\u00bade p\u00c3\u00bablica",
          "twitter_user": null,
          "updated": "2014-04-03T15:08:35.586311",
          "url_journal": null,
          "url_online_submission": null,
          "use_license": {
            "disclaimer": "<p> </p>",
            "id": 4,
            "is_default": false,
            "license_code": "nd",
            "reference_url": null,
            "resource_uri": "/api/v2/uselicenses/4/"
          }
        }
