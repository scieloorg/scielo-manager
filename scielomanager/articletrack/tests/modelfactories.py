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


class AttemptFactory(factory.Factory):
    FACTORY_FOR = models.Attempt

    articlepkg_id = 1
    checkin_id = 1
    collection = factory.SubFactory(CollectionFactory)
    article_title = u'An azafluorenone alkaloid and a megastigmane from Unonopsis lindmanii (Annonaceae)'
    journal_title = u'Journal of the Brazilian Chemical Society'
    issue_label = u'2013 v.24 n.4'
    pkgmeta_filename = u'20132404.zip'
    pkgmeta_md5 = u'sha1 strint'
    pkgmeta_filesize = 256
    pkgmeta_filecount = 10
    pkgmeta_submitter = u'SciELO Brasil'


class StatusFactory(factory.Factory):
    FACTORY_FOR = models.Status

    phase = u'upload'
    is_accomplished = True
    attempt = factory.SubFactory(AttemptFactory)
