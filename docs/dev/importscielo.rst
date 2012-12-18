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

#. journal_

#. book_

#. confproc_

#. thesis_

#. software_

#. database_

#. webpage_

#. patent_

#. report_

#. newspaper_

**Publication-Type: Journal**

Tipos possíveis no atributo person-group-type da tag person-group:

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

Tipos possíveis no atributo pub-id-type da tag pub-id:

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

Tipos possíveis no atributo content-type da tag date-in-citation:

#. epub
#. updated
#. acess-date      
      
Campos comuns entre os tipos:

.. code-block:: xml

  <ref id="{id}">
    <label>{label}</label>
    <element-citation publication-type="">
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
      <person-group person-group-type="">
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
      <collab>{collab}</collab>
      <etal>{etal}</etal>
      <source>{source}</source>
      <year>{year}</year>
      <month>{month}</month>
      <season>{season}</season>
      <day>{day}</day>
      <fpage>{fpage}</fpage>
      <lpage>{lpage}</lpage>
      <issue>{issue}</issue>
      <page-range>{page-range}</page-range>
      <comment>{comment}</comment>
      <date-in-citation content-type="">{epub}</date-in-citation>
      <element-citation>{element-citation}</element-citation> 
      <comment>
            <uri>{uri}</uri>
            <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </comment>
      <pub-id pub-id-type="">{doi}</pub-id>
      <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </element-citation>
  </ref>

.. _journal:

Exemplo da estrutura do XML da referência tipo Journal:

.. code-block:: xml

  <ref id="{id}">
      <article-title>{article-title}</article-title>
      <publisher-loc>{publisher-loc}</publisher-loc>
      <volume>{volume}</volume>
      <issue-part>{issue-part}</issue-part>
      <supplement>{supplement}</supplement>
      <pub-id pub-id-type="">{pmid}</pub-id> 
  </ref>

.. _book:

Exemplo da estrutura do XML da referência tipo Book:

.. code-block:: xml

  <ref id="{id}">
      <person-group person-group-type="author">
        <aff>{aff}</aff>
        <anonymous>{annonymous}</anonymous>
      </person-group>
      <chapter-title>{chapter-title}</chapter-title>
      <trans-source>{trans-source}</trans-source>
      <publisher-loc>{publisher-loc}</publisher-loc>
      <publisher-name>{publisher}</publisher-name>
      <series>{series}</series>
      <size units="page">{size}</size>
      <isbn>{isbn}</isbn> 
  </ref>

.. _confproc:

Exemplo da estrutura do XML da referência tipo Confproc:

.. code-block:: xml

  <ref id="{id}">
      <article-title>{article-title}</article-title>
      <part-title>{part-title}</part-title>
      <conf-name>{conf-name}<conf-name/>
      <conf-date>{conf-date}</conf-date>
      <conf-loc>{conf-loc}</conf-loc>
      <trans-source>{trans-source}</trans-source>           
      <publisher-loc>{publisher-loc}</publisher-loc>
      <publisher-name>{publisher-name}</publisher-name>
      <series>{series}</series>
      <size units="page">{size}</size>
      <isbn>{isbn}</isbn> 
  </ref>

.. _thesis:

Exemplo da estrutura do XML da referência tipo Thesis:

.. code-block:: xml

   <ref id="{id}">
      <person-group person-group-type="author">
        <aff>{aff}</aff>
        <anonymous>{anonymous}</anonymous>
      </person-group>
      <chapter-title>{chapter-title}</chapter-title>
      <trans-source>{trans-source}</trans-source>
      <part-title>{part-title}</part-title>
      <publisher-loc>{publisher-loc}</publisher-loc>
      <publisher-name>{publisher-name}</publisher-name>
      <series>{series}</series>
      <size units="page"/>
      <isbn>{isbn}</isbn>
      <pub-id pub-id-type="">{pmid}</pub-id>
  </ref>

.. _software:

Exemplo da estrutura do XML da referência tipo Software:

.. code-block:: xml

  <ref id="{id}">
      <element-citation publication-type="">
          <edition>{edition}}</edition>
          <publisher-loc>{publisher-loc}</publisher-loc>
          <publisher-name>{publisher-name}</publisher-name>
          <year>{year}</year>
      </element-citation>
  </ref>

.. _database:

.. code-block:: xml

  Todos as tags utilizadas nesse tipo estão no XML comun. 

.. _webpage:

.. code-block:: xml

  Todos as tags utilizadas nesse tipo estão no XML comun. 

.. _patent:

  Exemplo da estrutura do XML da referência tipo Webpage:

.. code-block:: xml

  <ref id="{id}">
    <element-citation publication-type="">
        <patent country="{country}">{country}</patent>
    </element-citation>
  </ref>

.. _report:

  Exemplo da estrutura do XML da referência tipo Report:

.. code-block:: xml

  <ref id="{id}">
    <element-citation publication-type="">
        <chapter-title>{chapter}</chapter-title>
        <series>{source}</series>
        <publisher-loc>{publisher-loc}</publisher-loc>
        <publisher-name>{publisher-name}</publisher-name>
    </element-citation>
  </ref>

.. _newspaper:

  Exemplo da estrutura do XML da referência tipo Newspaper:
  
.. code-block:: xml

  <ref id="{id}">
    <element-citation publication-type="">
        <series>{series}</series>
        <article-title>{article-title}</article-title>
        <publisher-loc>{publisher-loc}}</publisher-loc>
        <publisher-name>{publisher-name}</publisher-name>
    </element-citation>
  </ref>

Documento com os campos que são utilizados na bibliometria:

Enviado em 18/12/2012 por Rogério Mugnaini: `Bibliometria Campos
<https://github.com/scieloorg/SciELO-Manager/raw/master/docs/_static/campos_usados_bibliometria.doc>`_.
