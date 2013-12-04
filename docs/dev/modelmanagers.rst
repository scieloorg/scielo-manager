Model Managers
==============

São objetos capazes de produzir querysets de tipos de entidades
com base em filtros e restrições pré definidas.


UserObjectManager
-----------------

Módulo: :mod:`scielomanager.journalmanager.modelmanagers`

São *model managers* atrelados ao contexto do usuário ativo, e só devem 
ser utilizados durante o ciclo de vida de `request/response`.

O seu objetivo é de facilitar a realização de consultas ao banco de 
dados respeitando as restrições de acesso em que o usuário ativo 
está sujeito, e aumentar a expressividade sintática das consultas.

Cada objeto de modelo cujo acesso pelo usuário deve estar condicionado
às regras de visibilidade da aplicação, por exemplo a coleção ativa,
deve prover um `model manager` chamado `userobjects`, de acordo com o 
seguinte protocolo:

Subclasse de ``models.Manager``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``get_query_set`` Retorna uma subclasse de `models.query.QuerySet`
* ``all`` Retorna todos os objetos acessíveis pelo usuário ativo
* ``active`` Retorna um subconjunto de ``all``, apenas com os objetos
  da coleção ativa

Subclasse de ``models.query.QuerySet``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* ``all`` Retorna todos os objetos acessíveis pelo usuário ativo
* ``active`` Retorna todos os objetos da coleção ativa
* ``startswith`` (opcional) Retorna todos os objetos cujo primeiro 
  caractere casa com o especificado. É útil para classificação de 
  listas e necessidades de apresentação
* ``simple_search`` (opcional) Realiza uma pesquisa simples em 1 ou mais 
  campos. Aceita apenas 1 string como termo de busca.
* ``available`` Retorna todos os objetos não marcados como excluídos 
  (`is_trashed=False`)
* ``unavailable`` Retorna todos os objetos marcados como excluídos
  (`is_trashed=True`)

