# coding: utf-8
""" Tasks do celery para a aplicação `journalmanager`.

  - Todas as tasks que executam `Article.save` devem tomar cuidado com
    problemas de concorrência, haja vista que os callbacks de post save
    devem ser desabilitados em alguns casos, por meio do contexto
    `avoid_circular_signals`.
"""
import os
import io
import logging
import threading
import contextlib
import datetime
import operator
from copy import deepcopy

from lxml import isoschematron, etree
from django.db.models import Q
from django.db import IntegrityError, transaction
from celery.utils.log import get_task_logger

from scielomanager.celery import app
from scielomanager import connectors
from . import models


logger = get_task_logger(__name__)


ARTICLE_SAVE_MUTEX = threading.Lock()
BASIC_ARTICLE_META_PATH = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 'basic_article_meta.sch')


# instâncias de isoschematron.Schematron não são thread-safe
ARTICLE_META_SCHEMATRON = isoschematron.Schematron(file=BASIC_ARTICLE_META_PATH)


elasticsearch_client = connectors.ArticleElasticsearch()


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

    partial_struct = {
        'version': article.xml_version,
        'is_aop': article.is_aop,
        'source': article_as_octets,
        'aid': article.aid,
        'timestamp': datetime.datetime.now(),
    }

    es_struct.update(partial_struct)

    return es_struct


@contextlib.contextmanager
def avoid_circular_signals(mutex):
    """ Garante a execução de um bloco de código sem o disparo de signals.

    A finalidade deste gerenciador de contexto é de permitir que entidades
    de `models.Article` sejam modificadas e salvas dentro de tasks invocadas
    por signals de `post_save`, sem que esses signals sejam disparados novamente.
    I.e. evita loop de signals.
    """
    try:
        mutex.acquire()
        models.disconnect_article_post_save_signals()
        yield
        models.connect_article_post_save_signals()
    finally:
        mutex.release()


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
    elasticsearch_client.add(article.aid, struct)

    logger.info('Article "%s" was indexed successfully.', article.domain_key)

    article.es_updated_at = datetime.datetime.now()
    article.es_is_dirty = False
    with avoid_circular_signals(ARTICLE_SAVE_MUTEX):
        article.save()


@app.task(ignore_result=True)
def link_article_to_journal(article_pk):
    """ Tenta associar o artigo ao seu periódico.
    """
    try:
        article = models.Article.objects.get(pk=article_pk, journal=None)
    except models.Article.DoesNotExist:
        logger.info('Cannot find unlinked Article with pk: %s. Skipping the linking task.', article_pk)
        return None

    try:
        query_params = []
        if article.issn_ppub:
            query_params.append(Q(print_issn=article.issn_ppub))

        if article.issn_epub:
            query_params.append(Q(eletronic_issn=article.issn_epub))

        if not query_params:
            logger.error('Missing attributes issn_ppub and issn_epub in Article wit pk: %s.', article_pk)
            return None

        query_expr = reduce(operator.or_, query_params)
        journal = models.Journal.objects.get(query_expr)

    except models.Journal.DoesNotExist:
        # Pode ser que os ISSNs do XML estejam invertidos...
        try:
            query_params = []
            if article.issn_ppub:
                query_params.append(Q(eletronic_issn=article.issn_ppub))

            if article.issn_epub:
                query_params.append(Q(print_issn=article.issn_epub))

            if not query_params:
                logger.error('Missing attributes issn_ppub and issn_epub in Article wit pk: %s.', article_pk)
                return None

            query_expr = reduce(operator.or_, query_params)
            journal = models.Journal.objects.get(query_expr)

        except models.Journal.DoesNotExist:
            logger.info('Cannot find parent Journal for Article with pk: %s. Skipping the linking task.', article_pk)
            return None

    article.journal = journal
    with avoid_circular_signals(ARTICLE_SAVE_MUTEX):
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
            with avoid_circular_signals(ARTICLE_SAVE_MUTEX):
                article.save()

            logger.info('Article "%s" is now linked to issue "%s".',
                    article.domain_key, issue.label)

    return None


@app.task(ignore_result=True)
def process_orphan_articles():
    """ Tenta associar os artigos órfãos com periódicos e fascículos.
    """
    orphans = models.Article.objects.only('pk', 'journal').filter(issue=None)

    for orphan in orphans:
        if orphan.journal is None:
            link_article_to_journal.delay(orphan.pk)
        else:
            link_article_to_issue.delay(orphan.pk)


@app.task(ignore_result=True)
def process_dirty_articles():
    """ Task (periódica) que garanta a indexação dos artigos sujos.
    """
    dirties = models.Article.objects.only('pk').filter(es_is_dirty=True)

    for dirty in dirties:
        submit_to_elasticsearch.delay(dirty.pk)


