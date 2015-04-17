Diretório de configurações
==========================

Este diretório conta com uma quantidade arbitrária de arquivos de configuração 
que serão carregados pelo módulo `scielomanager.settings`.

* Cada arquivo de configuração deve ser um módulo Python, sintaticamente válido,
  utilizando a extensão `.conf`. 
* Os arquivos serão carregados em ordem alfabética.


Opcionalmente, o último arquivo a ser carregado pode ser especificado por meio 
da variável de ambiente `SCIELOMANAGER_SETTINGS_FILE`. Este arquivo deve, 
obrigatoriamente, estar alocado fora da estrutura de arquivos do pacote da 
aplicação.

