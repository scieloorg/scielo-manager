===============================
Data Model (samples) JSON / XML
===============================

Sample with xpath
=================

.. code-block:: javascript

    {
        'front': {
            'journal-title': '/front/journal-meta/journal-title-group/journal-title',
            'abbrev-journal-title': '/front/journal-meta/journal-title-group/abbrev-journal-title',
            'issn': '/articles/article/front/journal-meta/issn',
            'publisher-name': '/articles/article/front/journal-meta/publisher/publisher-name',
            'publisher-loc': '/articles/article/front/journal-meta/publisher/publisher-loc',
            'journal-id': '/front/journal-meta/journal-id',
            'default-language': '/articles/article/@xml:lang',
            'pub-date': {
                'month': '/articles/article/front/article-meta/pub-date/month',
                'year': '/articles/article/front/article-meta/pub-date/year',
                'day': '/articles/article/front/article-meta/pub-date/day'
            },
            'volume': '/articles/article/front/article-meta/volume',
            'number': '/articles/article/front/article-meta/issue',
            'fpage': '/articles/article/front/article-meta/fpage',
            'lpage': '/articles/article/front/article-meta/lpage',
            'article-ids': {
                'publisher-id': '/articles/article/front/article-meta/article-id[@pub-id-type="publisher-id"]',
                'doi': '/articles/article/front/article-meta/article-id[@pub-id-type="doi"]'
            },
            'subjects': {
                'wos': [
                    '/articles/article/front/article-meta/article-categories/subj-group[0]',
                    '/articles/article/front/article-meta/article-categories/subj-group[0]'
                ],
                'cnpq': ['public health']
            },
            'title-group': {
                '/articles/article/front/article-meta/title-group/article-title/@xml:lang': '/articles/article/front/article-meta/title-group/article-title',
                '/articles/article/front/article-meta/title-group/trans-title-group/@xml:lang': '/articles/article/front/article-meta/title-group/trans-title-group',
            },
            'contrib-group': {
                '/articles/article/front/article-meta/contrib-group/contrib/@contrib-type': [
                    {
                    'surname': '/articles/article/front/article-meta/contrib-group/contrib/name/surname',
                    'given-names': '/articles/article/front/article-meta/contrib-group/contrib/name/given-names',
                    'role': '/articles/article/front/article-meta/contrib-group/contrib/role',
                    'affiliations': '/articles/article/front/article-meta/contrib-group/contrib/xref'
                    },
                ],
                'affiliations': [
                    {
                    'addr-line': '/articles/article/front/article-meta/aff/addr-line',
                    'institution': '/articles/article/front/article-meta/aff/institution',
                    'country': '/articles/article/front/article-meta/aff/country',
                    'ref': '/articles/article/front/article-meta/aff/@id',
                    },
                ],
                'abstract': {
                    '/articles/article/front/article-meta/abstract/@xml:lang': '/articles/article/front/article-meta/abstract',
                    '/articles/article/front/article-meta/trans-abstract@xml:lang': '/articles/article/front/article-meta/trans-abstract',
                },
                'keyword-group': {
                    '/articles/article/front/article-meta/kwd-group/@xml"lang': [
                        '/articles/article/front/article-meta/kwd-group/kwd[0]', 
                        '/articles/article/front/article-meta/kwd-group/kwd[1]',
                        '/articles/article/front/article-meta/kwd-group/kwd[2]'
                    ],
                    '/articles/article/front/article-meta/kwd-group/@xml"lang': [
                        '/articles/article/front/article-meta/kwd-group/kwd[0]', 
                        '/articles/article/front/article-meta/kwd-group/kwd[1]',
                        '/articles/article/front/article-meta/kwd-group/kwd[2]'
                    ]
                }
            },

        },
        'body': u'<p>All body content</p>',
        'back': [
            {
                'article-title': u'Alternatives for logistic regression in cross-sectional studies: an empirical comparison of models that directly estimate the prevalence ratio',
                'type': u'journal'
            }
        ]
    }

Sample with data
================

