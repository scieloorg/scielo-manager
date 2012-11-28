SciELO Importação XML
=====================

Front
-----
Body
----
Back
----

Tag: <ref>

Tipos possíveis no atributo Publication-Type:

#. journal_.

#. book

#. confproc

#. thesis

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

Exemplo:

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


