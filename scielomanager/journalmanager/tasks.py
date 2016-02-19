# coding: utf-8
""" Tasks do celery para a aplicação `journalmanager`.

  - Todas as tasks que executam `Article.save` devem tomar cuidado com
    problemas de concorrência, haja vista que os callbacks de post save
    devem ser desabilitados em alguns casos, por meio do contexto
    `avoid_circular_signals`.
"""
import os
import io
import datetime
import operator
from copy import deepcopy

from lxml import isoschematron, etree
from django.db.models import Q
from django.db import IntegrityError, transaction
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from celery.utils.log import get_task_logger

from scielomanager.celery import app
from scielomanager import connectors
from . import models


logger = get_task_logger(__name__)


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

    try:
        links_to = [{'aid': rel.link_to.aid, 'type': rel.link_type}
                    for rel in article.links_to.all()]
    except ObjectDoesNotExist:
        links_to = []

    try:
        referrers = [{'aid': rel.referrer.aid, 'type': rel.link_type}
                     for rel in article.referrers.all()]
    except ObjectDoesNotExist:
        referrers = []

    partial_struct = {
        'version': article.xml_version,
        'is_aop': article.is_aop,
        'source': article_as_octets,
        'aid': article.aid,
        'timestamp': datetime.datetime.now(),
        'links_to': links_to,
        'referrers': referrers,
    }

    es_struct.update(partial_struct)

    return es_struct


@app.task(ignore_result=True)
def submit_to_elasticsearch(article_pk):
    """ Submete a instância de `journalmanager.models.Article` para indexação
    do Elasticsearch.
    """
    try:
        article = models.Article.objects.get(pk=article_pk,
                control_attributes__es_is_dirty=True)
    except models.Article.DoesNotExist:
        logger.error('Cannot find or Article is not ready to be submitted to elasticsearch. Pk: %s. Skipping.', article_pk)
        return None

    struct = _gen_es_struct_from_article(article)
    elasticsearch_client.add(article.aid, struct)

    logger.info('Article "%s" was indexed successfully.', article.domain_key)

    article_ctrl_attrs = article.control_attributes
    article_ctrl_attrs.es_updated_at = datetime.datetime.now()
    article_ctrl_attrs.es_is_dirty = False
    article_ctrl_attrs.save()


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
    dirties = models.Article.objects.only('pk').filter(
            control_attributes__es_is_dirty=True)

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
    new_article.save()

    logger.info('New Article added with aid: %s.', new_article.aid)

    return new_article.aid


@app.task(ignore_result=True)
def mark_articles_as_dirty():
    """ Marca todos os artigos para serem reindexados.
    """
    with transaction.commit_on_success():
        total_rows = models.ArticleControlAttributes.objects.all().update(es_is_dirty=True)

    logger.info('%s Articles were set as dirty to Elasticsearch.', total_rows)



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
                control_attributes__articles_linkage_is_pending=True)
    except models.Article.DoesNotExist:
        logger.info('Cannot find Article with with pk: %s. Skipping the task.',
                article_pk)
        return None

    related_article_elements = referrer.xml.xpath(
            models.Article.XPaths.RELATED_CORRECTED_ARTICLES)

    doi_type_pairs = ([elem.attrib['{http://www.w3.org/1999/xlink}href'],
                      elem.attrib['related-article-type']]
                      for elem in related_article_elements)

    def _ensure_articles_are_linked(doi, rel_type):
        try:
            target = models.Article.objects.get(doi=doi)
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
            referrer.control_attributes.articles_linkage_is_pending = False
            referrer.control_attributes.save()


@app.task(ignore_result=True)
def process_related_articles():
    """ Tenta associar artigos relacionados.
    """
    articles = models.Article.objects.only('pk').filter(
            control_attributes__articles_linkage_is_pending=True)

    for article in articles:
        link_article_with_their_related.delay(article.pk)


@app.task(throws=(ValueError,))
def create_articleasset_from_bytes(aid, filename, content, owner=None,
        use_license=None):
    """Cria uma instância de `journalmanager.models.ArticleAsset`.

    :param aid: ``article-id`` formado por uma string de 32 bytes.
    :param filename: string de texto contendo o nome do arquivo do ativo digital.
    :param content: string de bytes com o conteúdo do ativo digital.
    :param owner: (opcional) string de texto informando o detentor do copyright.
    :param use_license: (opcional): string de texto informando a licença de uso.
    """
    try:
        article = models.Article.objects.get(aid=aid)

    except models.Article.DoesNotExist:
        raise ValueError('Cannot find Article with aid: %s' % aid)

    _owner = owner or u''
    _use_license = use_license or u''

    asset = models.ArticleAsset(article=article, owner=_owner,
            use_license=_use_license)
    asset.file.save(filename, ContentFile(content))

    logger.info('New ArticleAsset %s added to Article with aid: %s.',
            repr(asset), aid)

    return asset.file.url

