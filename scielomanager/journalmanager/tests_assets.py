# coding: utf-8
"""
Collection of domain object factories to make testing easier.
"""
from django.contrib.auth.models import User

from scielomanager.journalmanager import models

def get_sample_section_dataform(**kwargs):
    section_attrs = {
      'title': 'Artigo Original',
    }

    section_attrs.update(kwargs)

    return section_attrs

def get_sample_journal_dataform(dict_params):
    journal_attrs = {
      'journal-sponsor': 'FAPESP',
      'journal-ctrl_vocabulary': 'decs',
      'journal-national_code': '083653-2',
      'journal-frequency': 'Q',
      'journal-final_num': '',
      'journal-validated': False,
      'journal-treatment_level': 'c',
      'journal-eletronic_issn': '',
      'journal-init_vol': '1',
      'journal-title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
      'journal-editorial_standard': 'vancouv',
      'journal-scielo_issn': 'print',
      'journal-secs_code': '6633',
      'journal-init_year': '1986',
      'journal-updated': '2012-01-19 15:44:21',
      'journal-acronym': 'ABCD',
      'journal-pub_level': 'CT',
      'journal-init_num': '1',
      'journal-literature_type': 'S',
      'journal-created': '2012-01-19 15:44:21',
      'journal-final_vol': '',
      'journal-subject_descriptors': 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA',
      'journal-pub_status': 'C',
      'journal-alphabet': 'B',
      'journal-print_issn': '0102-6720',

      #Title formset data
      'title-TOTAL_FORMS': 1,
      'title-INITIAL_FORMS': 0,
      'title-0-title': 'TITLE FORMSET TEST',
      'title-0-category': 'other',

      #Study Area formset data
      'studyarea-TOTAL_FORMS': 1,
      'studyarea-INITIAL_FORMS': 0,
      'studyarea-0-study_area': 'Agricultural Sciences',
      
      #Mission formset data
      'mission-TOTAL_FORMS': 1,
      'mission-INITIAL_FORMS': 0,
      'mission-0-description': 'To publish original scientific papers about Amazonia...',
      'mission-0-language': 'pt',

      #Text Language formset data
      'textlanguage-TOTAL_FORMS': 1,
      'textlanguage-INITIAL_FORMS': 0,
      'textlanguage-0-language': 'pt',

      #History Language formset data
      'hist-TOTAL_FORMS': 1,
      'hist-INITIAL_FORMS': 0,
      'hist-0-date': '2005-10-10',
      'hist-0-status': 'C',

      #History Language formset data
      'indexcoverage-TOTAL_FORMS': 1,
      'indexcoverage-INITIAL_FORMS': 0,
      'indexcoverage-0-title': 'ABCD. Arquivos Brasileiros de Cirurgia....',
      'indexcoverage-0-database': 1,
      'indexcoverage-0-identify': 'ABDC-Medline',

    }

    journal_attrs.update(dict_params)

    return journal_attrs

def get_sample_publisher_dataform(**kwargs):
    publisher_attrs = {
      'city': '',
      'fax': '',
      'validated': True,
      'name': u'Associação Nacional de História - ANPUH',
      'address_number': '222',
      'acronym': 'rbh',
      'country': 'BR',
      'cel': '',
      'phone': '',
      'state': '',
      'address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'mail': 'teste@scielo.org',
      'address_complement': '',
      'is_available': True,
    }

    publisher_attrs.update(kwargs)

    return publisher_attrs

def get_sample_issue_dataform(**kwargs):
    """
    Missing attributes: ['update_date', 'title', 'publisher_fullname', 'creation_date',
        'bibliographic_strip', 'section', 'use_license']
    """
    issue_attrs = {
        'total_documents': 16,
        'ctrl_vocabulary': '',
        'number': '3',
        'volume': '29',
        'editorial_standard': '',
        'is_available': True,
        'is_press_release': False,
        'publication_date': '1998-09-01',
        'is_marked_up': False,
    }

    issue_attrs.update(kwargs)

    return issue_attrs

def get_sample_uselicense_dataform(**kwargs):

    uselicense_attrs = {
        'license_code': 'CC BY-NC-SA',
        'reference_url': 'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.pt',
        'disclaimer': r'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Licença Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />Este trabalho foi licenciado com uma Licença <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons - Atribuição - NãoComercial - CompartilhaIgual 3.0 Não Adaptada</a>.'
    }

    uselicense_attrs.update(kwargs)

    return uselicense_attrs

