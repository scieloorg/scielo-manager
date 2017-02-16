====================================
Exportação para bases ISIS do SciELO
====================================

--------
Objetivo
--------

Essa documentação tem como objetivo documentar os requisitos necessários para criar uma rotina de exportação dos metadados inseridos no SciELO Manager para o formato de bases de dados atual do SciELO.

------------
Antecedentes
------------

O projeto SciELO no início utilizou como definição de metadados a metodologia LILACS da BIREME. A metodologia LILACS se caracteriza pela capacidade de permitir o amarzenamento de diversos tipos de documentos, neste sentido, na época, a ferramenta desenvolvida para gestão de títulos e fascículos da SciELO teve como premissa, contemplar todas características de metadados da metodologia LILACS.

Durante os 15 anos de operação da SciELO foi possível detectar pelas equipes de produção e desenvolvimento de aplicativos que boa parte dos campos não erão utilizados por não se encaixarem nas características de metadados de periódicos.

Para a nova versão da ferramenta de gestão de periódicos, considerando as características dos metadados inseridos na coleção nos últimos 15 anos, foi decidido junto com a equipe de gestão e publicação de conteúdo avaliar quais eram os metadados realmente necessários para a metodologia SciELO.

----------
Introdução
----------

As bases de dados ISIS geradas pelo Title Manager são utilizadas em dois pontos do processo de publicação da SciELO, são eles: processo de marcação e processamento para inclusão de conteúdo.

Processamento para inclusão de conteúdo
=======================================

Atualmente o SciELO possui um processamento (geraPadrao.bat) para inclusão de novas revistas, fascículos e artigos na coleção. Esse processamento recebe como entrada um conjunto de bases de dados, são elas: artigo, issue, code, title.

As bases code, title e issue são únicas para todo o processamento, significa que uma base de dados com todo o conteúdo de título, outra com todo conteúdo de code e outra com todo conteúdo de issues são geradas e gravadas em um diretório chamado serial gerando a seguinte estrutura de dados de entrada para o processamento.

.. code-block:: text

  serial/
  serial/title
  serial/title/title.mst
  serial/title/title.xrf
  serial/code
  serial/code/newcode.mst
  serial/code/newcode.xrf
  serial/issue
  serial/issue/issue.mst
  serial/issue/issue.xrf

Para criação da base de dados de artigos são criadas diversas pequenas bases que representam cada fascículo do periódico. Essas bases de dados são gravadas seguindo a seguinte estrutura de dados de entrada para o processamento.

.. code-block:: text

  serial/
  serial/bjmbr
  serial/bjmbr/v40n5
  serial/bjmbr/v40n5/v40n5.mst
  serial/bjmbr/v40n5/v40n5.xrf
  serial/bjmbr/v40n5/base
  serial/bjmbr/v40n5/base/v40n5.mst
  serial/bjmbr/v40n5/base/v40n5.xrf
  serial/bjmbr/v41n1
  serial/bjmbr/v41n1/v41n1.mst
  serial/bjmbr/v41n1/v41n1.xrf
  serial/bjmbr/v41n1/base
  serial/bjmbr/v41n1/base/v41n1.mst
  serial/bjmbr/v41n1/base/v41n1.xrf
  serial/rpsp/v10n1
  serial/rpsp/v10n1/v10n1.mst
  serial/rpsp/v10n1/v10n1.xrf
  serial/rpsp/v10n1/base
  serial/rpsp/v10n1/base/v10n1.mst
  serial/rpsp/v10n1/base/v10n1.xrf

Em resumo, significa que o processo de exportação de bases do SciELO Manager para ISIS deve gerar essa estrutura de arquivos como entrada para o processamento de inclusão de novos conteúdos na coleção. Mais a frente será tratada a estrutura de dados dessas bases de dados.

Processo de Marcação
====================

O processo de marcação de metadados de artigos nas SciELO é feito através da ferramenta Markup, que corresponde a um aplicativo VBScript embutido no Word para identificar os elementos dos artigos. Esse plugin do Word consulta algumas bases de dados ISIS geradas pela Title Manager para complementar a identificação de elementos no texto do artigo, como por exemplo:

