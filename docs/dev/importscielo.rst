SciELO Importação XML
=====================

DTD Pubmed Central Version3: http://dtd.nlm.nih.gov/publishing/tag-library/3.0/n-qdc2.html.

Front
-----
Body
----
Back
----

Tag: <ref>

Tipos possíveis no atributo Publication-Type:

#. journal_.

#. book_.

#. confproc_.

#. thesis_.

#. software

#. database

#. webpage

#. patent

#. report

#. newspaper

**Publication-Type: Journal**

Tipos possíveis no atributo Person-Group-Type:

#. allauthors

#. assignee

#. author

#. compiler

#. director

#. editor

#. guest-editor

#. inventor

#. transed

#. translator 

Tipos possíveis no atributo pub-id-type:

#. art-access-id

#. coden

#. doaj

#. doi

#. manuscript

#. other

#. pii

#. pmcid

#. pmid

#. publisher-id

#. sici          

Tipos possíveis no atributo content-type:

#. epub
#. updated
#. acess-date      
      
.. _journal:

Exemplo da estrutura do XML da referência tipo Journal:

.. code-block:: text

  <ref id="{id}">
    <label>{label}</label>
    <element-citation publication-type="journal">
      <name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </name>
      <string-name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </string-name>
      <collab>{collab}</collab>
      <person-group person-group-type="author">
        <name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
        </name>
        <string-name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
          <suffix>{suffix}</suffix>
          <prefix>{prefix}</prefix>
        </string-name>
        <collab>{collab}</collab>
        <etal/>
      </person-group>
      <etal/>
      <article-title>{article-title}</article-title>
      <source>{source}</source>
      <publisher-loc>{publisher-loc}</publisher-loc>
      <year>{year}</year>
      <month>{month}</month>
      <season>{season}</season>
      <day>{day}</day>
      <volume>{volume}</volume>
      <issue>{issue}</issue>
      <issue-part>{issue-part}</issue-part>
      <edition>{edition}</edition>
      <supplement>{supplement}</supplement>            
      <fpage>{fpage}</fpage>
      <lpage>{lpage}</lpage>
      <page-range>{page-range}</page-range>
      <comment>{comment}</comment>
      <comment>
            <uri>{uri}</uri>
            <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </comment>
      <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      <pub-id pub-id-type="doi">{doi}</pub-id>
      <pub-id pub-id-type="pmid">{pmid}</pub-id>            
      <date-in-citation content-type="epub">{epub}</date-in-citation>           
    </element-citation> 
  </ref>

Exemplo da estrutura JSON do ref tipo Journal:

.. code-block:: text

  {
    "ref": {
      "@id": "{id}", 
      "label": "{label}", 
      "element-citation": {
        "@publication-type": "journal", 
        "name": {
          "surname": "{surname}", 
          "given-names": "{given-names}", 
          "suffix": "{suffix}", 
          "prefix": "{prefix}"
        }, 
        "string-name": {
          "surname": "{surname}", 
          "given-names": "{given-names}", 
          "suffix": "{suffix}", 
          "prefix": "{prefix}"
        }, 
        "collab": "{collab}", 
        "person-group": {
          "@person-group-type": "author", 
          "name": {
            "surname": "{surname}", 
            "given-names": "{given-names}"
          }, 
          "string-name": {
            "surname": "{surname}", 
            "given-names": "{given-names}", 
            "suffix": "{suffix}", 
            "prefix": "{prefix}"
          }, 
          "collab": "{collab}", 
          "etal": null
        }, 
        "etal": null, 
        "article-title": "{article-title}", 
        "source": "{source}", 
        "publisher-loc": "{publisher-loc}", 
        "year": "{year}", 
        "month": "{month}", 
        "season": "{season}", 
        "day": "{day}", 
        "volume": "{volume}", 
        "issue": "{issue}", 
        "issue-part": "{issue-part}", 
        "edition": "{edition}", 
        "supplement": "{supplement}", 
        "fpage": "{fpage}", 
        "lpage": "{lpage}", 
        "page-range": "{page-range}", 
        "comment": [
          "{comment}", 
          {
            "uri": "{uri}", 
            "ext-link": "{url}"
          }
        ], 
        "ext-link": "{url}", 
        "pub-id": [
          {
            "@pub-id-type": "doi", 
            "#text": "{doi}"
          }, 
          {
            "@pub-id-type": "pmid", 
            "#text": "{pmid}"
          }
        ], 
        "date-in-citation": {
          "@content-type": "epub", 
          "#text": "{epub}"
        }
      }
    }
  }

