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
const string VERSION = "2.1.0"


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

/* Recurso requerido não existe. */
exception DoesNotExist {
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
 * Collection representa um conjunto de metadados de um periódico. Os dados são
 * compatíveis com o modelo de dados definidos em models.py entretanto apenas
 * alguns metadados estão disponíveis.
 *
 */

struct Collection {
    1: optional i64 id;
    2: required string name;
    3: optional string name_slug;
    4: optional string url;
    5: required string acronym;
    6: optional string country;
    7: optional string state;
    8: optional string city;
    9: optional string address;
    10: optional string address_number;
    11: optional string address_complement;
    12: optional string zip_code;
    13: optional string phone;
    14: optional string fax;
    15: optional string email;
    16: optional list<i64> journals;
}

struct UseLicense {
    1: required string license_code;
    2: optional string reference_url;
    3: optional string disclaimer;
    4: required bool is_default;
}

struct JournalMission {
    1: optional string language;
    2: optional string description;
}

struct JournalTimeline {
    1: required string since;
    2: required string status;
    3: optional string reason;
}

/*
 * Journal representa um conjunto de metadados de um periódico. Os dados são
 * compatíveis com o modelo de dados definidos em models.py entretanto apenas
 * alguns metadados estão disponíveis.
 *
 */

struct Journal {
    1: optional i64 id;
    2: required string title;
    3: required string title_iso;
    4: optional string short_title;
    5: optional string medline_title;
    6: optional string medline_code;
    7: optional string twitter_user;
    8: required list<string> study_areas;
    9: required list<string> subject_categories;
    10: required UseLicense use_license;
    11: optional string created;
    12: optional string updated;
    13: required string acronym;
    14: required string scielo_issn;
    15: optional string print_issn;
    16: optional string electronic_issn;
    17: optional string frequency;
    18: optional string copyrighter;
    19: optional string url_online_submission;
    20: optional string url_journal;
    21: optional string notes;
    22: optional bool is_trashed;
    23: optional bool is_indexed_scie;
    24: optional bool is_indexed_ssci;
    25: optional bool is_indexed_aehci;
    26: optional list<JournalMission> missions;
    27: optional list<i64> issues;
    28: optional list<i64> collections;
    29: optional list<JournalTimeline> timeline;
}

/*
 * EditorialBoardMember representa os dados de um membro de um corpo editorial. 
 * Os dados são compatíveis com o modelo de dados definidos em models.py
 * entretanto apenas alguns metadados estão disponíveis através.
 *
 */

struct EditorialBoardMember {
    1: optional string first_name;
    2: optional string last_name;
    3: optional string city;
    4: optional string country;
    5: optional string state;
    6: optional string email;
    7: optional string research_id;
    8: optional string orcid;
    9: optional string link_cv;
    10: optional string role;
    11: optional i64 order;
    12: optional string institution;
}

/*
 * IssueTitle representa o título de um fascículo em um idioma específico. Os
 * dados são compatíveis com o modelo de dados definidos em models.py entretanto
 * apenas alguns metadados estão disponíveis através.
 *
 */

struct IssueTitle {
    1: optional string language;
    2: optional string title;
}

/*
 * Issue representa um conjunto de metadados de um fascículo. Os dados são
 * compatíveis com o modelo de dados definidos em models.py entretanto apenas
 * alguns metadados estão disponíveis.
 *
 */

 struct Issue {
    1: optional i64 id;
    2: optional Journal journal;
    3: optional string volume;
    4: optional string number;
    5: optional string created;
    6: optional string updated;
    7: optional i64 publication_start_month;
    8: optional i64 publication_end_month;
    9: optional i64 publication_year;
    10: optional string publication_date;
    11: optional UseLicense use_license;
    12: optional string label;
    13: optional i64 order;
    14: required string type;
    15: optional string suppl_text;
    16: optional string spe_text;
    17: optional string identification;
    18: optional list<IssueTitle> issue_title;
    19: optional list<i64> articles;
    20: optional list<EditorialBoardMember> editorial_board;
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

/*
 * ArticleAssetMeta representa metadados associados ao ativo digital, como 
 * informação de licenciamento por exemplo.
 */
struct ArticleAssetMeta {
    1: optional string owner;
    2: optional string use_license;
}


service JournalManagerServices {
    /*
     * Adiciona uma nova entidade tipo Article, com base no seu doc XML.
     *
     * Retorna string `task_id` correspondente ao identificador da tarefa
     * criada. `task_id` deve ser utilizada para obter o resultado da função. 
     */
    string addArticle(1:string xml_string, 2:bool overwrite) throws (
            1:ServerError srv_err);

    /*
     * Adiciona um novo ativo digital, vinculado a uma entidade Article.
     *
     * Retorna string `task_id` correspondente ao identificador da tarefa
     * criada. `task_id` deve ser utilizada para obter o resultado da função. 
     */
    string addArticleAsset(1:string aid, 2:string filename, 3:binary content, 
            4:ArticleAssetMeta meta) throws (1:ServerError srv_err);

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
            1:ServerError srv_err, 2:BadRequestError req_err); 


    #
    # Meta-API
    #    

    /*
     * Obtém a versão da interface Thrift do servidor.
     */
    string getInterfaceVersion();

    /*
     * Obtém metadados de periódicos.
     *
     * Os resultados são representados pela struct `Journal`.
     *
     */

    Journal getJournal(1:i64 journal_id, 2: optional i64 collection_id) throws (1:ServerError srv_err,
            2:BadRequestError req_err, 3:DoesNotExist match_err);

    /*
     * Obtém metadados de fascículos.
     *
     * Os resultados são representados pela struct `Issue`.
     *
     */

    Issue getIssue(1:i64 issue_id) throws (1:ServerError srv_err,
            2:BadRequestError req_err, 3:DoesNotExist match_err);

    /*
     * Obtém metadados de fascículos.
     *
     * Os resultados são representados pela struct `Issue`.
     *
     */

    Collection getCollection(1:i64 collection_id) throws (1:ServerError srv_err,
            2:BadRequestError req_err, 3:DoesNotExist match_err);

    /*
     * Obtém lista de periódicos de uma coleção ou de todo o catálogo.
     *
     * Os resultados são representados por uma lista instâncias de struct
     * `Journal`.
     *
     */

    list<Journal> getJournals(1: optional i64 collection_id, 2: optional string from_date, 3: optional string until_date, 4: i32 limit, 5: i32 offset)  throws (1:ServerError srv_err, 2:BadRequestError req_err)

    /*
     * Obtém lista de fascículos de um periódico ou de todo o catálogo.
     *
     * Os resultados são representados por uma lista instâncias de struct
     * `Issue`.
     *
     */

    list<Issue> getIssues(1: optional i64 journal_id, 2: optional string from_date, 3: optional string until_date, 4: i32 limit, 5: i32 offset)  throws (1:ServerError srv_err, 2:BadRequestError req_err)

    /*
     * Obtém lista de coleções do catálogo.
     *
     * Os resultados são representados por uma lista instâncias de struct
     * `Collection`.
     *
     */

    list<Collection> getCollections(1: optional string from_date, 2: optional string until_date, 3: i32 limit, 4: i32 offset)  throws (1:ServerError srv_err, 2:BadRequestError req_err)
}