* Identificação de seções dos fascículos (base code)

A exportação de dados da ferramenta SciELO Manager deve gerar as bases de dados utilizadas pelo Markup e gravá-las seguindo a seguinte extrutura de dados.

.. code-block:: text

 /serial
 /serial/code
 /serial/code/newcode.mst
 /serial/code/newcode.xrf

Em resumo, significa que o processo de exportação de bases do SciELO Manager para ISIS deve gerar essa estrutura de arquivos como entrada para o processo de marcação. Mais a frente será tratada a estrutura de dados dessas bases de dados.

* Arquivos textos para ferramenta de Markup

Alguns arquivos texto também são gerados como entrada de dados para ferramenta de marcação, são eles:

 * **automata.mds**

  Formato::

    ISSN;<tag_citat>;<acron>.amd;tg<norma>.amd

  Onde:

    <tag_citat> é tag da citação, podendo ser:

      * ocitat para other 
      * vcitat para vancouver
      * acitat para abnt
      * icitat para iso
      * pcitat para apa

    <norma> é um dos valores, podendo ser: 

      * other (other standard)
      * vancouv (the vancouver group - uniform requirements for manuscripts submitted to biomedical journals) 
      * apa (American Psychological Association)
      * nbr6023 (nbr 6023/89 - associação nacional de normas técnicas)
      * iso690 (iso 690/87 - international standard organization)

    Valores utilizados no arquivo automata.mds

      * icitat
      * acitat
      * ocitat
      * vcitat
      * pcitat

    Valores utilizados no arquivo LANGUAGE_issue.mds

      * iso 690/87 - international standard organization
      * nbr 6023/89 - associação nacional de normas técnicas
      * other standard
      * the vancouver group - uniform requirements for manuscripts submitted to biomedical journals
      * American Psychological Association

    Valores utilizados para o arquivo journal_standart.txt

      * iso690
      * nbr6023
      * other
      * vancouv
      * apa 

  Exemplo::

    0044-5967;ocitat;aa.amd;tgother.amd
    0102-3306;ocitat;abb.amd;tgother.a,d
    0102-8650;ocitat;acb.amd;tgother.amd
    1413-7852;ocitat;aob.amd;tgother.amd
    0103-2100;vcitat;ape.amd;tgvanc.amd

 * **issue.mds**

  Formato::

    linha 1: Braz. J. Microbiol. v.41 n.4  # Legenda do número
    linha 2: mes inicial/mes final
    linha 3: issue order (v64 + v36)
    linha 4: em branco
    linha 5: em branco

  Exemplo::

    Braz. J. Microbiol. v.41 n.4
    Jan/Mar  
    20031


    Rev. Saúde Pública  n.ahead pr 2010
    Oct/Dec  
    20032



 * **en_issue.mds, pt_issue.mds e es_issue.mds**

  Formato::

    linha 1: Braz. J. Microbiol. v.41 n.4  # Legenda do número
    linha 2: título abrev;vol;suplvol;num;suplno;dateiso;issn;status
    linha 3: seções separadas por ponto-e-virgula
    linha 4: código das seções separadas por ponto-e-virgula
    linha 5: vocabulario controlado
    linha 6: norma
    linha 7: em branco

  Exemplo::

    Rev. Saúde Pública  n.ahead pr 2010
    Rev. Saúde Pública;;;ahead;;20100000;0034-8910;1
    No section title
    nd
    Health Science Descriptors
    the vancouver group - uniform requirements for manuscripts submitted to biomedical journals

    Rev. Bras. Psiquiatr.  n.ahead 2010
    Rev. Bras. Psiquiatr.;;;ahead;;20100000;1516-4446;1
    No section title
    nd
    Health Science Descriptors
    the vancouver group - uniform requirements for manuscripts submitted to biomedical journals

    Braz. J. Microbiol. v.41 n.4
    Braz. J. Microbiol.;41;;4;;20101200;1517-8382;1
    No section title
    nd
    No Descriptor
    other standard

    Rev. Inst. Med. trop. S. Paulo v.52 n.4
    Rev. Inst. Med. trop. S. Paulo;52;;4;;20100800;0036-4665;1
    Case Report;Animal Envenomation;Malaria;Parasitology;Review;Editorial;Microbiology;Leishmaniasis;Bacteriology;Book Review;No section title
    RIMTSP014;RIMTSP021;RIMTSP070;RIMTSP090;RIMTSP110;RIMTSP200;RIMTSP280;RIMTSP350;RIMTSP580;RIMTSP780;nd
    No Descriptor
    other standard

  * **journal_standard.txt**

  Arquivo CSV com atributos separado por #

  Onde esta "print|online" deve ser indicado apenas um dos valores de acordo com o tipo de ISSN usado na SciELO.

  Formato::

    issn_id#título abreviado#norma#print|online#issn_atual#area temática#título Medline#codigo medline#título completo#acron#print_issn#online_issn

  Exemplo::

