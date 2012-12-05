# coding: utf-8
import factory
from django_factory_boy import auth

from journalmanager import models


class SubjectCategoryFactory(factory.Factory):
    FACTORY_FOR = models.SubjectCategory

    term = 'Acoustics'


class StudyAreaFactory(factory.Factory):
    FACTORY_FOR = models.StudyArea

    study_area = 'Health Sciences'


class SponsorFactory(factory.Factory):
    FACTORY_FOR = models.Sponsor

    name = u'Fundação de Amparo a Pesquisa do Estado de São Paulo'
    address = u'Av. Professor Lineu Prestes, 338 Cidade Universitária \
                                Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047'
    email = 'fapesp@scielo.org'
    complement = ''


class UseLicenseFactory(factory.Factory):
    FACTORY_FOR = models.UseLicense

    license_code = factory.Sequence(lambda n: 'CC BY-NC-SA%s' % n)
    reference_url = u'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.pt'
    disclaimer = u'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Licença Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />Este trabalho foi licenciado com uma Licença <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons - Atribuição - NãoComercial - CompartilhaIgual 3.0 Não Adaptada</a>.'


class CollectionFactory(factory.Factory):
    FACTORY_FOR = models.Collection

    url = u'http://www.scielo.br/'
    name = factory.Sequence(lambda n: 'scielo%s' % n)
    address_number = u'430'
    country = u'Brasil'
    address = u'Rua Machado Bittencourt'
    email = u'fapesp@scielo.org'
    name_slug = factory.Sequence(lambda n: 'scl%s' % n)


class JournalFactory(factory.Factory):
    FACTORY_FOR = models.Journal

    ctrl_vocabulary = u'decs'
    frequency = u'Q'
    scielo_issn = u'print'
    print_issn = factory.Sequence(lambda n: '1234-%04d' % int(n))
    init_vol = u'1'
    title = u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)'
    title_iso = u'ABCD. Arquivos B. de C. D. (São Paulo)'
    short_title = u'ABCD.(São Paulo)'
    editorial_standard = u'vancouv'
    secs_code = u'6633'
    init_year = u'1986'
    acronym = factory.Sequence(lambda n: 'ABCD%s' % int(n))
    pub_level = u'CT'
    init_num = u'1',
    subject_descriptors = u"""
        MEDICINA
        CIRURGIA
        GASTROENTEROLOGIA
        GASTROENTEROLOGIA""".strip()
    pub_status = u'current'
    pub_status_reason = u'Motivo da mudança é...'
    publisher_name = u'Colégio Brasileiro de Cirurgia Digestiva'
    publisher_country = u'BR'
    publisher_state = u'SP'
    publication_city = u'São Paulo'
    editor_address = u'Av. Brigadeiro Luiz Antonio, 278 - 6° - Salas 10 e 11, 01318-901 São Paulo/SP Brasil, Tel. = (11) 3288-8174/3289-0741'
    editor_email = u'cbcd@cbcd.org.br'

    creator = factory.SubFactory(auth.UserF)
    pub_status_changed_by = factory.SubFactory(auth.UserF)
    use_license = factory.SubFactory(UseLicenseFactory)
    collection = factory.SubFactory(CollectionFactory)


class SectionFactory(factory.Factory):
    FACTORY_FOR = models.Section

    code = factory.Sequence(lambda n: 'BJCE%s' % n)

    journal = factory.SubFactory(JournalFactory)


class IssueFactory(factory.Factory):
    FACTORY_FOR = models.Issue

    total_documents = 16
    number = factory.Sequence(lambda n: '%s' % n)
    volume = factory.Sequence(lambda n: '%s' % n)
    is_trashed = False
    is_press_release = False
    publication_start_month = 9
    publication_end_month = 11
    publication_year = 2012
    is_marked_up = False

    journal = factory.SubFactory(JournalFactory)

    @classmethod
    def _prepare(cls, create, **kwargs):
        section = SectionFactory()
        issue = super(IssueFactory, cls)._prepare(create, **kwargs)
        issue.section.add(section)
        return issue


class UserProfileFactory(factory.Factory):
    FACTORY_FOR = models.UserProfile

    user = factory.SubFactory(auth.UserF)
    email = factory.Sequence(lambda n: 'email%s@example.com' % n)


class LanguageFactory(factory.Factory):
    FACTORY_FOR = models.Language

    iso_code = 'pt'
    name = 'portuguese'


class SectionTitleFactory(factory.Factory):
    FACTORY_FOR = models.SectionTitle

    title = u'Artigos Originais'

    language = factory.SubFactory(LanguageFactory)
    section = factory.SubFactory(SectionFactory)
