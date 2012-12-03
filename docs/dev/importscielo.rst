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
      
Campos comuns entre os tipos:

.. code-block:: xml

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
      <date-in-citation content-type="epub">{epub}</date-in-citation>
      <element-citation>{element-citation}</element-citation> 
      <comment>
            <uri>{uri}</uri>
            <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
      </comment>
      <pub-id pub-id-type="doi">{doi}</pub-id>
      <ext-link ext-link-type="uri" xlink:href="{url_value}">{url}</ext-link>
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
      <pub-id pub-id-type="pmid">{pmid}</pub-id> 
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
      <pub-id pub-id-type="pmid">{pmid}</pub-id>
  </ref>
