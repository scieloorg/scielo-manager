# coding: utf-8
import factory

from articletrack import models
from journalmanager.tests.modelfactories import JournalFactory, UserFactory
from accounts.tests import HASH_FOR_123


class ArticleFactory(factory.Factory):
    FACTORY_FOR = models.Article

    #journals = JournalFactory()
    article_title = u'An azafluorenone alkaloid and a megastigmane from Unonopsis lindmanii (Annonaceae)'
    articlepkg_ref = 1
    journal_title = u'Journal of the Brazilian Chemical Society'
    issue_label = u'2013 v.24 n.4'
    pissn = '1234-1234'
    eissn = ''

    @classmethod
    def _prepare(cls, create, **kwargs):
        journal = JournalFactory()
        article = super(ArticleFactory, cls)._prepare(create, **kwargs)
        article.journals.add(journal)
        return article


class CheckinFactory(factory.Factory):
    FACTORY_FOR = models.Checkin

    attempt_ref = 1
    package_name = u'20132404.zip'
    uploaded_at = '2013-11-13 15:23:12.286068-02'
    created_at = '2013-11-13 15:23:18.286068-02'

    article = factory.SubFactory(ArticleFactory)


class NoticeFactory(factory.Factory):
    FACTORY_FOR = models.Notice

    checkin = factory.SubFactory(CheckinFactory)

    stage = u'reference'
    checkpoint = u'Validation'
    message = u'The reference xyz is not ok'
    status = 'error'
    created_at = '2013-11-13 15:23:18.286068-02'


class TicketFactory(factory.Factory):
    FACTORY_FOR = models.Ticket

    started_at = '2013-11-13 15:23:12'
    #finished_at = '2013-11-20 15:23:18.286068-02'
    title = u'change XYZ at ABC for XXX'
    message = u'the XYZ at ABC must be changed for XXX because YYY'
    article = factory.SubFactory(ArticleFactory)
    author = UserFactory(password=HASH_FOR_123, is_active=True)


class CommentFactory(factory.Factory):
    FACTORY_FOR = models.Comment

    #date = '2013-11-21 15:23:18'
    author = UserFactory(password=HASH_FOR_123, is_active=True)
    ticket = factory.SubFactory(TicketFactory)
    message = u'Fixed!'
