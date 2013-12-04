Middlewares
===========

ThreadLocalMiddleware
---------------------

Torna o objeto `request` visível por toda a aplicação, por meio de variável 
com *escopo de thread* (`threading.local`).

Para instalar, a linha à seguir deve ser incluída na diretiva `MIDDLEWARE_CLASSES`,
do arquivo `settings.py`:

   `scielomanager.utils.middlewares.threadlocal.ThreadLocalMiddleware`

À partir desse momento, o objeto `request` de qualquer requisição pode ser 
acessado por meio da função :func:`scielomanager.utils.middlewares.threadlocal.get_current_request` e,
o usuário corrente por meio da função :func:`scielomanager.utils.middlewares.threadlocal.get_current_user`.

Esse middleware viabiliza a operação do maquinário de obtenção do contexto da requisição do usuário
(:mod:`scielomanager.utils.usercontext`).

.. Note:: Thread local scope!
   Este middleware manipula o scopo global da `thread` ativa, fazendo uso do nome 
   `_request`. 

