<?xml version="1.0" encoding="utf-8"?>
<schema xmlns="http://purl.oclc.org/dsdl/schematron"
        queryBinding="xslt"
        xml:lang="en">
    
    <phase id="phase.root-elements">
        <active pattern="root-elements"/>
    </phase>

    <phase id="phase.journal-meta-elements">
        <active pattern="journal-meta_journal-title"/>
        <active pattern="journal-meta_issn"/>
    </phase>

    <phase id="phase.article-meta-elements">
        <active pattern="article-meta"/>
        <active pattern="article-meta_volume"/>
        <active pattern="article-meta_issue"/>
        <active pattern="article-meta_year"/>
    </phase>

    <pattern id="is_present_and_not_empty" abstract="true">
        <title>
            Pattern abstrato que verifica se determinado elemento existe e possui
            qualquer conteúdo.
        </title>
        <rule context="$base_context">
            <assert test="$assert_expr and (string-length(normalize-space($assert_expr)) != 0)">
                Error at '<name/>'.
            </assert>
        </rule>
    </pattern>

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

    <pattern id="journal-meta_journal-title" is-a="is_present_and_not_empty">
        <param name="base_context" value="article/front/journal-meta"/>
        <param name="assert_expr" value="journal-title-group/journal-title"/>
    </pattern>

    <pattern id="journal-meta_issn" is-a="is_present_and_not_empty">
        <param name="base_context" value="article/front/journal-meta"/>
        <param name="assert_expr" value="issn[@pub-type='epub' or @pub-type='ppub']"/>
    </pattern>

    <pattern id="article-meta_volume" is-a="is_present_and_not_empty">
        <param name="base_context" value="article/front/article-meta"/>
        <param name="assert_expr" value="volume"/>
    </pattern>

    <pattern id="article-meta_issue" is-a="is_present_and_not_empty">
        <param name="base_context" value="article/front/article-meta"/>
        <param name="assert_expr" value="issue"/>
    </pattern>

    <pattern id="article-meta_year" is-a="is_present_and_not_empty">
        <param name="base_context" value="article/front/article-meta"/>
        <param name="assert_expr" value="pub-date/year"/>
    </pattern>

    <pattern id="article-meta">
        <title>
            A paginação é única entre artigos de um mesmo fascículo, portanto
            funciona como chave primária candidata.
        </title>

        <rule context="article/front/article-meta">
            <assert test="(fpage and lpage) or elocation-id">
                Missing elements (fpage and lpage) or elocation-id.
            </assert>
        </rule>
    </pattern>

</schema>
