# coding: utf-8
import os
import thriftpy
import json
import logging
from datetime import date

from thriftpy.rpc import make_client
from xylose.scielodocument import Article, Journal, Issue

LIMIT = 1000

logger = logging.getLogger(__name__)

articlemeta_thrift = thriftpy.load(
    os.path.join(os.path.dirname(__file__))+'/articlemeta.thrift')


class ServerError(Exception):
    def __init__(self, message=None):
        self.message = message or 'thirftclient: ServerError'

    def __str__(self):
        return repr(self.message)


class ArticleMeta(object):

    def __init__(self, address, port):
        """
        Cliente thrift para o Articlemeta.
        """
        self._address = address
        self._port = port

    @property
    def client(self):

        client = make_client(
            articlemeta_thrift.ArticleMeta,
            self._address,
            self._port
        )
        return client

    def journals(self, collection=None, issn=None):
        offset = 0
        while True:
            identifiers = self.client.get_journal_identifiers(
                collection=collection, issn=issn, limit=LIMIT, offset=offset)
            if len(identifiers) == 0:
                raise StopIteration

            for identifier in identifiers:

                journal = self.client.get_journal(
                    code=identifier.code[0], collection=identifier.collection)

                jjournal = json.loads(journal)

                xjournal = Journal(jjournal)

                logger.info('Journal loaded: %s_%s' % (
                    identifier.collection, identifier.code))

                yield xjournal

            offset += 1000

    def exists_article(self, code, collection):
        try:
            return self.client.exists_article(
                code,
                collection
            )
        except:
            msg = 'Error checking if document exists: %s_%s' % (collection, code)
            raise ServerError(msg)

    def set_doaj_id(self, code, collection, doaj_id):
        try:
            article = self.client.set_doaj_id(
                code,
                collection,
                doaj_id
            )
        except:
            msg = 'Error senting doaj id for document: %s_%s' % (collection, code)
            raise ServerError(msg)

    def issue(self, code, collection, replace_journal_metadata=True):

        try:
            issue = self.client.get_issue(
                code=code,
                collection=collection,
                replace_journal_metadata=True
            )
        except:
            msg = 'Error retrieving issue: %s_%s' % (collection, code)
            raise ServerError(msg)

        try:
            jissue = json.loads(issue)
        except:
            msg = 'Fail to load JSON when retrienving document: %s_%s' % (
                collection, code)
            raise ServerError(msg)

        xissue = Issue(jissue)

        logger.info('Issue loaded: %s_%s' % (collection, code))
        return xissue

    def issues(self, collection=None, issn=None, from_date=None, until_date=None, extra_filter=None):
        offset = 0

        while True:
            identifiers = self.client.get_issue_identifiers(
                collection=collection, issn=issn, from_date=from_date,
                until_date=until_date, limit=LIMIT, offset=offset,
                extra_filter=extra_filter)

            if len(identifiers) == 0:
                raise StopIteration

            for identifier in identifiers:

                issue = self.issue(
                    code=identifier.code,
                    collection=identifier.collection,
                    replace_journal_metadata=True
                )

                yield issue

            offset += 1000

    def document(self, code, collection, replace_journal_metadata=True, fmt='xylose'):
        try:
            article = self.client.get_article(
                code=code,
                collection=collection,
                replace_journal_metadata=True,
                fmt=fmt
            )
        except:
            msg = 'Error retrieving document: %s_%s' % (collection, code)
            raise ServerError(msg)

        if fmt == 'xylose':
            jarticle = None
            try:
                jarticle = json.loads(article)
            except:
                msg = 'Fail to load JSON when retrienving document: %s_%s' % (collection, code)
                raise ServerError(msg)

            if not jarticle:
                logger.warning('Document not found for : %s_%s' % (collection, code))
                return None

            xarticle = Article(jarticle)
            logger.info('Document loaded: %s_%s' % (collection, code))

            return xarticle

        logger.info('Document loaded: %s_%s' % (collection, code))
        return article

    def documents(self, collection=None, issn=None, from_date=None, until_date=None, fmt='xylose', extra_filter=None):
        offset = 0
        while True:
            identifiers = self.client.get_article_identifiers(
                collection=collection, issn=issn, from_date=from_date,
                until_date=until_date, limit=LIMIT, offset=offset,
                extra_filter=extra_filter)

            if len(identifiers) == 0:
                raise StopIteration

            for identifier in identifiers:

                document = self.document(
                    code=identifier.code,
                    collection=identifier.collection,
                    replace_journal_metadata=True,
                    fmt=fmt
                )

                yield document

            offset += 1000

    def collections(self):

        return [i for i in self.client.get_collection_identifiers()]
