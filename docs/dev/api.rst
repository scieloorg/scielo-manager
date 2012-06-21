=============================================================
Journal Manager API
=============================================================

API to allow access to Journals, Issues and collections data.

**Current version:** API v1

Get Collections List
====================

Request::

  GET /api/v1/collections

Parameters:

  **parameters not necessary**

Optional Parameters:

  **callback**
    
    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/collections?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/collections?format=xml

Response Example::

  [
      {
          "city": "São paulo", 
          "fax": "", 
          "name": "Brasil", 
          "address_number": "430", 
          "phone": "", 
          "url": "http://www.scielo.br/", 
          "country": "Brasil", 
          "acronym": "scl", 
          "state": "São Paulo", 
          "address": "Rua Machado Bittencourt", 
          "mail": "scielo@scielo.org", 
          "zip_code": "", 
          "address_complement": ""
      }, 
      {
          "city": "San Tiago", 
          "fax": "", 
          "name": "Chile", 
          "address_number": "123", 
          "phone": "", 
          "url": "http://www.scielo.sld.cu/", 
          "country": "Chile", 
          "acronym": "chl", 
          "state": "San Tiago", 
          "address": "Rua ", 
          "mail": "scielo@scielo.cl", 
          "zip_code": "", 
          "address_complement": ""
      }
  ]

Get a Collection Metadata
=========================

Request::

  GET /api/v1/collections/:<collection_name_slug>

Parameters:

  **collection_name_slug**

    *String* of the name of a collection, for example: brasil, chile, cuba. If you doesn't know the 
    available collections you can fetch it with the "Get Collections List"

Optional Parameters:

  **callback**
    
    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/collections/brasil/?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/collections/brasil/?format=xml

Response Example::

  {
      "city": "São paulo", 
      "fax": "", 
      "name": "Brasil", 
      "address_number": "430", 
      "phone": "", 
      "url": "http://www.scielo.br/", 
      "country": "Brasil", 
      "acronym": "scl", 
      "state": "São Paulo", 
      "address": "Rua Machado Bittencourt", 
      "mail": "scielo@scielo.org", 
      "zip_code": "", 
      "address_complement": ""
  }

Get Journals List
=================

Request::

  GET /api/v1/journals/:<collection_name_slug>

Parameters:

  **collection_name_slug**

    *String* of the name of a collection, for example: brasil, chile, cuba. If you doesn't know the 
    available collections you can fetch it with the "Get Collections List"

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/brasil?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/brasil?format=xml

