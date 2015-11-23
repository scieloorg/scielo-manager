# coding: utf-8
"""
Interface do connector tipo `Storage`:
    - add(id: str, data: dict)
    - get(id: str) -> dict
    - scan(query: str) -> str
    - scroll(scroll_id: str) -> (str, list)
"""
import os
import logging
import functools

import elasticsearch

from .. import tools
from . import exceptions


__all__ = ['ArticleElasticsearch']


LOGGER = logging.getLogger(__name__)
# Consumo de memória com XML (aprox): ES_RESULTS_PER_SHARD * total_shards * 200KB
# i.e., 10MB por lote (atualmente com 5 shards).
ES_RESULTS_PER_SHARD = '10'
ES_SCROLL_TIMEOUT = '30s'
ES_NODES = tools.get_setting_or_raise('ELASTICSEARCH_NODES')
ES_ARTICLE_INDEX_NAME = tools.get_setting_or_raise('ES_ARTICLE_INDEX_NAME')
ES_ARTICLE_DOC_TYPE = tools.get_setting_or_raise('ES_ARTICLE_DOC_TYPE')

_CWD = os.path.dirname(os.path.abspath(__file__))
ES_ARTICLE_MAPPING_PATH = os.path.join(_CWD, 'article_mapping.json')


def _get_article_mapping():
    with open(ES_ARTICLE_MAPPING_PATH, 'r') as mapping_file:
        mapping_data = mapping_file.read()

    return mapping_data


def translate_exceptions(wrapped):
    """Traduz exceções das dependências internas do pacote, para as que
    fazem parte da sua API.
    """
    @functools.wraps(wrapped)
    def _wrapper(*args, **kwargs):
        try:
            return wrapped(*args, **kwargs)
        except elasticsearch.exceptions.TransportError as exc:
            # Caso não haja exceção mapeada para esse caso, será levantada a
            # exceção mais genérica: BaseConnectorError.
            new_exception = exceptions.translations.get(
                    exc.status_code, exceptions.BaseConnectorError)
            raise new_exception(exc.message)

    return _wrapper


def ArticleElasticsearch():
    """Fábrica de connectores do Elasticsearch para entidades `article`.

    O cliente é pré-configurado de acordo com as diretivas definidas na
    configuração do projeto.

    As diretivas são:
      - ELASTICSEARCH_NODES
      - ES_ARTICLE_INDEX_NAME
      - ES_ARTICLE_DOC_TYPE
    """
    if not hasattr(ArticleElasticsearch, '_cached_client'):
        ArticleElasticsearch._cached_client = elasticsearch.Elasticsearch(ES_NODES)

    return _Elasticsearch(ArticleElasticsearch._cached_client,
            ES_ARTICLE_INDEX_NAME, ES_ARTICLE_DOC_TYPE)


class _Elasticsearch(object):
    """Adapta a interface de `elasticsearch.Elasticsearch`.
    """
    def __init__(self, es_client, index, doctype):
        self.es_client = es_client
        self.index = index
        self.doctype = doctype

    def __repr__(self):
        return u'<%s es_client=%s index=%s doctype=%s>' % (
                self.__class__.__name__, self.es_client, self.index,
                self.doctype)

    @translate_exceptions
    def add(self, id, data):
        """Armazena `data` sob o identificador `id`.

        Registros serão sobrescritos caso `id` corresponda a um registro já
        armazenado.
        """
        _ = self.es_client.index(index=self.index, doc_type=self.doctype,
                id=id, body=data)

    def get(self, id):
        return NotImplemented

    @translate_exceptions
    def scan(self, query):
        """Consulta expressão definida por `query`.

        Esse método é otimizado para a recuperação de grandes quantidades de
        dados, portanto: 1) a ordenação dos resultados por relevância é
        desabilitada e 2) os resultados devem ser recuperados por lotes.
        """
        resp = self.es_client.search(body=query, scroll=ES_SCROLL_TIMEOUT,
                search_type='scan', index=self.index, doc_type=self.doctype,
                size=ES_RESULTS_PER_SHARD)

        return resp.get('_scroll_id')

    @translate_exceptions
    def scroll(self, scroll_id):
        """Recupera lote identificado por `scroll_id`.

        Retorna um tupla contendo o `scroll_id` do próximo lote e a lista de
        resultados. Lotes podem conter zero resultado, e a decisão de parar
        de pedir por novos lotes deve ser do consumidor.
        """
        resp = self.es_client.scroll(scroll_id, scroll=ES_SCROLL_TIMEOUT)

        results = []
        for result in resp.get('hits', {}).get('hits', []):
            try:
                source = result['_source']
            except KeyError:
                LOGGER.warning('Cannot find field "_source" in record "%s"',
                        result['_id'])
            else:
                results.append(source)

        return resp.get('_scroll_id'), results

    @translate_exceptions
    def delete_index(self):
        """Remove o índice `self.index`.

        Atenção: Além do índice, o mapping e todos os registros serão removidos!
        """
        _ = self.es_client.indices.delete(index=self.index)

    @translate_exceptions
    def create_index(self):
        """Cria o índice `self.index`.
        """
        mapping_data = _get_article_mapping()

        _ = self.es_client.indices.create(index=self.index, body=mapping_data)