------------------------
Requisitos da Exportação
------------------------

Estrutura de dados
==================

Título
``````

Fascículo
`````````

**Fascículos Especiais (Press Release, Ahead, Review in Progress)**


Ficou definido que para esses tipos de fascículos não será feita nenhuma mudança de modelo devido à característica do campo **Number** e **Volume** que pode receber qualquer tipo de conteúdo para identificar um fascículo.

Considerando que esse conteúdo é livre não caberá normalização.

A regra de negócio para esses dados será a seguinte:

1. Informação de número especial "es/esp", único "unico", composição de números "10-14", números compostos de letras "1a, 1b", etc, deverão ser inseridas no próprio campo **Number** que será de preenchimento livre. Cabe ao documentalista garantir a integridade entre a sequencia de números no SciELO e a sequencia de números da revista.

2. Ahead, Review, Press Release, não mais serão criados pelo SciELO Manager, será considerado que todos periódicos possuem um único Ahead, Review, Press Release. Cabe ao processo de exportação gerar esses fascículos especiais para cada periódico e tratar a apresentação do mesmo no site público caso algum artigo seja marcado como pertencente a um desses fascículos especiais.

3. Campo v6 representa numeração sequencial de fascículos de um periódico, esse campo não deve ser considerado na exportação pois é gerado pelo processamento SciELO.

4. Campos 65 e 64 devem ser construidos utilizando o ano de publicação YYYY concatenado com o mês final de publicação "publication_end_month". MM e precedido de 00 para o caracteres que representam o dia 

  Ex: 20100300


Artigo
``````

Code
````

Remoção de Campos desnecessários
================================

De acordo com reunião realizada em 27 de março alguns campos no contexto da SciELO não serão mais cosiderados pelo SciELO Manager, entretanto para manter a compatibilidade com a atual estrutura de dados os valores deste campo serão inseridos nas bases de dados de forma automática pois seus valores sempre foram os mesmos durante os 15 anos de operação do SciELO.

Issue
`````

