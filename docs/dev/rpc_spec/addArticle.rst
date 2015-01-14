``string addArticle(1:string xml_string) throws (1:DuplicationError dup_err, 2:ValueError val_err);``
=====================================================================================================

Cadastra uma nova entidade ``journalmanager.models.Article``. 


Resumo
------

O sistema deve permitir que essas entidades sejam cadastradas de maneira programática, por softwares do 
fluxo de ingestão. 

Essa função deve ser consistente, i.e. deve retornar o identificador do registro no caso
de sucesso ou levantar uma exceção no caso contrário. Em chamadas sucessivas, apenas a 
primeira deve retornar o identificador do registro, as demais devem levantar ``DuplicationError``.

Caso o valor de ``xml_string`` seja mal-formado ou apresente algum problema estrutural que impeça sua 
identificação, a exceção ``ValueError`` é levantada. Os elementos de identificação são: 

  Para identificar o periódico e número:

    * ``//journal-meta/journal-title-group/abbrev-journal-title[@abbrev-type="publisher"]``
    * ``//article-meta/volume``
    * ``//article-meta/issue``
    * ``//article-meta/pub-date/year``

  Para identificar o artigo (duplicidade):

    Devem ser concatenados os campos abaixo seguindo a ordem.

    * ``//article-meta/title-group/article-title``
    * ``//article-meta/contrib-group/contrib[@contrib-type="author" or 
                                             @contrib-type="compiler" or 
                                             @contrib-type="editor" or 
                                             @contrib-type="translator"]/name[1]/surname``
    * ``//article-meta/pub-date/year``


A associação da entidade com ``journalmanager.models.Issue`` deve ser realizada de maneira
assíncrona, a fim de aumentar a capacidade de atendimento de requisições do sistema. 
Entidades órfãs (desassociadas) são permitidas e periódicamente são resubmetidas ao processo de 
associação.


Casos de uso
------------

* O *Conversor XML* deve armazenar os XML SciELO PS crus no SciELO Manager
* O conteúdo legado das coleções SciELO (carregados inicialmente pelo fluxo 
  antigo) deve ser transformado em XML SciELO PS e carregado no SciELO Manager
* O sistema de ingestão de artigos (Balaio) deve carregar um XML SciELO PS 
  no SciELO Manager após a aprovação da equipe de QA

