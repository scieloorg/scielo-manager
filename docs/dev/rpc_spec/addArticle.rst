.. _func-addArticle:

``string addArticle(1:string xml_string, 2:bool overwrite) throws (1:ServerError srv_err);``
============================================================================================

Cadastra uma nova entidade ``journalmanager.models.Article``. 


Resumo
------

O sistema deve permitir que essas entidades sejam cadastradas de maneira programática, por softwares do 
fluxo de ingestão. 

A função deve ser assíncrona, a fim de que o serviço seja resiliente e atenda um número 
arbitrário de requisições com tempo de resposta virtualmente constante. O resultado 
da sua execução deve ser consultado por meio do uso do identificador ``task_id``. 
Ver documentação da função :ref:`func-getTaskResult`.

Os resultados possíveis são:

+----------------------------------------+-------------------------------------------------------------+
| Estado                                 | Objeto retornado                                            |
+========================================+=============================================================+
| A função está pendente de execução     | AsyncResult(status=PENDING, value='')                       | 
+----------------------------------------+-------------------------------------------------------------+
| A função está em execução              | AsyncResult(status=STARTED, value='')                       |
+----------------------------------------+-------------------------------------------------------------+
| A função falhou e está aguardando nova | AsyncResult(status=RETRY, value='')                         |
| execução                               |                                                             |
+----------------------------------------+-------------------------------------------------------------+
| A função falhou definitivamente        | AsyncResult(status=FAILURE, value='[errno, "err_message"]') |
+----------------------------------------+-------------------------------------------------------------+
| A função foi executada com sucesso     | AsyncResult(status=SUCCESS, value='article_id')             |
+----------------------------------------+-------------------------------------------------------------+


No caso de resultados com status ``FAILURE``, os valores para ``errno`` são:

+-------+------------------+----------------------------------------------------------+
| errno | Tipo             | Descrição                                                |
+=======+==================+==========================================================+
| 1     | DuplicationError | O artigo representado por ``xml_string`` já havia sido   |
|       |                  | adicionado anteriormente                                 |
+-------+------------------+----------------------------------------------------------+
| 2     | ValueError       | ``xml_string`` é mal-formado ou apresenta algum problema |
|       |                  | estrutural que impeça sua identificação                  |
+-------+------------------+----------------------------------------------------------+


.. note:: Erros do tipo ``DuplicationError`` ocorrem apenas em invocações cujo 
          valor do argumento ``overwrite`` é igual a ``FALSE``. Caso o valor 
          seja ``TRUE``, a entidade pré-existente será substituída de maneira 
          permanente.


Os elementos de identificação são: 

  Para identificar o periódico e número:

    * ``//journal-meta/journal-title-group/journal-title``
    * ``//journal-meta/issn[@pub-type="ppub"]``
    * ``//journal-meta/issn[@pub-type="epub"]``
    * ``//article-meta/volume``
    * ``//article-meta/issue``
    * ``//article-meta/pub-date/year``

  Para identificar o artigo (duplicidade):

    Devem ser concatenados os campos abaixo seguindo a ordem.

    * ``//journal-meta/journal-title-group/journal-title``
    * ``//article-meta/volume``
    * ``//article-meta/issue``
    * ``//article-meta/pub-date/year``
    * ``//article-meta/fpage``
    * ``//article-meta/lpage``
    * ``//article-meta/elocation-id``


A associação da entidade com ``journalmanager.models.Issue`` também deve ser 
realizada de maneira assíncrona. Entidades órfãs (desassociadas) são permitidas 
e periódicamente são resubmetidas ao processo de associação.