@app.task(throws=(IntegrityError, ValueError))
def create_article_from_string(xml_string):
    """ Cria uma instância de `journalmanager.models.Article`.

    Pode levantar `django.db.IntegrityError` no caso de artigos duplicados,
    TypeError no caso de argumento com tipo diferente de unicode ou
    ValueError no caso de artigos cujos elementos identificadores não estão
    presentes.

    :param xml_string: String de texto unicode.
    :return: aid (article-id) formado por uma string de 32 bytes.
    """
    if not isinstance(xml_string, unicode):
        raise TypeError('Only unicode strings are accepted')

    xml_bstring = xml_string.encode('utf-8')

    try:
        parsed_xml = etree.parse(io.BytesIO(xml_bstring))

    except etree.XMLSyntaxError as exc:
        raise ValueError(u"Syntax error: %s.", exc.message)

    metadata_sch = deepcopy(ARTICLE_META_SCHEMATRON)
    if not metadata_sch.validate(parsed_xml):
        logger.debug('Schematron validation error log: %s.', metadata_sch.error_log)
        raise ValueError('Missing identification elements')

    new_article = models.Article(xml=xml_bstring)
    with ARTICLE_SAVE_MUTEX:
        new_article.save_dirty()

    logger.info('New Article added with aid: %s.', new_article.aid)

    return new_article.aid


@app.task(ignore_result=True)
def rebuild_article_domain_key(article_pk):
    """ Reconstroi a chave de domínio do artigo.

    Atenção: Essa task não é utilizada pelo projeto e pode ser removida
    a qualquer momento.
    https://github.com/scieloorg/scielo-manager/issues/1183
    """
    try:
        article = models.Article.objects.get(pk=article_pk)
    except models.Article.DoesNotExist:
        logger.info('Cannot find Article with pk: %s.', article_pk)
        return None

    # a chave é gerada automaticamente ao salvar o objeto e
    # o artigo não precisa ser reindexado no Elasticsearch
    article.save()


@app.task(ignore_result=True)
def rebuild_articles_domain_key():
    """ Dispara a tarefa de reconstrução da chave de domínio para todos artigos.

    Atenção: Essa task não é utilizada pelo projeto e pode ser removida
    a qualquer momento.
    https://github.com/scieloorg/scielo-manager/issues/1183
    """
    articles = models.Article.objects.only('pk').all()

    for article in articles:
        rebuild_article_domain_key.delay(article.pk)


@app.task(ignore_result=True)
def link_article_with_their_related(article_pk):
    """ Tenta associar artigos relacionados.

    Essa função é idempotente, e pode ser executada inúmeras vezes até
    que todas as referências de um artigo sejam estabelecidas.

    Caso alguma exceção seja levantada, nenhuma mudança será persistida na
    base de dados.
    """
    try:
        referrer = models.Article.objects.get(pk=article_pk,
                articles_linkage_is_pending=True)
    except models.Article.DoesNotExist:
        logger.info('Cannot find Article with with pk: %s. Skipping the task.',
                article_pk)
        return None

    related_article_elements = (
            referrer.xml.xpath(models.Article.XPaths.RELATED_CORRECTED_ARTICLES) +
            referrer.xml.xpath(models.Article.XPaths.RELATED_COMMENTARY_ARTICLES)
    )

    doi_type_pairs = ([elem.attrib['{http://www.w3.org/1999/xlink}href'],
                      elem.attrib['related-article-type']]
                      for elem in related_article_elements)

    def _ensure_articles_are_linked(doi, rel_type):
        try:
            target = models.Article.objects.only('pk').get(doi=doi)
        except (models.Article.DoesNotExist, models.Article.MultipleObjectsReturned) as exc:
            logger.error('Cannot get article with DOI "%s". The error message is: "%s"',
                    doi, exc.message)
            return False

        _, created = models.ArticlesLinkage.objects.get_or_create(
                referrer=referrer, link_to=target, link_type=rel_type)

        logger.info('Article with pk %s is %s linked to %s',
                'now' if created else 'already', target.pk, referrer.pk)

        return True

    with transaction.commit_on_success():
        link_statuses = (_ensure_articles_are_linked(doi, rel_type)
                         for doi, rel_type in doi_type_pairs)

        if all(link_statuses):
            referrer.articles_linkage_is_pending = False
            with avoid_circular_signals(ARTICLE_SAVE_MUTEX):
                referrer.save()


@app.task(ignore_result=True)
def process_related_articles():
    """ Tenta associar artigos relacionados.
    """
    articles = models.Article.objects.only('pk').filter(
            articles_linkage_is_pending=True)

    for article in articles:
        link_article_with_their_related.delay(article.pk)

