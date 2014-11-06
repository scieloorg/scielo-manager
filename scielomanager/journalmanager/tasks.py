# coding: utf-8
import logging
import base64
import threading
import contextlib

from elasticsearch import Elasticsearch
from django.conf import settings
from django.db.models import Q

from scielomanager.celery import app
from . import models


logger = logging.getLogger(__name__)
thread_lock = threading.Lock()

ARTICLE_INDEX_NAME = 'icatman'
ARTICLE_DOC_TYPE = 'article'


def get_elasticsearch():
    """Fábrica de clientes do Elasticsearch.

    Essa função é um singleton.
    """
    if not hasattr(get_elasticsearch, 'client'):
        get_elasticsearch.client = Elasticsearch(settings.ELASTICSEARCH_NODES)

    return get_elasticsearch.client


def index_article(id, struct):
    """Indexa `struct` no índice de artigos do catman no Elasticsearch.
    """
    client = get_elasticsearch()
    result = client.index(
            index=ARTICLE_INDEX_NAME, doc_type=ARTICLE_DOC_TYPE,
            id=id, body=struct
    )


def _gen_es_struct_from_article(article):
    """Retorna `article` em estrutura de dados esperada pelo Elasticsearch.
    """
    paths = article.XPaths

    values_to_struct_mapping = [
        ['abbrev_journal_title', paths.ABBREV_JOURNAL_TITLE],
        ['epub', paths.ISSN_EPUB], ['ppub', paths.ISSN_PPUB],
        ['volume', paths.VOLUME], ['issue', paths.ISSUE],
        ['year', paths.YEAR], ['doi', paths.DOI],
        ['pid', paths.PID], ['head_subject', paths.HEAD_SUBJECT],
        ['article_type', paths.ARTICLE_TYPE],
    ]

    es_struct = {attr: article.get_value(expr)
                 for attr, expr in values_to_struct_mapping}

    article_as_octets = str(article.xml)
    base64_octets = base64.b64encode(article_as_octets)

    partial_struct = {
        'version': article.xml_version,
        'is_aop': article.is_aop,
        'b64_source': base64_octets,
        'source': article_as_octets,
    }

    es_struct.update(partial_struct)

    return es_struct


@contextlib.contextmanager
def avoid_circular_signals():
    """ Garante a execução de um bloco de código sem o disparo de signals.

    A finalidade deste gerenciador de contexto é de permitir que entidades
    de `models.Article` sejam modificadas e salvas dentro de tasks invocadas
    por signals de `post_save`, sem que esses signals sejam disparados novamente.
    I.e. evita loop de signals.
    """
    try:
        thread_lock.acquire()
        models.disconnect_article_post_save_signals()
        yield
        models.connect_article_post_save_signals()
    finally:
        thread_lock.release()


@app.task(ignore_result=True)
def submit_to_elasticsearch(article_pk):
    """ Submete a instância de `journalmanager.models.Article` para indexação
    do Elasticsearch.
    """
    try:
        article = models.Article.objects.get(pk=article_pk)
    except models.Article.DoesNotExist:
        logger.error('Cannot find Article with pk: %s. Skipping the submission to elasticsearch.', article_pk)
        return None

    struct = _gen_es_struct_from_article(article)
    index_article(article.aid, struct)


@app.task(ignore_result=True)
def link_article_to_journal(article_pk):
    """ Tenta associar o artigo ao seu periódico.
    """
    try:
        article = models.Article.nocacheobjects.get(pk=article_pk, journal=None)
    except models.Article.DoesNotExist:
        logger.info('Cannot find unlinked Article with pk: %s. Skipping the linking task.', article_pk)
        return None

    try:
        journal = models.Journal.objects.get(
                Q(print_issn=article.issn_ppub) | Q(eletronic_issn=article.issn_epub))
    except models.Journal.DoesNotExist:
        logger.info('Cannot find parent Journal for Article with pk: %s. Skipping the linking task.', article_pk)
        return None

    article.journal = journal
    with avoid_circular_signals():
        article.save()

    logger.info('Article "%s" is now linked to journal "%s".',
            article.domain_key, journal.title)

    link_article_to_issue.delay(article_pk)


@app.task(ignore_result=True)
def link_article_to_issue(article_pk):
    """ Tenta associar o artigo ao seu número.
    """
    try:
        article = models.Article.objects.get(pk=article_pk, issue=None, is_aop=False)
    except models.Article.DoesNotExist:
        logger.info('Cannot find unlinked Article with pk: %s. Skipping the linking task.', article_pk)
        return None

    if article.journal is None:
        logger.info('Cannot link Article to issue without having a journal. Article pk: %s. Skipping the linking task.', article_pk)
    else:
        volume = article.get_value(article.XPaths.VOLUME)
        issue = article.get_value(article.XPaths.ISSUE)
        year = article.get_value(article.XPaths.YEAR)

        try:
            issue = article.journal.issue_set.get(
                    volume=volume, number=issue, publication_year=year)
        except models.Issue.DoesNotExist:
            logger.info('Cannot find Issue for Article with pk: %s. Skipping the linking task.', article_pk)
        else:
            article.issue = issue
            with avoid_circular_signals():
                article.save()

            logger.info('Article "%s" is now linked to issue "%s".',
                    article.domain_key, issue.label)

    return None


@app.task(ignore_result=True)
def process_orphan_articles():
    """ Tenta associar os artigos órfãos com periódicos e fascículos.
    """
    orphans = models.Article.objects.filter(issue=None)

    for orphan in orphans:
        if orphan.journal is None:
            link_article_to_journal.delay(orphan.pk)
        else:
            link_article_to_issue.delay(orphan.pk)

