# coding: utf-8
import datetime
import logging
import base64
from elasticsearch import Elasticsearch
from django.conf import settings
from django.db.models import get_model
from scielomanager.celery import app


logger = logging.getLogger(__name__)
ARTICLE_INDEX_NAME = 'icatman'
ARTICLE_DOC_TYPE = 'article'
Article = get_model('journalmanager', 'Article') # to avoid import models.Article then circular import hell!!!

def _get_es_client():
    return Elasticsearch([{
        'host': settings.ELASTICSEARCH_CONFIG['HOST'],
        'port': settings.ELASTICSEARCH_CONFIG['PORT'],
        }])


@app.task(bind=True)
def new_article_create_es_index(self, article_aid):
    """
    When a new article is submited in the SciELO Manager then
    must submit relevant data to the Elasticsearch instance.
    """
    logger.debug('[new_article_create_es_index] START task to CREATE index on ES (aid=%s) at %s' % (article_aid, datetime.datetime.now()))

    try:
        article = Article.objects.get(aid=article_aid)
    except Article.DoesNotExist as e:
        logger.error('[new_article_create_es_index] FAIL while retrieving article (aid: %s): %s' % (article_aid, e))
    else:
        article_xml_as_string = str(article.xml)
        article_data = {
            "abbrev_journal_title": article.xml_abbrev_journal_title,
            "epub": article.xml_epub,
            "ppub": article.xml_ppub,
            "volume": article.xml_volume,
            "issue": article.xml_issue,
            "year": article.xml_year,
            "doi": article.xml_doi,
            "pid": article.xml_pid,
            "head_subject": article.xml_head_subject,
            "is_aop": article.xml_is_aop,
            "article_type": article.xml_article_type,
            "version": article.xml_version,
            "b64_source": base64.b64encode(article_xml_as_string),
            "source": article_xml_as_string,
        }
        es = _get_es_client()
        result = es.index(index=ARTICLE_INDEX_NAME, doc_type=ARTICLE_DOC_TYPE, id=article_aid, body=article_data)
        logger.info('[new_article_create_es_index] RESULT: %s' % result)
    logger.debug('[new_article_create_es_index] FINISH task at %s' % datetime.datetime.now())
