.. _func-getScanArticlesBatch:

``scanResults getScanArticlesBatch(1:string batch_id) throws (1:ServerError srv_err, 2:BadRequestError req_err, 3:TimeoutError tou_err);``
==========================================================================================================================================


Retorna a struct ``ScanArticlesResults`` representando o lote identificado 
por *batch_id*. A struct contém dois campos: 1) next_batch_id - que é o 
identificador para a obtenção do próximo lote e 2) articles - a lista de 
``Article``. 

A responsabilidade de saber o momento de parar de solicitar por novos lotes é 
do cliente. O serviço sempre retornará valores para ''next_batch_id'', mesmo 
que não haja mais resultado.


Exemplo:: 

    def get_articles(year):
        batch_id = client.scanArticles(
                '{"query": {"match": {"year": %s}}, "size": 50}' % year)

        while True:
            result = client.getScanArticlesBatch(batch_id)

            if not result.articles:
                return

            for article in result.articles:
                yield article

            batch_id = result.next_batch_id


.. note:: A lista de resultados de um lote não é ordenada por data ou qualquer 
          campo. 