.. _book:

Exemplo da estrutura do XML da referência tipo Book:

.. code-block:: text

  <ref id="{id}">
     <label>{label}</label>
     <element-citation publication-type="book">
          <name>
              <surname>{surname}</surname>
              <given-names>{given-names}</given-names>
              <suffix>{suffix}</suffix>
              <prefix>{prefix}</prefix>
          </name>
          <string-name>
              <surname>{surname}</surname>
              <given-names>{given-names}</given-names>
              <suffix>{suffix}</suffix>
              <prefix>{prefix}</prefix>
          </string-name>
          <collab>{collab}</collab>
          <person-group person-group-type="author">
              <name>
                  <surname>{surname}</surname>
                  <given-names>{given-names}</given-names>
              </name>
              <string-name>
                  <surname>{surname}</surname>
                  <given-names>{given-names}</given-names>
                  <suffix>{suffix}</suffix>
                  <prefix>{prefix}</prefix>
              </string-name>
              <aff>{aff}</aff>
              <anonymous>{annonymous}</anonymous>
              <collab>{collab}</collab>
              <etal>{etal}</etal>
          </person-group>
          <etal>{etal}</etal>
          <chapter-title>{chapter-title}</chapter-title>
          <source>{source}</source>
          <trans-source>{trans-source}</trans-source>
          <edition>{edition}</edition>
          <publisher-loc>{publisher-loc}</publisher-loc>
          <publisher-name>{publisher}</publisher-name>
          <year>{year}</year>
          <month>{month}</month>
          <season>{season}</season>
          <day>{day}</day>
          <date-in-citation>{date-in-citation}</date-in-citation>
          <series>{series}</series>
          <size units="page">{size}</size>
          <fpage>{fpage}</fpage>
          <lpage>{lpage}</lpage>
          <page-range>{page-range}</page-range>
          <isbn>{isbn}</isbn>                
          <comment>{comment}</comment>          
          <comment>
              <uri>{uri}</uri>
              <ext-link>{uri}</ext-link>
          </comment>
          <ext-link>{uri}</ext-link>
          <pub-id pub-id-type="doi">{doi}</pub-id>      
      </element-citation>  
  </ref>

Exemplo da estrutura JSON do ref tipo Book:

.. code-block:: text

  {
      "ref": {
          "@id": "{id}", 
          "label": "{label}", 
          "element-citation": {
              "@publication-type": "book", 
              "name": {
                  "surname": "{surname}", 
                  "given-names": "{given-names}", 
                  "suffix": "{suffix}", 
                  "prefix": "{prefix}"
              }, 
              "string-name": {
                  "surname": "{surname}", 
                  "given-names": "{given-names}", 
                  "suffix": "{suffix}", 
                  "prefix": "{prefix}"
              }, 
              "collab": "{collab}", 
              "person-group": {
                  "@person-group-type": "author", 
                  "name": {
                      "surname": "{surname}", 
                      "given-names": "{given-names}"
                  }, 
                  "string-name": {
                      "surname": "{surname}", 
                      "given-names": "{given-names}", 
                      "suffix": "{suffix}", 
                      "prefix": "{prefix}"
                  }, 
                  "aff": "{aff}", 
                  "anonymous": "{annonymous}", 
                  "collab": "{collab}", 
                  "etal": "{etal}"
              }, 
              "etal": "{etal}", 
              "chapter-title": "{chapter-title}", 
              "source": "{source}", 
              "trans-source": "{trans-source}", 
              "edition": "{edition}", 
              "publisher-loc": "{publisher-loc}", 
              "publisher-name": "{publisher}", 
              "year": "{year}", 
              "month": "{month}", 
              "season": "{season}", 
              "day": "{day}", 
              "date-in-citation": "{date-in-citation}", 
              "series": "{series}", 
              "size": {
                  "@units": "page", 
                  "#text": "{size}"
              }, 
              "fpage": "{fpage}", 
              "lpage": "{lpage}", 
              "page-range": "{page-range}", 
              "isbn": "{isbn}", 
              "comment": [
                  "{comment}", 
                  {
                      "uri": "{uri}", 
                      "ext-link": "{uri}"
                  }
              ], 
              "ext-link": "{uri}", 
              "pub-id": {
                  "@pub-id-type": "doi", 
                  "#text": "{doi}"
              }
          }
      }
  }


