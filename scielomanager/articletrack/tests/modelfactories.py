# coding: utf-8
import factory

from articletrack import models


class CollectionFactory(factory.Factory):
    FACTORY_FOR = models.Collection

    url = u'http://www.scielo.br/'
    name = factory.Sequence(lambda n: 'scielo%s' % n)
    address_number = u'430'
    country = u'Brasil'
    address = u'Rua Machado Bittencourt'
    email = u'fapesp@scielo.org'
    name_slug = factory.Sequence(lambda n: 'scl%s' % n)


class CheckinFactory(factory.Factory):
    FACTORY_FOR = models.Checkin

    collection = factory.SubFactory(CollectionFactory)

    articlepkg_ref = 1
    attempt_ref = 1
    article_title = u'An azafluorenone alkaloid and a megastigmane from Unonopsis lindmanii (Annonaceae)'
    journal_title = u'Journal of the Brazilian Chemical Society'
    issue_label = u'2013 v.24 n.4'
    package_name = u'20132404.zip'
    uploaded_at = '2013-11-13 15:23:12.286068-02'
    created_at = '2013-11-13 15:23:18.286068-02'


class NoticeFactory(factory.Factory):
    FACTORY_FOR = models.Notice

    checkin = factory.SubFactory(CheckinFactory)

    stage = u'reference'
    checkpoint = u'Validation'
    message = u'The reference xyz is not ok'
    status = 'error'
    created_at = '2013-11-13 15:23:18.286068-02'
