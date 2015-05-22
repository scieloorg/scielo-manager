<?xml version="1.0" encoding="utf-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="xslt"
        xml:lang="en">
    
    <phase id="phase.root-elements">
        <active pattern="root-elements"/>
    </phase>

    <phase id="phase.journal-meta-elements">
        <active pattern="journal-meta"/>
    </phase>

    <phase id="phase.article-meta-elements">
        <active pattern="article-meta"/>
    </phase>


    <pattern id="root-elements">
        <rule context="/">
            <assert test="article/front/journal-meta">
                Missing element article/front/journal-meta.
            </assert>
            <assert test="article/front/article-meta">
                Missing element article/front/article-meta.
            </assert>
        </rule>
    </pattern>

    <pattern id="journal-meta">
        <rule context="article/front/journal-meta">
            <assert test="journal-title-group/abbrev-journal-title[@abbrev-type='publisher']">
                Missing element abbrev-journal-title[@abbrev-type='publisher'].
            </assert>
        </rule>
    </pattern>

    <pattern id="article-meta">
        <rule context="article/front/article-meta">
            <assert test="volume">
                Missing element volume.
            </assert>
            <assert test="issue">
                Missing element issue.
            </assert>
            <assert test="pub-date/year">
                Missing element year.
            </assert>
            <assert test="title-group/article-title">
                Missing element article-title.
            </assert>
            <assert test="count(contrib-group/contrib[@contrib-type='author' or 
                                                      @contrib-type='compiler' or 
                                                      @contrib-type='editor' or 
                                                      @contrib-type='translator']/name/surname) > 0">
                Missing element contrib/name/surname.
            </assert>
        </rule>
    </pattern>

</schema>
