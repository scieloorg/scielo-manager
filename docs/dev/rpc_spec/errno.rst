.. _errno:

Números do sistema de erros
===========================

Espaço de nomes para a representação dos diferentes tipos de erro, que podem 
ocorrer durante a execução das tarefas assíncronas, na estrutura retornada pela 
função ``getTaskResult``. 


Resumo
------

A função ``getTaskResult`` retorna o resultado de uma tarefa assíncrona 
representada por uma struct contendo os campos *status* e *value*. Exceções 
são representadas pelo *status* ``FAILURE`` e *value* ``[errno, mensagem]``. 
``errno`` é um número inteiro que representa o tipo da exceção.

Os valores para ``errno`` são:

+-------+------------------+----------------------------------------------------------+
| errno | Tipo             | Descrição                                                |
+=======+==================+==========================================================+
| 1     | DuplicationError | A entidade não pôde ser criada pois já existe um registro|
|       |                  | com a mesma chave única.                                 |
+-------+------------------+----------------------------------------------------------+
| 2     | ValueError       | O valor passado por argumento causou um erro na execução |
|       |                  | da tarefa.                                               |
+-------+------------------+----------------------------------------------------------+


