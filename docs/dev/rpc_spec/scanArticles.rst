.. _func-scanArticles:

``string scanArticles(1:string es_dsl_query) throws (1:ServerError srv_err, 2:BadRequestError req_err, 3:TimeoutError tou_err);``
=================================================================================================================================


Realiza consulta nos registros do tipo de ``journalmanager.models.Article``, 
fazendo uso da DSL do Elasticsearch, e retorna identificador para o primeiro 
lote de resultados.

Os índices que podem ser utilizados na consulta são:

+----------------------+------------------------------------------------------+
| Índice               | Descrição                                            |
+======================+======================================================+
| abbrev_journal_title | Título abreviado do periódico conforme ISSN.         |
+----------------------+------------------------------------------------------+
| epub                 | ISSN eletrônico do periódico.                        |
+----------------------+------------------------------------------------------+
| ppub                 | ISSN impresso do periódico.                          |
+----------------------+------------------------------------------------------+
| volume               | Identificador de volume do fascículo o qual o artigo | 
|                      | é parte.                                             |
+----------------------+------------------------------------------------------+
| issue                | Identificador do fascículo o qual o artigo é parte.  |
+----------------------+------------------------------------------------------+
| year                 | Ano de publicação.                                   |
+----------------------+------------------------------------------------------+
| doi                  | Digital Object Identifier.                           |
+----------------------+------------------------------------------------------+
| pid                  | Identificador único de artigo (legado).              |
+----------------------+------------------------------------------------------+
| aid                  | Article Id (identificador único atual).              |
+----------------------+------------------------------------------------------+
| head_subject         | Seção do fascículo a qual o artigo é parte.          |
+----------------------+------------------------------------------------------+
| article_type         | O tipo do documento conforme consta no doc XML.      |                     
+----------------------+------------------------------------------------------+
| version              | A versão da especificação SciELO PS.                 |
+----------------------+------------------------------------------------------+
| is_aop               | Se o artigo é `ahead of print`.                      |
+----------------------+------------------------------------------------------+
| source               | O documento XML codificado em utf-8.                 |
+----------------------+------------------------------------------------------+


.. note:: A quantidade de registros por lote não é definida pelo cliente, e 
          sim pelo servidor, a fim de manter a saúde dos serviços.


Exemplo::

    batch_id = client.scanArticles('{"query": {"match": {"year": "2013"}}}')
    next_batch_id, articles = client.getScanArticlesBatch(batch_id)

    for article in articles:
        ...

