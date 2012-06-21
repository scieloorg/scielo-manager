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

As bases de dados ISIS geradas pelo Title Manager são utilizadas em dois prontos do processo de publicação da SciELO, são eles: processo de marcação e processamento para inclusão de conteúdo.

Processamento para inclusão de conteúdo
=======================================

Atualmente o SciELO possui um processamento (geraPadrao.bat) para inclusão de novas revistas, fascículos e artigos na coleção. Esse processamento recebe como entrada um conjunto de bases de dados, são elas: artigo, issue, code, title.

As bases code, title e issue são únicadas para todo o processamento, significa que uma base de dados com todo o conteúdo de título, outra com todo conteúdo de code e outra com todo conteúdo de issues são geradas e gravadas em um diretório chamado serial gerando a seguinte estrutura de dados de entrada para o processamento.

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

O processo de marcação de metadados de artigos nas SciELO é feito através da ferramenta Markup, que corresponde a um aplicativo VBSript embutido no Word para identificar os elementos dos artigos. Esse plugin do Word consulta algumas bases de dados ISIS geradas pela Title Manager para complementar a identificação de elementos no texto do artigo, como por exemplo:

* Identificação de seções dos fascículos (base code)

A exportação de dados da ferramenta SciELO Manager deve gerar as bases de dados utilizadas pelo Markup e gravá-las seguindo a seguinte extrutura de dados.

.. code-block:: text

 /serial
 /serial/code
 /serial/code/newcode.mst
 /serial/code/newcode.xrf

Em resumo, significa que o processo de exportação de bases do SciELO Manager para ISIS deve gerar essa estrutura de arquivos como entrada para o processo de marcação. Mais a frente será tratada a estrutura de dados dessas bases de dados.

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

Artigo
``````

Code
````

Remoção de Campos desnecessários
================================

De acordo com reunião realizada em 27 de março alguns campos no contexto da SciELO não serão mais cosiderados pelo SciELO Manager, entretanto para manter a compatibilidade com a atual estrutura de dados os valores deste campo serão inseridos nas bases de dados de forma automática pois seus valores sempre foram os mesmos durante os 15 anos de operação do SciELO.

1. Later Title
  
  Será controlado automaticamente pelo campo "título anterior". Deve ser mantido na exportação para compatibilidade.

2. Center

  Excluído da aplicação. Não precisa ser mantido para compatibilidade. Tem relação com o centro reponsável pela marcação de um documento.

3. Final Volume

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

4. Final Number

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

5. Alphabet

  Excluído da aplicação. Não precisa ser mantido para compatibilidade.

6. National Code

  Excluído da aplicação. Deve ser mantido na exportação para compatibilidade. Exemplo: BR1.1
  Deve ser parametrizado na exportação.

7. Literature Type

  Excluído da aplicação. Deve ser cravado o valor "S" para manter compatibilidade.

8. Treatment Level

  Excluído da aplicação. Deve ser cravado o valor "Collective Level" para manter compatibilidade.