.. code-block:: javascript

    {
        'front': {
            'journal-title': u'Revista de Saúde Pública',
            'abbrev-journal-title': u'Rev. Saúde Pública',
            'issn': '0034-8910',
            'publisher-name': u'Faculdade de Saúde pública da Universidade de São Paulo',
            'publisher-loc': u'São Paulo',
            'journal-id': u'rsp',
            'default-language': u'pt',
            'pub-date': {
                'month': u'08',
                'year': u'2010'
            },
            'volume': u'44',
            'number': u'4',
            'fpage': u'601',
            'lpage': u'610',
            'urls': {
                'full-text-page': u'http://www.scielo.br/scielo.php?script=sci_arttext&amp;pid=S0034-89102010000400003&amp;lng=en&amp;tlng=en',
                'issue-page': u'http://www.scielo.br/scielo.php?script=sci_issuetoc&amp;pid=S0034-891020100004&amp;lng=en&amp;tlng=en',
                'journal-page': u'http://www.scielo.br/scielo.php?script=sci_serial&amp;pid=0034-8910&amp;lng=en&amp;tlng=en'
            },
            'article-ids': {
                'publisher-id': u'S0034-89102010000400003',
                'doi': u'10.1590/S0034-89102010000400003'
            },
            'subjects': {
                'wos': [u'PUBLIC, ENVIROMENTAL & OCCUPATIONAL HEATH', u'SOCIOLOGY'],
                'cnpq': [u'public health']
            },
            'title-group': {
                'pt': u'Uso de medicamentos por pessoas com deficiências em áreas do estado de São Paulo',
                'es': u'Uso de medicamentos por personas con deficiencias en áreas del Estado de Sao Paulo, Sureste de Brasil',
                'en': u'Use of medicines by persons with disabilities in São Paulo state areas, Southeastern Brazil'
            },
            'contrib-group': {
                'authors': [{
                    'surname': u'Castro',
                    'given-names': u'Shamyr Sulyvan',
                    'role': u'ND',
                    'affiliations': [u'A01']
                    },
                    {
                    'surname': u'Pelicione',
                    'given-names': u'Americo Focesi',
                    'role': u'ND',
                    'affiliations': [u'A02']
                    },
                    {
                    'surname': u'Cesar',
                    'given-names': u'Chester Luiz Galvão',
                    'role': u'ND',
                    'affiliations': [u'A03']
                    },
                    {
                    'surname': u'Carandina',
                    'given-names': u'Luana',
                    'role': u'ND',
                    'affiliations': [u'A04']
                    },
                    {
                    'surname': u'Barros',
                    'given-names': u'Marilisa Berti de Azevedo',
                    'role': u'ND',
                    'affiliations': [u'A05']
                    },
                    {
                    'surname': u'Alves',
                    'given-names': u'Maria Cecilia Goi Porto',
                    'role': u'ND',
                    'affiliations': [u'A06']
                    },
                    {
                    'surname': u'Goldbaum',
                    'given-names': u'Moisés',
                    'role': u'ND',
                    'affiliations': [u'A07']
                    },
                ],
                'coordinators': [
                    {
                    'surname': u'Goldbaum',
                    'given-names': u'Moisés',
                    'role': u'ND',
                    'affiliations': [u'A07']
                    },
                ],
                'affiliations': [
                    {
                    'addr-line': u'São Paulo',
                    'institution': u'Universidade de São Paulo',
                    'country': u'Brasil',
                    'ref': u'A01',
                    },
                    {
                    'addr-line': u'São Paulo',
                    'institution': u'Faculdades Metropolitanas Unidas',
                    'country': u'Brasil',
                    'ref': u'A02',
                    },
                    {
                    'addr-line': u'São Paulo',
                    'institution': u'USP',
                    'country': u'Brasil',
                    'ref': u'A03',
                    },
                    {
                    'addr-line': u'Botucatu',
                    'institution': u'Universidade Estadual Paulista Julio de Mesquita Filho',
                    'country': u'Brasil',
                    'ref': u'A04',
                    },
                    {
                    'addr-line': u'Campinas',
                    'institution': u'Universidade Federal de Campinas',
                    'country': u'Brasil',
                    'ref': u'A05',
                    },
                    {
                    'addr-line': u'São Paulo',
                    'institution': u'Secretaria de Saúde do Estado de São Paulo',
                    'country': u'Brasil',
                    'ref': u'A06',
                    },
                    {
                    'addr-line': u'São Paulo',
                    'institution': u'USP',
                    'country': u'Brasil',
                    'ref': u'A07',
                    },
                ],
                'abstract': {
                    'pt': u'OBJETIVO: Analisar o consumo de medicamentos e os principais grupos terapêuticos consumidos por pessoas com deficiências físicas, auditivas ou visuais. MÉTODOS: Estudo transversal em que foram analisados dados do Inquérito Multicêntrico de Saúde no Estado de São Paulo (ISA-SP) em 2002 e do Inquérito de Saúde no Município de São Paulo (ISA-Capital), realizado em 2003. Os entrevistados que referiram deficiências foram estudados segundo as variáveis que compõem o banco de dados: área, sexo, renda, faixa etária, raça, consumo de medicamentos e tipos de medicamentos consumidos. RESULTADOS: A percentagem de consumo entre as pessoas com deficiência foi de: 62,8% entre os visuais; 60,2% entre os auditivos e 70,1% entre os físicos. As pessoas com deficiência física consumiram 20% mais medicamentos que os não-deficientes. Entre as pessoas com deficiência visual, os medicamentos mais consumidos foram os diuréticos, agentes do sistema renina-angiotensina e analgésicos. Pessoas com deficiência auditiva utilizaram mais analgésicos e agentes do sistema renina-angiotensina. Entre indivíduos com deficiência física, analgésicos, antitrombóticos e agentes do sistema renina-angiotensina foram os medicamentos mais consumidos. CONCLUSÕES: Houve maior consumo de medicamentos entre as pessoas com deficiências quando comparados com os não-deficientes, sendo os indivíduos com deficiência física os que mais consumiram fármacos, seguidos de deficientes visuais e auditivos.',
                    'es': u'OBJETIVO: Analizar el consumo de medicamentos y los principales grupos terapéuticos consumidos por personas con deficiencias físicas, auditivas o visuales. MÉTODOS: Estudio transversal en que fueron analizados datos de la Pesquisa Multicentrica de Salud en el Estado de Sao Paulo (ISA-SP) en 2002 y de la Pesquisa de Salud en el Municipio de Sao Paulo (ISA-Capital), realizado en 2003. Los entrevistados que refirieron deficiencias fueron estudiados según las variables que componen el banco de datos: área, sexo, renta, grupo etario, raza, consumo de medicamentos y tipos de medicamentos consumidos. RESULTADOS: El porcentaje de consumo entre las personas con deficiencia fue de: 62,8% entre los visuales; 60,2% entre los auditivos y de 70,1% entre los físicos. Las personas con deficiencia física consumieron 20% más medicamentos que los no deficientes. Entre las personas con deficiencia visual, los medicamentos más consumidos fueron los diuréticos, agentes del sistema renina-angiotensina y analgésicos. Personas con deficiencia auditiva utilizaron más analgésicos y agentes del sistema renina-angiotensina. Entre individuos con deficiencia física, analgésicos, antitrombóticos y agentes del sistema renina-angiotensina fueron los medicamentos más consumidos. CONCLUSIONES: Hubo mayor consumo de medicamentos entre las personas con deficiencias al compararse con los no deficientes, siendo los individuos con deficiencia física los que más consumieron fármacos, seguidos de los deficientes visuales y auditivos.',
                    'en': u'OBJECTIVE: To analyze the use of medicines and the main therapeutic groups consumed by persons with physical, hearing and visual disabilities. METHODS: A cross-sectional study was performed, where data from the 2002 Inquérito Multicêntrico de Saúde no Estado de São Paulo (ISA-SP - São Paulo State Multicenter Health Survey), as well as the 2003 Inquérito de Saúde no Município de São Paulo (ISA-Capital - City of São Paulo Health Survey), Southeastern Brazil, were analyzed. Respondents who reported having disabilities were studied, according to variables that comprise the database: geographic area, gender, income, age group, ethnic group, use of medicines and types of drugs consumed. RESULTS: The percentage of use of drugs by persons with disabilities was 62.8% among the visually impaired; 60.2% among the hearing impaired; and 70.1% among the persons with physical disabilities. Individuals with physical disabilities consumed 20% more medications than non-disabled ones. Among persons with visual disabilities, the most frequently consumed drugs were diuretics, agents of the renin-angiotensin system and analgesics. Persons with hearing disabilities used more analgesics and agents of the renin-angiotensin system. Among those with physical disabilities, analgesics, antithrombotics and agents of the renin-angiotensin system were the most frequently consumed medicines. CONCLUSIONS: There was a greater use of medicines among persons with disabilities than non-disabled ones. Persons with physical disabilities were those who most consumed medicines, followed by the visually impaired and the hearing impaired.'
                },
                'keyword-group': {
                    'pt': [u'Pessoas com Deficiência', u'Uso de Medicamentos', u'Inquéritos de Morbidade'],
                    'es': [u'Personas con Discapacidad', u'Utilización de Medicamentos', u'Medicamentos de Uso Contínuo', u'Encuestas de Morbilidad'],
                    'en': [u'Disabled Persons', u'Drug Utilization', u'Drugs of Continuous Use', u'Morbidity Surveys']
                }
            },

        },
        'body': u'<p>All body content</p>',
        'back': [
            {
                'article-title': u'Alternatives for logistic regression in cross-sectional studies: an empirical comparison of models that directly estimate the prevalence ratio',
                'type': u'journal'
            }
        ]
    }

