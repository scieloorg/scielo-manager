.. _func-addArticleAsset:

``void addArticleAsset(1:string aid, 2:string filename, 3:binary content, 4:ArticleAssetMeta meta) throws (1:ServerError srv_err);``
====================================================================================================================================

Cadastra uma nova entidade ``journalmanager.models.ArticleAsset``, vinculada à 
instância de ``journalmanager.models.Article`` definida pelo argumento ``aid``. 


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
| A função foi executada com sucesso     | AsyncResult(status=SUCCESS, value='asset_url')              |
+----------------------------------------+-------------------------------------------------------------+


No caso de resultados com status ``FAILURE``, os valores para ``errno`` são:

+-------+------------------+----------------------------------------------------------+
| errno | Tipo             | Descrição                                                |
+=======+==================+==========================================================+
| 2     | ValueError       | ``aid`` não corresponde a uma instância de               |
|       |                  | ``journalmanager.models.Article``.                       |
+-------+------------------+----------------------------------------------------------+

