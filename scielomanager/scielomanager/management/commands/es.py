# coding: utf-8
"""Tarefas de manutenção da integração com o Elasticsearch.
"""
from django.core.management.base import BaseCommand, CommandError
import elasticsearch

from scielomanager import connectors
from journalmanager import tasks


_HELP = u"""\
Executa tarefas de manutenção da integração com o Elasticsearch.

Os comandos são:
    createindex    Cria o índice e define o mapping.
    deleteindex    Remove o índice.
    reindex        Reindexa todos os artigos.
"""


def _to_bytestring(text):
    return text.encode('utf-8')


def _create_index():
    client = connectors.ArticleElasticsearch()
    client.create_index()


def _delete_index():
    client = connectors.ArticleElasticsearch()
    client.delete_index()


def _reindex_articles():
    tasks.mark_articles_as_dirty()
    tasks.process_dirty_articles.delay()


class Command(BaseCommand):
    args = '<command> [<args>]'
    help = _HELP
    requires_model_validation = False

    def handle(self, *args, **options):
        if not args:
            raise CommandError(
                    _to_bytestring("'./manage.py help es' para ajuda."))

        command = args[0]

        try:
            if command == 'createindex':
                _create_index()
            elif command == 'deleteindex':
                _delete_index()
            elif command == 'reindex':
                _reindex_articles()
            else:
                raise CommandError(
                        _to_bytestring(u'Comando inválido'))

        except elasticsearch.exceptions.TransportError as exc:
            raise CommandError(str(exc))