.. _confproc:

Exemplo da estrutura do XML da referência tipo Confproc:

.. code-block:: text

  <ref id="{id}">
    <label>{label}</label>
    <element-citation publication-type="confproc">
      <name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </name>
      <string-name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </string-name>
      <collab>{collab}</collab>
      <person-group person-group-type="author">
        <name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
        </name>
        <string-name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
          <suffix>{suffix}</suffix>
          <prefix>{prefix}</prefix>
        </string-name>
        <collab>{collab}</collab>
        <etal>{etal}<etal>
      </person-group>
      <etal>{etal}</etal>
      <article-title>{article-title}</article-title>
      <source>{source}</source>
      <part-title>{part-title}</part-title>
      <conf-name>{conf-name}<conf-name/>
      <conf-date>{conf-date}</conf-date>
      <conf-loc>{conf-loc}</conf-loc>
      <trans-source>{trans-source}</trans-source>
      <edition>{edition}</edition>           
      <publisher-loc>{publisher-loc}</publisher-loc>
      <publisher-name>{publisher-name}</publisher-name>
      <year>{year}</year>
      <month>{month}</month>
      <season>{season}</season>
      <day>{day}</day>
      <series>{series}</series>
      <size units="page">{size}</size>
      <fpage>{fpage}</fpage>
      <lpage>{lpage}</lpage>
      <page-range>{page-range}</page-range>
      <isbn>{isbn}</isbn>
      <comment>{comment}</comment>
      <comment>
            <uri>{uri}</uri>
            <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </comment>
      <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      <pub-id pub-id-type="doi">{doi}</pub-id>           
      <date-in-citation content-type="epub">{epub}</date-in-citation>           
    </element-citation> 
  </ref>

Exemplo da estrutura JSON do ref tipo Confproc:

.. code-block:: text

  {
    "ref": {
        "@id": "{id}", 
        "label": "{label}", 
        "element-citation": {
            "@publication-type": "confproc", 
            "name": {
                "surname": "{surname}", 
                "given-names": "{given-names}", 
                "suffix": "{suffix}", 
                "prefix": "{prefix}"
            }, 
            "string-name": {
                "surname": "{surname}", 
                "given-names": "{given-names}", 
                "suffix": "{suffix}", 
                "prefix": "{prefix}"
            }, 
            "collab": "{collab}", 
            "person-group": {
                "@person-group-type": "author", 
                "name": {
                    "surname": "{surname}", 
                    "given-names": "{given-names}"
                }, 
                "string-name": {
                    "surname": "{surname}", 
                    "given-names": "{given-names}", 
                    "suffix": "{suffix}", 
                    "prefix": "{prefix}"
                }, 
                "collab": "{collab}", 
                "etal": "{etal}"
            }, 
            "etal": "{etal}", 
            "article-title": "{article-title}", 
            "source": "{source}", 
            "part-title": "{part-title}", 
            "conf-name": "{conf-name}", 
            "conf-date": "{conf-date}", 
            "conf-loc": "{conf-loc}", 
            "trans-source": "{trans-source}", 
            "edition": "{edition}", 
            "publisher-loc": "{publisher-loc}", 
            "publisher-name": "{publisher-name}", 
            "year": "{year}", 
            "month": "{month}", 
            "season": "{season}", 
            "day": "{day}", 
            "series": "{series}", 
            "size": {
                "@units": "page", 
                "#text": "{size}"
            }, 
            "fpage": "{fpage}", 
            "lpage": "{lpage}", 
            "page-range": "{page-range}", 
            "isbn": "{isbn}", 
            "comment": [
                "{comment}", 
                {
                    "uri": "{uri}", 
                    "ext-link": "{url}"
                }
            ], 
            "ext-link": "{url}", 
            "pub-id": {
                "@pub-id-type": "doi", 
                "#text": "{doi}"
            }, 
            "date-in-citation": {
                "@content-type": "epub", 
                "#text": "{epub}"
            }
        }
    }
  }

