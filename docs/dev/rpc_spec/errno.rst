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
| 1     | DuplicationError | O artigo representado por ``xml_string`` já havia sido   |
|       |                  | adicionado anteriormente                                 |
+-------+------------------+----------------------------------------------------------+
| 2     | ValueError       | ``xml_string`` é mal-formado ou apresenta algum problema |
|       |                  | estrutural que impeça sua identificação                  |
+-------+------------------+----------------------------------------------------------+