Title
`````

1. Later Title 
  
  Será controlado automaticamente pelo campo "título anterior". Deve ser mantido na exportação para compatibilidade.

2. Center (v10)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade. Tem relação com o centro reponsável pela marcação de um documento.

3. Final Volume (v305)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

4. Final Number (v304)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

5. Alphabet (v340)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

6. Literature Type (v5)

  Excluído da aplicação. Deve ser cravado o valor "S" para manter compatibilidade.

7. Treatment Level (v6)

  Excluído da aplicação. Deve ser cravado o valor "Collective Level" para manter compatibilidade.

8. País de Publicação (v310)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade, esses dados são repetidos no campo address

9. Estado de Publicação (v320)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade, esses dados são repetidos no campo address

10. Cidade de Publicação (v490)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade, esses dados são repetidos no campo address

11. Classificação (v430)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

12. Número de identificação (v30)
  
  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

13. URL Site SciELO (v690)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

14. Rede SciELO (v691)

  Excluído da aplicação. Era utilizado como flag de coleções para processamento de geração de bases, 
  quando mais de uma coleção compartilha mesma base title no site local. Resolver este problema
  criando instalações independentes para cada coleção SciELO, ex: Brasil e Saúde Pública.

  Foram encontradas ocorrências do campo v691 no arquivo sci_serial.xis entretanto parece não estar
  em uso uma vez que faz referência a arquivos template (ScieloXML/collections.xis) que não estão 
  atualizados.


15. É suplemento de (v560)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

16. É suplemento de (v550)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

16. Código Medline (v420)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade. 

  Apenas 17 periódicos possuem este código hoje. Segue lista de referência para implementação futura
  deste campo::

    Anais da Academia Brasileira de Ciências - 45A
    Arquivos Brasileiros de Endocrinologia & Metabologia - 0403437
    Arquivos Brasileiros de Oftalmologia - 0400645
    Arquivos de Gastroenterologia - 8TR
    Brazilian Dental Journal  - 9214652
    Brazilian Journal of Medical and Biological Research - BOF
    Memórias do Instituto Oswaldo Cruz - MRY
    Physis: Revista de Saúde Coletiva - 9440484
    Revista Brasileira de Biologia - RGH 
    Revista Brasileira de Parasitologia Veterinária - 9440482
    Revista Gaúcha de Enfermagem - 15712799
    Revista Latino-Americana de Enfermagem - 9420934
    Revista da Associação M?dica Brasileira - BR5
    Revista da Sociedade Brasileira de Medicina Tropical - RET
    Revista do Hospital das Clínicas - S3L
    Revista do Instituto de Medicina Tropical de São Paulo - S9D
    São Paulo Medical Journal - SZ5

17. Título Abreviado Medline (v421)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade. Importado como other titles 
  para compor bibliometria e afins.

  Apenas 29 periódicos possuem este dado na base de dado. Segue lista de renferência para implementação
  futura deste campo::

    Anais da Academia Brasileira de Ciências - An Acad Bras Cienc
    Arquivos Brasileiros de Cardiologia - Arq Bras Cardiol
    Arquivos Brasileiros de Endocrinologia & Metabologia - Arq Bras Endocrinol Metabol. 
    Arquivos Brasileiros de Oftalmologia - Arq Bras Oftalmol.
    Arquivos de Gastroenterologia - Arq Gastroenterol
    Arquivos de Neuro-Psiquiatria - Arq Neuropsiquiatr
    Brazilian Dental Journal  - Braz Dent J
    Brazilian Journal of Biology - Braz J Biol.
    Brazilian Journal of Infectious Diseases - Braz J Infect Dis
    Brazilian Journal of Medical and Biological Research - Braz J Med Biol Res
    Brazilian Oral Research - Braz. oral res
    Cadernos de Saúde Pública - Cad Saude Publica
    Clinics - Clinics
    International braz j urol - int j urol
    Memórias do Instituto Oswaldo Cruz - Mem Inst Oswaldo Cruz
    Pesquisa Odontológica Brasileira - Pesqui Odontol Bras.
    Physis: Revista de Saúde Coletiva - Physis
    Revista Brasileira de Biologia - Rev Bras Biol
    Revista Brasileira de Parasitologia Veterinária - Rev Bras Parasitol Vet
    Revista Gaúcha de Enfermagem - Rev Gaucha Enferm.
    Revista Latino-Americana de Enfermagem - Rev Lat Am Enfermagem
    Revista da Associação Médica Brasileira - Rev Assoc Med Bras
    Revista da Sociedade Brasileira de Medicina Tropical - Rev Soc Bras Med Trop
    Revista de Saúde Pública - Rev Saude Publica
    Revista do Hospital das Clínicas - Rev. Hosp. Clin. Fac. Med. Univ. São Paulo
    Revista do Instituto de Medicina Tropical de São Paulo - Rev Inst Med Trop São Paulo
    São Paulo Medical Journal - São Paulo Med J

18. FTP (v66)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

19. Assinatura do usuário (v67)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

20. Seção (130)

  Excluído da aplicação. Não precisa ser mantido para compatibilidade. Nunca foi usado
