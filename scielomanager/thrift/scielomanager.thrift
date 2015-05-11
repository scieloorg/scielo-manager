/*
 * Exceções.
 *
 * ServerError é levantada sempre que um erro inesperado ocorre no servidor. 
 * Equivale aos erros da classe 5xx do protocolo HTTP.
 */
exception ServerError {
    1: string message;
}

exception DuplicationError {
    1: string message;
}

exception ValueError {
    1: string message;
}

/*
 * Manuseio de requisições assíncronas.
 */
enum ResultStatus {
    PENDING,
    STARTED,
    RETRY,
    FAILURE,
    SUCCESS
}

struct AsyncResult {
    1: ResultStatus status;
    2: string value;                  // string codificada em json
}

/*
 * Protótipo dos serviços.
 */
service JournalManagerServices {
    /*
     * Funções assíncronas. 
     *
     * Retorna string `task_id` correspondente ao identificador da tarefa
     * criada. `task_id` deve ser utilizada para obter o resultado da função. 
     */
    string addArticle(1:string xml_string, 2:bool raw) throws (
        1:ServerError srv_err);

    /*
     * Funções síncronas - seja bacana e utilize suas versões assíncronas 
     * quando disponíveis.
     */
    AsyncResult getTaskResult(1:string task_id) throws (1:ServerError srv_err); 
}