XML Sample
==========

.. code-block:: javascript

    <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" dtd-version="3.0" article-type="research-article" lang_id="pt">
        <front>
            <journal-meta>
                <journal-id journal-id-type="publisher">rsp</journal-id>
                <journal-title-group>
                    <journal-title>Revista de Saúde Pública</journal-title><abbrev-journal-title>Rev. Saúde Pública</abbrev-journal-title></journal-title-group><issn>0034-8910</issn><publisher><publisher-name>Faculdade de Saúde Pública da Universidade de São Paulo</publisher-name><publisher-loc>São Paulo</publisher-loc></publisher></journal-meta><article-meta><unique-article-id pub-id-type="publisher-id">S0034-89102010000400003</unique-article-id><article-id pub-id-type="publisher-id">S0034-89102010000400003</article-id><article-id pub-id-type="doi">10.1590/S0034-89102010000400003</article-id><article-categories><subj-group><subject>PUBLIC, ENVIRONMENTAL &amp; OCCUPATIONAL HEALTH</subject><subject>SOCIOLOGY</subject></subj-group></article-categories><title-group><article-title lang_id="pt">Uso de medicamentos por pessoas com deficiências em áreas do estado de São Paulo</article-title><trans-title-group lang_id="en"><trans-title>Use of medicines by persons with disabilities in São Paulo state areas, Southeastern Brazil</trans-title></trans-title-group><trans-title-group lang_id="es"><trans-title>Uso de medicamentos por personas con deficiencias en áreas del Estado de Sao Paulo, Sureste de Brasil</trans-title></trans-title-group></title-group><contrib-group><contrib contrib-type="author"><name><surname>Castro</surname><given-names>Shamyr Sulyvan</given-names></name><role>ND</role><xref ref-type="aff" rid="A01"></xref></contrib><contrib contrib-type="author"><name><surname>Pelicioni</surname><given-names>Americo Focesi</given-names></name><role>ND</role><xref ref-type="aff" rid="A02"></xref></contrib><contrib contrib-type="author"><name><surname>Cesar</surname><given-names>Chester Luiz Galvão</given-names></name><role>ND</role><xref ref-type="aff" rid="A03"></xref></contrib><contrib contrib-type="author"><name><surname>Carandina</surname><given-names>Luana</given-names></name><role>ND</role><xref ref-type="aff" rid="A04"></xref></contrib><contrib contrib-type="author"><name><surname>Barros</surname><given-names>Marilisa Berti de Azevedo</given-names></name><role>ND</role><xref ref-type="aff" rid="A05"></xref></contrib><contrib contrib-type="author"><name><surname>Alves</surname><given-names>Maria Cecilia Goi Porto</given-names></name><role>ND</role><xref ref-type="aff" rid="A06"></xref></contrib><contrib contrib-type="author"><name><surname>Goldbaum</surname><given-names>Moisés</given-names></name><role>ND</role><xref ref-type="aff" rid="A07"></xref></contrib></contrib-group><aff id="A01"><addr-line>São Paulo</addr-line><institution>Universidade de São Paulo</institution><country>Brasil</country></aff><aff id="A02"><addr-line>São Paulo</addr-line><institution>Faculdades Metropolitanas Unidas</institution><country>Brasil</country></aff><aff id="A03"><addr-line>São Paulo</addr-line><institution>USP</institution><country>Brasil</country></aff><aff id="A04"><addr-line>Botucatu</addr-line><institution>Universidade Estadual Paulista Julio de Mesquita Filho</institution><country>Brasil</country></aff><aff id="A05"><addr-line>Campinas</addr-line><institution>Universidade Estadual de Campinas</institution><country>Brasil</country></aff><aff id="A06"><addr-line>São Paulo</addr-line><institution>Secretaria de Saúde do Estado de São Paulo</institution><country>Brasil</country></aff><aff id="A07"><addr-line>São Paulo</addr-line><institution>USP</institution><country>Brasil</country></aff><pub-date><month>08</month><year>2010</year></pub-date><volume>44</volume><issue>4</issue><fpage>601</fpage><lpage>610</lpage><self-uri xlink:href="http://www.scielo.br/scielo.php?script=sci_arttext&amp;amp;pid=S0034-89102010000400003&amp;amp;lng=en&amp;amp;tlng=en" content-type="full_text_page">Full Text</self-uri><self-uri xlink:href="http://www.scielo.br/scielo.php?script=sci_issuetoc&amp;amp;pid=S0034-891020100004&amp;amp;lng=en&amp;amp;tlng=en" content-type="issue_page">Issue Page</self-uri><self-uri xlink:href="http://www.scielo.br/scielo.php?script=sci_serial&amp;amp;pid=0034-8910&amp;amp;lng=en&amp;amp;tlng=en" content-type="journal_page">Journal Page</self-uri><abstract lang_id="pt"><p>OBJETIVO: Analisar o consumo de medicamentos e os principais grupos terapêuticos consumidos por pessoas com deficiências físicas, auditivas ou visuais. MÉTODOS: Estudo transversal em que foram analisados dados do Inquérito Multicêntrico de Saúde no Estado de São Paulo (ISA-SP) em 2002 e do Inquérito de Saúde no Município de São Paulo (ISA-Capital), realizado em 2003. Os entrevistados que referiram deficiências foram estudados segundo as variáveis que compõem o banco de dados: área, sexo, renda, faixa etária, raça, consumo de medicamentos e tipos de medicamentos consumidos. RESULTADOS: A percentagem de consumo entre as pessoas com deficiência foi de: 62,8% entre os visuais; 60,2% entre os auditivos e 70,1% entre os físicos. As pessoas com deficiência física consumiram 20% mais medicamentos que os não-deficientes. Entre as pessoas com deficiência visual, os medicamentos mais consumidos foram os diuréticos, agentes do sistema renina-angiotensina e analgésicos. Pessoas com deficiência auditiva utilizaram mais analgésicos e agentes do sistema renina-angiotensina. Entre indivíduos com deficiência física, analgésicos, antitrombóticos e agentes do sistema renina-angiotensina foram os medicamentos mais consumidos. CONCLUSÕES: Houve maior consumo de medicamentos entre as pessoas com deficiências quando comparados com os não-deficientes, sendo os indivíduos com deficiência física os que mais consumiram fármacos, seguidos de deficientes visuais e auditivos.</p></abstract><trans-abstract lang_id="en"><p>OBJECTIVE: To analyze the use of medicines and the main therapeutic groups consumed by persons with physical, hearing and visual disabilities. METHODS: A cross-sectional study was performed, where data from the 2002 Inquérito Multicêntrico de Saúde no Estado de São Paulo (ISA-SP - São Paulo State Multicenter Health Survey), as well as the 2003 Inquérito de Saúde no Município de São Paulo (ISA-Capital - City of São Paulo Health Survey), Southeastern Brazil, were analyzed. Respondents who reported having disabilities were studied, according to variables that comprise the database: geographic area, gender, income, age group, ethnic group, use of medicines and types of drugs consumed. RESULTS: The percentage of use of drugs by persons with disabilities was 62.8% among the visually impaired; 60.2% among the hearing impaired; and 70.1% among the persons with physical disabilities. Individuals with physical disabilities consumed 20% more medications than non-disabled ones. Among persons with visual disabilities, the most frequently consumed drugs were diuretics, agents of the renin-angiotensin system and analgesics. Persons with hearing disabilities used more analgesics and agents of the renin-angiotensin system. Among those with physical disabilities, analgesics, antithrombotics and agents of the renin-angiotensin system were the most frequently consumed medicines. CONCLUSIONS: There was a greater use of medicines among persons with disabilities than non-disabled ones. Persons with physical disabilities were those who most consumed medicines, followed by the visually impaired and the hearing impaired.</p></trans-abstract><trans-abstract lang_id="es"><p>OBJETIVO: Analizar el consumo de medicamentos y los principales grupos terapéuticos consumidos por personas con deficiencias físicas, auditivas o visuales. MÉTODOS: Estudio transversal en que fueron analizados datos de la Pesquisa Multicentrica de Salud en el Estado de Sao Paulo (ISA-SP) en 2002 y de la Pesquisa de Salud en el Municipio de Sao Paulo (ISA-Capital), realizado en 2003. Los entrevistados que refirieron deficiencias fueron estudiados según las variables que componen el banco de datos: área, sexo, renta, grupo etario, raza, consumo de medicamentos y tipos de medicamentos consumidos. RESULTADOS: El porcentaje de consumo entre las personas con deficiencia fue de: 62,8% entre los visuales; 60,2% entre los auditivos y de 70,1% entre los físicos. Las personas con deficiencia física consumieron 20% más medicamentos que los no deficientes. Entre las personas con deficiencia visual, los medicamentos más consumidos fueron los diuréticos, agentes del sistema renina-angiotensina y analgésicos. Personas con deficiencia auditiva utilizaron más analgésicos y agentes del sistema renina-angiotensina. Entre individuos con deficiencia física, analgésicos, antitrombóticos y agentes del sistema renina-angiotensina fueron los medicamentos más consumidos. CONCLUSIONES: Hubo mayor consumo de medicamentos entre las personas con deficiencias al compararse con los no deficientes, siendo los individuos con deficiencia física los que más consumieron fármacos, seguidos de los deficientes visuales y auditivos.</p></trans-abstract><kwd-group lang_id="en" kwd-group-type="author-generated"><kwd>Disabled Persons</kwd><kwd>Drug Utilization</kwd><kwd>Drugs of Continuous Use</kwd><kwd>Morbidity Surveys</kwd></kwd-group><kwd-group lang_id="es" kwd-group-type="author-generated"><kwd>Personas con Discapacidad</kwd><kwd>Utilización de Medicamentos</kwd><kwd>Medicamentos de Uso Contínuo</kwd><kwd>Encuestas de Morbilidad</kwd></kwd-group><kwd-group lang_id="pt" kwd-group-type="author-generated"><kwd>Pessoas com Deficiência</kwd><kwd>Uso de Medicamentos</kwd><kwd>Inquéritos de Morbidade</kwd></kwd-group></article-meta></front><back><ref-list><ref id="B1"><element-citation publication-type="article"><article-title>Alternatives for logistic regression in cross-sectional studies: an empirical comparison of models that directly estimate the prevalence ratio</article-title><source>BMC Med Res Methodol</source><date><year>2003</year></date><fpage>21</fpage><volume>3</volume><person-group><name><surname>Barros</surname><given-names>AJD</given-names></name><name><surname>Hirakata</surname><given-names>VN</given-names></name></person-group></element-citation></ref><ref id="B2"><element-citation publication-type="article"><article-title>Utilização de medicamentos em adultos: prevalência e determinantes individuais</article-title><source>Rev Saude Publica</source><date><year>2004</year></date><fpage>228</fpage><issn>0034-8910</issn><issue>2</issue><volume>38</volume><lpage>38</lpage><person-group><name><surname>Bertoldi</surname><given-names>AD</given-names></name><name><surname>Barros</surname><given-names>AJD</given-names></name><name><surname>Hallal</surname><given-names>PC</given-names></name><name><surname>Lima</surname><given-names>RC</given-names></name></person-group></element-citation></ref><ref id="B3"><element-citation publication-type="article"><article-title>Utilization of medicines by the Brazilian population, 2003</article-title><source>Cad Saude Publica</source><date><year>2005</year></date><fpage>100</fpage><issn>0102-311X</issn><issue></issue><volume>21</volume><lpage>8</lpage><person-group><name><surname>Carvalho</surname><given-names>MF</given-names></name><name><surname>Pascom</surname><given-names>ARP</given-names></name><name><surname>Souza-Jr</surname><given-names>PRB</given-names></name><name><surname>Damacena</surname><given-names>GM</given-names></name><name><surname>Szwarcwald</surname><given-names>CL</given-names></name></person-group></element-citation></ref><ref id="B4"><element-citation publication-type="article"><article-title>Deficiência visual, auditiva e física: prevalência e fatores associados em estudo de base populacional</article-title><source>Cad Saude Publica</source><date><year>2008</year></date><fpage>1773</fpage><issn>0102-311X</issn><issue>8</issue><volume>24</volume><lpage>82</lpage><person-group><name><surname>Castro</surname><given-names>SS</given-names></name><name><surname>Cesar</surname><given-names>CLG</given-names></name><name><surname>Carandina</surname><given-names>L</given-names></name><name><surname>Barros</surname><given-names>MBA</given-names></name><name><surname>Alves</surname><given-names>MCGP</given-names></name><name><surname>Goldbaum</surname><given-names>M</given-names></name></person-group></element-citation></ref><ref id="B5"><element-citation publication-type="article"><article-title>Physical disability, recent illnesses and health self-assessment in a population-based study in São Paulo, Brazil</article-title><source>Disabil Rehabil</source><issn>0963-8288</issn><person-group><name><surname>Castro</surname><given-names>SS</given-names></name><name><surname>Cesar</surname><given-names>CL</given-names></name><name><surname>Carandina</surname><given-names>L</given-names></name><name><surname>Barros</surname><given-names>MB</given-names></name><name><surname>Alves</surname><given-names>MC</given-names></name><name><surname>Goldbaum</surname><given-names>M</given-names></name></person-group></element-citation></ref><ref id="B6"><element-citation publication-type="article"><article-title>Secondary conditions and women with physical disabilities: a descriptive study</article-title><source>Arch Phys Med Rehabil</source><date><year>2000</year></date><fpage>1380</fpage><issn>0003-9993</issn><issue>10</issue><volume>81</volume><lpage>7</lpage><person-group><name><surname>Coyle</surname><given-names>CP</given-names></name><name><surname>Santiago</surname><given-names>MC</given-names></name><name><surname>Shank</surname><given-names>JW</given-names></name><name><surname>Ma</surname><given-names>GX</given-names></name><name><surname>Boyd</surname><given-names>R</given-names></name></person-group></element-citation></ref><ref id="B7"><element-citation publication-type="article"><article-title>Relationship between use of diuretics and continence status in the elderly</article-title><source>Urology</source><date><year>1991</year></date><fpage>39</fpage><issn>0090-4295</issn><issue>1</issue><volume>8</volume><lpage>42</lpage><person-group><name><surname>Diokno</surname><given-names>AC</given-names></name><name><surname>Brown</surname><given-names>MB</given-names></name><name><surname>Herzog</surname><given-names>AR</given-names></name></person-group></element-citation></ref><ref id="B8"><element-citation publication-type="article"><article-title>The Tromsø study: Frequency and predicting factors of analgesic drug use in a free-living population (12-56 years)</article-title><source>J Clin Epidemiol</source><date><year>1993</year></date><fpage>1297</fpage><issn>0895-4356</issn><issue>11</issue><volume>46</volume><lpage>304</lpage><person-group><name><surname>Eggen</surname><given-names>AE</given-names></name></person-group></element-citation></ref><ref id="B9"><element-citation publication-type="article"><article-title>Chronic pain secondary to disability: a review</article-title><source>Clin J Pain</source><date><year>2003</year></date><fpage>3</fpage><issn>0749-8047</issn><issue>1</issue><volume>19</volume><lpage>17</lpage><person-group><name><surname>Ehde</surname><given-names>DM</given-names></name><name><surname>Jensen</surname><given-names>MP</given-names></name><name><surname>Engel</surname><given-names>JM</given-names></name><name><surname>Turner</surname><given-names>JA</given-names></name><name><surname>Hoffman</surname><given-names>AJ</given-names></name><name><surname>Cardenas</surname><given-names>DD</given-names></name></person-group></element-citation></ref><ref id="B10"><element-citation publication-type="article"><article-title>Concerns with chronic analgesic therapy in elderly patients</article-title><source>Am J Med</source><date><year>1996</year></date><fpage>19S</fpage><issn>0002-9343</issn><issue>1A</issue><volume>101</volume><lpage>24</lpage><person-group><name><surname>Gloth FM</surname><given-names>3rd</given-names></name></person-group></element-citation></ref><ref id="B11"><element-citation publication-type="article"><article-title>Health promotion for persons with disabilities: what does the literature reveal?</article-title><source>Fam Community Health</source><date><year>2006</year></date><fpage>12</fpage><issn>0160-6379</issn><issue></issue><volume>29</volume><lpage>9</lpage><person-group><name><surname>Harrison</surname><given-names>T</given-names></name></person-group></element-citation></ref><ref id="B12"><element-citation publication-type="book"><source>Health care: an international study</source><date><year>1976</year></date><person-group><name><surname>Kohn</surname><given-names>R</given-names></name><name><surname>White</surname><given-names>KL</given-names></name></person-group><publisher-loc>London</publisher-loc></element-citation></ref><ref id="B13"><element-citation publication-type="article"><article-title>Prevalência e fatores associados à automedicação: resultados do projeto Bambuí</article-title><source>Rev Saude Publica</source><date><year>2002</year></date><fpage>55</fpage><issn>0034-8910</issn><issue>1</issue><volume>36</volume><lpage>62</lpage><person-group><name><surname>Loyola Filho</surname><given-names>AI</given-names></name><name><surname>Uchoa</surname><given-names>E</given-names></name><name><surname>Guerra</surname><given-names>HL</given-names></name><name><surname>Firmo</surname><given-names>JOA</given-names></name><name><surname>Lima-Costa</surname><given-names>MF</given-names></name></person-group></element-citation></ref><ref id="B14"><element-citation publication-type="article"><article-title>The epidemiology of cataract in Australia</article-title><source>Am J Ophthalmol</source><date><year>1999</year></date><fpage>446</fpage><issn>0002-9394</issn><issue>4</issue><volume>128</volume><lpage>65</lpage><person-group><name><surname>McCarty</surname><given-names>CA</given-names></name><name><surname>Mukesh</surname><given-names>BN</given-names></name><name><surname>Fu</surname><given-names>CL</given-names></name><name><surname>Taylor</surname><given-names>HR</given-names></name></person-group></element-citation></ref><ref id="B15"><element-citation publication-type="article"><article-title>Use of analgesics in adults with pain complaints: prevalence and associated factors, Turkey</article-title><source>Rev Saude Publica</source><date><year>2009</year></date><fpage>140</fpage><issn>0034-8910</issn><issue>1</issue><volume>43</volume><lpage>6</lpage><person-group><name><surname>Ozkan</surname><given-names>O</given-names></name><name><surname>Hamzaoglu</surname><given-names>O</given-names></name><name><surname>Erdine</surname><given-names>S</given-names></name><name><surname>Balta</surname><given-names>E</given-names></name><name><surname>Domac</surname><given-names>M</given-names></name></person-group></element-citation></ref><ref id="B16"><element-citation publication-type="article"><article-title>Prescription and non-prescription analgesic use among the US adult population: results from the third National Health and Nutrition Examination Survey (NHANES III)</article-title><source>Pharmacoepidemiol Drug Saf</source><date><year>2003</year></date><fpage>315</fpage><issue>4</issue><volume>12</volume><lpage>26</lpage><person-group><name><surname>Paulose-Ram</surname><given-names>R</given-names></name><name><surname>Hirsch</surname><given-names>R</given-names></name><name><surname>Dillon</surname><given-names>C</given-names></name><name><surname>Losonczy</surname><given-names>K</given-names></name><name><surname>Cooper</surname><given-names>M</given-names></name><name><surname>Ostchega</surname><given-names>Y</given-names></name></person-group></element-citation></ref><ref id="B17"><element-citation publication-type="article"><article-title>Physical disability in the Netherlands: prevalence, risk groups and time trends</article-title><source>Public Health</source><date><year>2002</year></date><fpage>231</fpage><issn>0033-3492</issn><issue>4</issue><volume>116</volume><lpage>7</lpage><person-group><name><surname>Picavet</surname><given-names>HSJ</given-names></name><name><surname>Hoeymans</surname><given-names>N</given-names></name></person-group></element-citation></ref><ref id="B18"><element-citation publication-type="article"><article-title>Pain, impairment, and disability in the AMA guides</article-title><source>J Law Med Ethics</source><date><year>2004</year></date><fpage>315</fpage><issn>1073-1105</issn><issue>2</issue><volume>32</volume><lpage>26</lpage><person-group><name><surname>Robinson</surname><given-names>JP</given-names></name><name><surname>Turk</surname><given-names>DC</given-names></name><name><surname>Loeser</surname><given-names>JD</given-names></name></person-group></element-citation></ref><ref id="B19"><element-citation publication-type="article"><article-title>Prevalência, fatores associados e mau uso de medicamentos entre idosos: uma revisão</article-title><source>Cad Saude Publica</source><date><year>2003</year></date><fpage>717</fpage><issn>0102-311X</issn><issue>3</issue><volume>19</volume><lpage>24</lpage><person-group><name><surname>Rozenfeld</surname><given-names>S</given-names></name></person-group></element-citation></ref><ref id="B20"><element-citation publication-type="article"><article-title>Systolic hypertension in the elderly: arterial wall mechanical properties and the renin-angiotensin-aldosterone system</article-title><source>J Hypertens</source><date><year>2005</year></date><fpage>673</fpage><issn>0263-6352</issn><issue>4</issue><volume>23</volume><lpage>81</lpage><person-group><name><surname>Safar</surname><given-names>ME</given-names></name></person-group></element-citation></ref><ref id="B21"><element-citation publication-type="article"><article-title>Prevalencia del consumo de medicamentos em la población adulta de Cataluña</article-title><source>Gac Sanit</source><date><year>2002</year></date><fpage>121</fpage><issn>0213-9111</issn><issue>2</issue><volume>16</volume><lpage>30</lpage><person-group><name><surname>Sans</surname><given-names>S</given-names></name><name><surname>Paluzie</surname><given-names>G</given-names></name><name><surname>Puig</surname><given-names>T</given-names></name><name><surname>Balañá</surname><given-names>L</given-names></name><name><surname>Balaguer-Vintró</surname><given-names>I</given-names></name></person-group></element-citation></ref><ref id="B22"><element-citation publication-type="article"><article-title>Indicadores do uso de medicamentos prescritos e de assistência ao paciente de serviços de saúde</article-title><source>Rev Saude Publica</source><date><year>2004</year></date><fpage>819</fpage><issn>0034-8910</issn><issue>6</issue><volume>38</volume><lpage>26</lpage><person-group><name><surname>Santos</surname><given-names>V</given-names></name><name><surname>Nitrini</surname><given-names>SMOO</given-names></name></person-group></element-citation></ref><ref id="B23"><element-citation publication-type="article"><article-title>¿Odds Ratio o razón de proporciones?: Su utilización en estudios transversales</article-title><source>Gac Sanit</source><date><year>2003</year></date><fpage>70</fpage><issn>0213-9111</issn><issue>1</issue><volume>17</volume><lpage>4</lpage><person-group><name><surname>Schiaffino</surname><given-names>A</given-names></name><name><surname>Rodriguez</surname><given-names>M</given-names></name><name><surname>Pasarin</surname><given-names>MI</given-names></name><name><surname>Regidor</surname><given-names>E</given-names></name><name><surname>Borrel</surname><given-names>C</given-names></name><name><surname>Fernandez</surname><given-names>E</given-names></name></person-group></element-citation></ref><ref id="B24"><element-citation publication-type="article"><article-title>Use of diuretics and opportunities for withdrawal in a Dutch nursing home population</article-title><source>Neth J Med</source><date><year>1998</year></date><fpage>20</fpage><issn>0300-2977</issn><issue>1</issue><volume>53</volume><lpage>6</lpage><person-group><name><surname>van Kraaij</surname><given-names>DJ</given-names></name><name><surname>Jansen</surname><given-names>RW</given-names></name><name><surname>Gribnau</surname><given-names>FW</given-names></name><name><surname>Hoefnagels</surname><given-names>WH</given-names></name></person-group></element-citation></ref><ref id="B25"><element-citation publication-type="book"><source>Collaborating Centre for Drug Statistics Methodology: Guidelines for ATC classification and DDD assignment</source><date><year>2000</year></date><edition>3</edition><institution>World Health Organization</institution><publisher-loc>Oslo</publisher-loc></element-citation></ref></ref-list></back></article>