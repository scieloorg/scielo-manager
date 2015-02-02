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
    Article = get_model('journalmanager', 'Article') # to avoid import models.Article then circular import hell!!!
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


@app.task(bind=True)
def link_article_to_issue(self, article_aid):
    """
    Retrieve an article (by aid). then pick the article metadata to look for an issue to match.
    """
    logger.debug('[link_article_to_issue] START task (aid=%s) at %s' % (article_aid, datetime.datetime.now()))
    # use of get_model to avoid circular import
    Article = get_model('journalmanager', 'Article')
    Journal = get_model('journalmanager', 'Journal')
    Issue = get_model('journalmanager', 'Issue')

    # retrieve article
    try:
        article = Article.objects.get(aid=article_aid)
    except Article.DoesNotExist as e:
        logger.error('[link_article_to_issue] FAIL while retrieving ARTICLE (aid: %s): %s' % (article_aid, e))
    else:
        if article.issue is None:
            # retrieve journal
            try:
                journal = Journal.objects.get(title_iso=article.xml_abbrev_journal_title)
            except Journal.DoesNotExist as e:
                logger.error('[link_article_to_issue] FAIL while retrieving JOURNAL (aid: %s, xml_abbrev_journal_title: %s): %s' % (article_aid, article.xml_abbrev_journal_title, e))
            except Journal.MultipleObjectsReturned as e:
                logger.error('[link_article_to_issue] FAIL Multiple JOURNALS Returned for (aid: %s, xml_abbrev_journal_title: %s): %s' % (article_aid, article.xml_abbrev_journal_title, e))
            else:

                # retrieve issue
                try:
                    issue = Issue.objects.get(journal=journal, volume=article.xml_volume, number=article.xml_issue)
                except Issue.DoesNotExist as e:
                    logger.error('[link_article_to_issue] FAIL while retrieving ISSUE (aid: %s, xml_volume: %s, xml_issue: %s): %s' % (article_aid, article.xml_volume, article.xml_issue, e))
                except Issue.MultipleObjectsReturned as e:
                    logger.error('[link_article_to_issue] FAIL Multiple ISSUES Returned for (aid: %s, xml_volume: %s, xml_issue: %s): %s' % (article_aid, article.xml_volume, article.xml_issue, e))
                else:
                    # link issue and article:
                    article.issue = issue
                    article.save()
                    logger.info('[link_article_to_issue] article has an issue now!: (aid: %s) -> (issue: %s)' % (article.aid, article.issue))
        else:
            logger.info('[link_article_to_issue] article has an issue already!: (aid: %s) -> (issue: %s)' % (article.aid, article.issue))

    logger.debug('[link_article_to_issue] FINISH task at %s' % datetime.datetime.now())


@app.task(bind=True)
def process_orphan_articles(self):
    """
    collect every orphan articles (orphan == articles without an issue related), and for each call: link_article_to_issue.
    This task is scheduled to run daily.
    """
    logger.debug("[process_orphan_articles] START process at %s" % datetime.datetime.now())
    # use of get_model to avoid circular import
    Article = get_model('journalmanager', 'Article')
    articles = Article.objects.filter(issue=None)
    logger.info('[process_orphan_articles] Found %s articles matching conditions' % articles.count())

    for article in articles:
        logger.info('[process_orphan_articles] Processing article (pk=%s, aid=%s)' % (article.pk, article.aid))
        link_article_to_issue.apply_async(args=[article.aid, ])

    logger.debug('[process_orphan_articles] FINISH process at %s' % datetime.datetime.now())

