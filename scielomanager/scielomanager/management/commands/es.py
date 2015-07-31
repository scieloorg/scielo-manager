# coding: utf-8
"""Tarefas de manutenção da integração com o Elasticsearch.
"""
from django.core.management.base import BaseCommand, CommandError
import elasticsearch

from scielomanager import connectors


_TYPE_CLIENT_MAP = {
        'article': connectors.ArticleElasticsearch,
}


_HELP = u"""\
Executa tarefas de manutenção da integração com o Elasticsearch.

Os comandos são:
    putmapping <type>     Adiciona ou atualiza o mapping de um tipo.
    createindex <type>    Cria o índice e define o mapping do tipo.

Os valores de <type> são:
    %s
""" % (_TYPE_CLIENT_MAP.keys(),)


def _to_bytestring(text):
    return text.encode('utf-8')


def _get_article_mapping():
    with open(connectors.ES_ARTICLE_MAPPING_PATH, 'r') as mapping_file:
        mapping_data = mapping_file.read()

    return mapping_data


def _put_mapping(type):
    """
    """
    client_cls = _TYPE_CLIENT_MAP.get(type)
    if client_cls is None:
        raise CommandError(
                _to_bytestring(u'"%s" não é um tipo válido' % type))

    client = client_cls()
    mapping_data = _get_article_mapping()

    client.es_client.indices.put_mapping(index=client.index,
            doc_type=client.doctype, body=mapping_data, ignore_conflicts=False,
            timeout=2)


def _create_index(type):
    client_cls = _TYPE_CLIENT_MAP.get(type)
    if client_cls is None:
        raise CommandError(
                _to_bytestring(u'"%s" não é um tipo válido' % type))

    client = client_cls()

    client.es_client.indices.create(index=client.index, timeout=2)
    _put_mapping(type)


class Command(BaseCommand):
    args = '<command> [<args>]'
    help = _HELP
    requires_model_validation = False

    def handle(self, *args, **options):
        if not args:
            raise CommandError(
                    _to_bytestring("'./manage.py help es' para ajuda."))

        command = args[0]
        arguments = args[1:]

        try:
            if command == 'putmapping':
                _put_mapping(*arguments)
            elif command == 'createindex':
                _create_index(*arguments)
            else:
                raise CommandError(
                        _to_bytestring(u'Comando inválido'))

        except elasticsearch.exceptions.TransportError as exc:
            raise CommandError(str(exc))