.. _thesis:

Exemplo da estrutura do XML da referência tipo Thesis:

.. code-block:: text

   <ref id="{id}">
    <label>{label}</label>
    <element-citation publication-type="thesis">
      <name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </name>
      <string-name>
        <surname>{surname}</surname>
        <given-names>{given-names}</given-names>
        <suffix>{suffix}</suffix>
        <prefix>{prefix}</prefix>
      </string-name>
      <collab>{collab}</collab>
      <person-group person-group-type="author">
        <name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
        </name>
        <string-name>
          <surname>{surname}</surname>
          <given-names>{given-names}</given-names>
          <suffix>{suffix}</suffix>
          <prefix>{prefix}</prefix>
        </string-name>
        <collab>{collab}</collab>
        <etal/>
        <aff/>
        <anonymous/>
      </person-group>
      <etal/>
      <chapter-title/>
      <source>{source}</source>
      <trans-source/>
      <part-title/>
      <edition>{edition}</edition>
      <publisher-loc>{publisher-loc}</publisher-loc>
      <publisher-name/>
      <year>{year}</year>
      <month>{month}</month>
      <season>{season}</season>
      <day>{day}</day>           
      <date-in-citation/>
      <series/>
      <size units="page"/>    
      <fpage>{fpage}</fpage>
      <lpage>{lpage}</lpage>
      <page-range>{page-range}</page-range>
      <isbn/>
      <comment>{comment}</comment>
      <comment>
            <uri>{uri}</uri>
            <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </comment>
      <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>

      <pub-id pub-id-type="pmid">{pmid}</pub-id>            
      <pub-id pub-id-type="doi">{doi}</pub-id>
    </element-citation> 
  </ref>

Exemplo da estrutura JSON do ref tipo Thesis:

.. code-block:: text

  {
    "ref": {
        "@id": "{id}", 
        "label": "{label}", 
        "element-citation": {
            "@publication-type": "thesis", 
            "name": {
                "surname": "{surname}", 
                "given-names": "{given-names}", 
                "suffix": "{suffix}", 
                "prefix": "{prefix}"
            }, 
            "string-name": {
                "surname": "{surname}", 
                "given-names": "{given-names}", 
                "suffix": "{suffix}", 
                "prefix": "{prefix}"
            }, 
            "collab": "{collab}", 
            "person-group": {
                "@person-group-type": "author", 
                "name": {
                    "surname": "{surname}", 
                    "given-names": "{given-names}"
                }, 
                "string-name": {
                    "surname": "{surname}", 
                    "given-names": "{given-names}", 
                    "suffix": "{suffix}", 
                    "prefix": "{prefix}"
                }, 
                "collab": "{collab}", 
                "etal": null, 
                "aff": null, 
                "anonymous": null
            }, 
            "etal": null, 
            "chapter-title": null, 
            "source": "{source}", 
            "trans-source": null, 
            "part-title": null, 
            "edition": "{edition}", 
            "publisher-loc": "{publisher-loc}", 
            "publisher-name": null, 
            "year": "{year}", 
            "month": "{month}", 
            "season": "{season}", 
            "day": "{day}", 
            "date-in-citation": null, 
            "series": null, 
            "size": {
                "@units": "page"
            }, 
            "fpage": "{fpage}", 
            "lpage": "{lpage}", 
            "page-range": "{page-range}", 
            "isbn": null, 
            "comment": [
                "{comment}", 
                {
                    "uri": "{uri}", 
                    "ext-link": {
                        "@ext-link-type": "uri", 
                        "#text": "{url}"
                    }
                }
            ], 
            "ext-link": {
                "@ext-link-type": "uri", 
                "#text": "{url}"
            }, 
            "pub-id": [
                {
                    "@pub-id-type": "pmid", 
                    "#text": "{pmid}"
                }, 
                {
                    "@pub-id-type": "doi", 
                    "#text": "{doi}"
                }
            ]
        }
    }
  }
