#!/usr/local/bin/thrift --py
# Copyright (c) 2012, SciELO <scielo-dev@googlegroups.com>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
# 
#     Redistributions of source code must retain the above copyright notice,
#     this list of conditions and the following disclaimer.
# 
#     Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions and the following disclaimer in the documentation
#     and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,
# INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY,
# WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY
# OF SUCH DAMAGE.

namespace java org.scielo.scielomanager.thrift
namespace py scielomanager


/*
 * IMPORTANTE! Alterar o valor de VERSION após qualquer alteração na interface.
 * Regras em: http://semver.org/lang/pt-BR/
 */
const string VERSION = "1.3.0"


#
# Exceções
#

/* Levantada sempre que um erro inesperado ocorre no servidor. */
exception ServerError {
}

/* Ocorre quando há algum problema com o valor passado como argumento. */
exception BadRequestError {
    1: optional string message;
}

/* A operação foi abortada pois o tempo excedeu na comunicação com o backend. */
exception TimeoutError {
}

/*
 * Representa a relação entre artigos.
 *
 * Esta relação é comumente estabelecida entre artigos e suas erratas, onde 
 * o campo `type` leva o valor `correction`.
 */
struct RelatedArticle {
    1: required string aid;
    2: optional string type;
}

/*
 * Article representa um documento XML em conformidade com a especificação 
 * SciELO-PS, em qualquer uma das versões, ou pré-sps para os documentos 
 * mais antigos.
 * 
 * O campo `timestamp` é produzido pelo SciELO Manager e representa a data
 * de modificação do registro.
 */
struct Article {
    1: optional string abbrev_journal_title;
    2: optional string epub;
    3: optional string ppub;
    4: optional string volume;
    5: optional string issue;
    6: optional string year;
    7: optional string doi;
    8: optional string pid;
    9: required string aid;
    10: optional string head_subject;
    11: required string article_type;
    12: required string version;
    13: optional bool is_aop;
    14: required string source;
    15: optional string timestamp;
    16: optional list<RelatedArticle> links_to;
    17: optional list<RelatedArticle> referrers;
}

/*
 * ScanArticlesResults representa um lote de entidades Article, retornado 
 * após uma consulta por meio da função ScanArticles.
 */
struct ScanArticlesResults {
    1: optional list<Article> articles;
    2: optional string next_batch_id;
}

/*
 * ResultStatus representa o status da execução de uma tarefa assíncrona.
 *
 * Os valores possíveis são:
 *  - PENDING: A tarefa ainda não foi executada.
 *  - STARTED: A tarefa está em execução.
 *  - RETRY: A execução da tarefa falhou, e uma nova tentativa está agendada.
 *  - FAILURE: A execução da tarefa falhou definitivamente.
 *  - SUCCESS: A tarefa foi executada com sucesso.
 */
enum ResultStatus {
    PENDING,
    STARTED,
    RETRY,
    FAILURE,
    SUCCESS
}

/*
 * AsyncResult representa o resultado da execução de uma tarefa assíncrona.
 */
struct AsyncResult {
    1: ResultStatus status;
    2: string value;                  // string codificada em json
}


service JournalManagerServices {
    /*
     * Adiciona uma nova entidade tipo Article, com base no seu doc XML.
     *
     * Retorna string `task_id` correspondente ao identificador da tarefa
     * criada. `task_id` deve ser utilizada para obter o resultado da função. 
     */
    string addArticle(1:string xml_string) throws (1:ServerError srv_err);

    /*
     * Consulta o resultado da execução de uma determinada tarefa assíncrona.
     */
    AsyncResult getTaskResult(1:string task_id) throws (1:ServerError srv_err); 

    /*
     * Realiza consulta em entidades do tipo `Article`.
     *
     * A consulta deve ser expressa utilizando a sintaxe `Query DSL` do 
     * Elasticsearch (http://bit.ly/1I9g37B). Os resultados não são ordenados
     * por relevância.
     *
     * Retorna string `batch_id` correspondente ao primeiro lote de resultados
     * que devem ser recuperados utilizando a função `getScanArticlesBatch`.
     */
    string scanArticles(1:string es_dsl_query) throws (1:ServerError srv_err, 
            2:BadRequestError req_err, 3:TimeoutError tou_err); 

    /*
     * Obtém lote de resultados de consulta.
     *
     * Os resultados são representados por structs `ScanArticlesResults`. O 
     * campo `next_batch_id` apresenta o identificador do próximo lote.
     */
    ScanArticlesResults getScanArticlesBatch(1:string batch_id) throws (
            1:ServerError srv_err, 2:BadRequestError req_err, 
            3:TimeoutError tou_err); 


    #
    # Meta-API
    #    

    /*
     * Obtém a versão da interface Thrift do servidor.
     */
    string getInterfaceVersion();
}

