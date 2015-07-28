# coding: utf-8
"""Exceções do pacote `connectors`.

O dicionário `translations` contém traduções de códigos de erro HTTP,
utilizados pela interface Restful do Elasticsearch, para as definidas
localmente.
"""


class BaseConnectorError(Exception):
    """Base para exceções do pacote `connectors`.
    """


class BadRequestError(BaseConnectorError):
    """Erro no conjunto de argumentos enviado ao servidor.
    """


class NotFoundError(BaseConnectorError):
    """O registro solicitado não existe.
    """


class TimeoutError(BaseConnectorError):
    """Tempo de conexão excedido.
    """


class ServerError(BaseConnectorError):
    """Algo ruim aconteceu no servidor.
    """


translations = {
        400: BadRequestError,
        404: NotFoundError,
        408: TimeoutError,
        500: ServerError,
        501: ServerError,
        502: ServerError,
        503: ServerError,
        504: ServerError,
        506: ServerError,
}