def get_sample_journal():
    """
    Journal object factory

    Returns a journal object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['sponsor', 'final_num', 'eletronic_issn', 'final_vol', 'copyrighter', 'creator',
       'url_journal', 'url_online_submission', 'next_title_id', 'final_year', 'collections',
       'indexing_coverage', 'use_license', 'previous_title_id', 'url_main_collection',
       'publisher', 'center', 'notes',]
    """

    journal_attrs = {
      'sponsor': 'FAPESP',
      'ctrl_vocabulary': 'decs',
      'national_code': '083653-2',
      'frequency': 'Q',
      'final_num': '',
      'validated': False,
      'treatment_level': 'c',
      'eletronic_issn': '',
      'init_vol': '1',
      'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
      'editorial_standard': 'vancouv',
      'scielo_issn': 'print',
      'secs_code': '6633',
      'init_year': '1986',
      'updated': '2012-01-19 15:44:21',
      'acronym': 'ABCD',
      'pub_level': 'CT',
      'init_num': '1',
      'literature_type': 'S',
      'created': '2012-01-19 15:44:21',
      'final_vol': '',
      'subject_descriptors': 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA',
      'pub_status': 'C',
      'alphabet': 'B',
      'print_issn': '0102-6720',
      'is_available': True,
    }

    return models.Journal(**journal_attrs)

def get_sample_creator(is_active = True, is_superuser = True, is_staff = True):

    user_attrs = {
      'username': 'dummyuser',
      'first_name': 'Dummy',
      'last_name': 'User',
      'is_active': is_active,
      'is_superuser': is_superuser,
      'is_staff': is_staff,
      'password': 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799',
      'email': 'dev@scielo.org',
    }

    return User(**user_attrs)

def get_sample_userprofile(user, collection):

    profile_attrs = {
      'is_manager': False,
      'user': user,
      'collection': collection,
    }

    return models.UserProfile(**profile_attrs)


def get_sample_collection(validated = True):

    collection_attrs = {
      'url': 'http://www.scielo.br/',
      'validated': validated,
      'name': 'SciELO',
    }

    return models.Collection(**collection_attrs)

def get_sample_publisher(validated = True):
    """
    Returns a publisher object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['city', 'fax', 'address_number', 'cel', 'collection', 'phone', 'state', 'mail',
       'address_complement']
    """

    publisher_attrs = {
      'city': '',
      'fax': '',
      'validated': validated,
      'name': u'Associação Nacional de História - ANPUH',
      'address_number': '',
      'acronym': 'rbh',
      'country': '',
      'cel': '',
      'phone': '',
      'state': '',
      'address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'mail': '',
      'address_complement': '',
      'is_available': True,
    }

    return models.Publisher(**publisher_attrs)

def get_sample_uselicense():

    uselicense_attrs = {
        'license_code': 'CC BY-NC-SA',
        'reference_url': 'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.pt',
        'disclaimer': r'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Licença Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />Este trabalho foi licenciado com uma Licença <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons - Atribuição - NãoComercial - CompartilhaIgual 3.0 Não Adaptada</a>.'
    }

    return models.UseLicense(**uselicense_attrs)

def get_sample_center(validated = True):
    """
    Returns a center object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['city', 'fax', 'address_number', 'cel', 'collection', 'phone', 'state', 'mail',
       'address_complement']
    """

    center_attrs = {
      'city': '',
      'fax': '',
      'validated': validated,
      'name': u'Associação Nacional de História - ANPUH',
      'address_number': '',
      'acronym': 'rbh',
      'country': '',
      'cel': '',
      'phone': '',
      'state': '',
      'address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'mail': '',
      'address_complement': '',
      'is_available': True,
    }

    return models.Center(**center_attrs)

def get_sample_index_coverage():

    indexing_coverage_attrs = {
        'title': u'Literatura Latino-americana e do Caribe em Ciências da Saúde',
        'identify': 'lil-llccs',
    }

    return models.JournalIndexCoverage(**indexing_coverage_attrs)

def get_sample_index_database():

    indexing_index_database_attrs = {
        'name': u'Lilacs',
    }

    return models.IndexDatabase(**indexing_index_database_attrs)

def get_sample_section():
    """
    Missing attributes: ['translation', 'journal']
    """
    section_attrs = {
        'code': 'BJCE110',
    }

    return models.Section(**section_attrs)

def get_sample_issue():
    """
    Missing attributes: ['update_date', 'title', 'publisher_fullname', 'creation_date',
        'bibliographic_strip', 'section', 'use_license']
    """
    issue_attrs = {
        'total_documents': 16,
        'ctrl_vocabulary': '',
        'number': '3',
        'volume': '29',
        'editorial_standard': '',
        'is_available': True,
        'is_press_release': False,
        'publication_date': '1998-09-01',
        'is_marked_up': False,
    }

    return models.Issue(**issue_attrs)