Response Example::

  [
    {
        "copyrighter": "", 
        "ctrl_vocabulary": "decs", 
        "frequency": "Q", 
        "url_journal": null, 
        "sponsor": [
            {
                "name": "Colégio Brasileiro de Cirurgia Digestiva - CBCD"
            }
        ], 
        "final_num": "", 
        "eletronic_issn": "", 
        "url_online_submission": null, 
        "init_vol": "1", 
        "title": "ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)", 
        "final_year": null, 
        "editorial_standard": "vancouv", 
        "languages": [
            {
                "iso_code": "en"
            }, 
            {
                "iso_code": "pt"
            }
        ], 
        "scielo_issn": "print", 
        "collections": [
            {
                "city": "São paulo", 
                "fax": "", 
                "name": "Brasil", 
                "address_number": "430", 
                "phone": "", 
                "url": "http://www.scielo.br/", 
                "country": "Brasil", 
                "acronym": "scl", 
                "state": "São Paulo", 
                "name_slug": "brasil", 
                "address": "Rua Machado Bittencourt", 
                "mail": "scielo@scielo.org", 
                "zip_code": "", 
                "address_complement": ""
            }
        ], 
        "secs_code": "6633", 
        "use_license": {
            "disclaimer": null, 
            "license_code": "###PLACEBO###"
        }, 
        "index_coverage": "ll - lilacs", 
        "previous_title": null, 
        "acronym": "ABCD", 
        "init_year": "1986", 
        "other_previous_title": "", 
        "init_num": "1", 
        "publisher": [
            {
                "name": "Colégio Brasileiro de Cirurgia Digestiva"
            }
        ], 
        "pub_level": "CT", 
        "final_vol": "", 
        "cover": "", 
        "short_title": "ABCD, arq. bras. cir. dig.", 
        "subject_descriptors": "medicina\ncirurgia\ngastroenterologia\ngastroenterologia", 
        "pub_status": "current", 
        "title_iso": "", 
        "print_issn": "0102-6720"
    }, 
    {
        "copyrighter": "", 
        "ctrl_vocabulary": "nd", 
        "frequency": "F", 
        "url_journal": null, 
        "sponsor": [], 
        "final_num": "", 
        "eletronic_issn": "", 
        "url_online_submission": null, 
        "init_vol": "", 
        "title": "ARS (São Paulo)", 
        "final_year": null, 
        "editorial_standard": "nbr6023", 
        "languages": [
            {
                "iso_code": "pt"
            }
        ], 
        "scielo_issn": "print", 
        "collections": [
            {
                "city": "São paulo", 
                "fax": "", 
                "name": "Brasil", 
                "address_number": "430", 
                "phone": "", 
                "url": "http://www.scielo.br/", 
                "country": "Brasil", 
                "acronym": "scl", 
                "state": "São Paulo", 
                "name_slug": "brasil", 
                "address": "Rua Machado Bittencourt", 
                "mail": "scielo@scielo.org", 
                "zip_code": "", 
                "address_complement": ""
            }
        ], 
        "secs_code": "", 
        "use_license": {
            "disclaimer": null, 
            "license_code": "###PLACEBO###"
        }, 
        "index_coverage": null, 
        "previous_title": null, 
        "acronym": "ARS", 
        "init_year": "20030100", 
        "other_previous_title": "", 
        "init_num": "", 
        "publisher": [
            {
                "name": "Escola de Comunicações e Artes da Universidade de São Paulo"
            }
        ], 
        "pub_level": "CT", 
        "final_vol": "", 
        "cover": "", 
        "short_title": "ARS (São Paulo)", 
        "subject_descriptors": "artes plásticas\neducação artística\nhistória da arte\nteoria da arte\nfotografia", 
        "pub_status": "current", 
        "title_iso": "", 
        "print_issn": "1678-5320"
    },
  ...
  ]

Get a Journal Metadata
======================

Request::

  GET /api/v1/journal/:<journal_issn>

Parameters:

  **issn**

    *String* of the ISSN. The ISSN could be the print or electronic ISSN.

Optional Parameters:

  **callback**

    *String* of the callback identifier to be returned when
    using JSONP.

  **format**

    *String* of the desired output format. The options are **xml, json, yml**. The default format is JSON.

Request Example::

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/0102-6720?callback=test

  $ curl -X GET journalmanager.scielo.org/api/v1/journals/0102-6720?format=xml

Response Example::

  {
    "copyrighter": "", 
    "ctrl_vocabulary": "decs", 
    "frequency": "Q", 
    "url_journal": null, 
    "sponsor": [
        {
            "name": "Colégio Brasileiro de Cirurgia Digestiva - CBCD"
        }
    ], 
    "final_num": "", 
    "eletronic_issn": "", 
    "url_online_submission": null, 
    "init_vol": "1", 
    "title": "ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)", 
    "final_year": null, 
    "editorial_standard": "vancouv", 
    "languages": [
        {
            "iso_code": "en"
        }, 
        {
            "iso_code": "pt"
        }
    ], 
    "scielo_issn": "print", 
    "collections": [
        {
            "name": "Brasil"
        }
    ], 
    "secs_code": "6633", 
    "use_license": {
        "disclaimer": null, 
        "license_code": "###PLACEBO###"
    }, 
    "index_coverage": "ll - lilacs", 
    "previous_title": null, 
    "acronym": "ABCD", 
    "init_year": "1986", 
    "other_previous_title": "", 
    "init_num": "1", 
    "publisher": [
        {
            "name": "Colégio Brasileiro de Cirurgia Digestiva"
        }
    ], 
    "pub_level": "CT", 
    "final_vol": "", 
    "cover": "", 
    "short_title": "ABCD, arq. bras. cir. dig.", 
    "subject_descriptors": "medicina\ncirurgia\ngastroenterologia\ngastroenterologia", 
    "pub_status": "current", 
    "title_iso": "", 
    "print_issn": "0102-6720"
  }

Get Journal Issues List
=========================

Request:

Parameters:

Optional Parameters:

Request Example:

Response Example:

Get a Journal Issue
====================

Request:

Parameters:

Optional Parameters:

Request Example:

Response Example: