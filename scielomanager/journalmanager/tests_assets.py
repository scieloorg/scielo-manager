# coding: utf-8
"""
Collection of domain object factories to make testing easier.
"""
from django.contrib.auth.models import User

from scielomanager.journalmanager import models

def get_sample_section_dataform(**kwargs):
    section_attrs = {
      #Titles formset data
      'titles-TOTAL_FORMS': 1,
      'titles-INITIAL_FORMS': 0,
      'titles-0-title': 'TITLES FORMSET TEST',
    }

    section_attrs.update(kwargs)

    return section_attrs

def get_sample_userprofile(**kwargs):
    userprofile_attrs = {
        'email': 'dev@scielo.org',
    }
    userprofile_attrs.update(kwargs)

    return models.UserProfile(**userprofile_attrs)

def get_sample_journal_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    journal_attrs = {
      'journal-sponsor': 'FAPESP',
      'journal-ctrl_vocabulary': 'decs',
      'journal-frequency': 'Q',
      'journal-final_num': '',
      'journal-validated': False,
      'journal-eletronic_issn': '0102-6720',
      'journal-init_vol': '1',
      'journal-title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
      'journal-title_iso': u'ABCD. Arquivos B. de C. D. (São Paulo)',
      'journal-short_title': u'ABCD.(São Paulo)',
      'journal-editorial_standard': 'vancouv',
      'journal-scielo_issn': 'print',
      'journal-secs_code': '6633',
      'journal-init_year': '1986',
      'journal-updated': '2012-01-19 15:44:21',
      'journal-acronym': 'ABCD',
      'journal-pub_level': 'CT',
      'journal-init_num': '1',
      'journal-created': '2012-01-19 15:44:21',
      'journal-final_vol': '',
      'journal-subject_descriptors': 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA',
      'journal-pub_status': 'C',
      'journal-pub_status_changed_by': 'O motivo da mudança é...',
      'journal-print_issn': '0102-6720',
      'journal-copyrighter': 'Texto do copyrighter',

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


      #History Language formset data
      'hist-TOTAL_FORMS': 1,
      'hist-INITIAL_FORMS': 0,
      'hist-0-date': '2005-10-10',
      'hist-0-status': 'C',

    }

    journal_attrs.update(dict_params)

    return journal_attrs

def get_sample_institution_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    institution_attrs = {
      'institution-city': '',
      'institution-fax': '',
      'institution-validated': True,
      'institution-name': u'Associação Nacional de História - ANPUH',
      'institution-Address_number': '222',
      'institution-acronym': 'rbh',
      'institution-country': 'BR',
      'institution-cel': '',
      'institution-phone': '',
      'institution-state': '',
      'institution-Address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'institution-mail': 'teste@scielo.org',
      'institution-Address_complement': '',
      'institution-is_trashed': False,

      #Collection formset data
      'institutioncollections-TOTAL_FORMS': 1,
      'institutioncollections-INITIAL_FORMS': 0,

    }

    institution_attrs.update(dict_params)

    return institution_attrs

def get_sample_collection_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    sponsor_attrs = {
      'collection-url': u'http://www.scielo.br/',
      'collection-validated': True,
      'collection-name': u'SciELO',
      'collection-address_number': u'430',
      'collection-country': u'Brasil',
      'collection-address': u'Rua Machado Bittencourt',
      'collection-mail': u'fapesp@scielo.org',
    }

    sponsor_attrs.update(dict_params)

    return sponsor_attrs

def get_sample_sponsor_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    sponsor_attrs = {
      'sponsor-city': '',
      'sponsor-fax': '',
      'sponsor-validated': True,
      'sponsor-name': u'Fundação de Amparo a Pesquisa do Estado de São Paulo',
      'sponsor-address_number': '222',
      'sponsor-acronym': 'FAPESP',
      'sponsor-country': 'BR',
      'sponsor-cel': '',
      'sponsor-phone': '',
      'sponsor-state': '',
      'sponsor-address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'sponsor-mail': 'fapesp@scielo.org',
      'sponsor-address_complement': '',
      'sponsor-is_trashed': False,
    }

    sponsor_attrs.update(dict_params)

    return sponsor_attrs

def get_sample_publisher_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    publisher_attrs = {
      'publisher-city': '',
      'publisher-fax': '',
      'publisher-validated': True,
      'publisher-name': u'Associação Nacional de História - ANPUH',
      'publisher-address_number': '222',
      'publisher-acronym': 'rbh',
      'publisher-country': 'BR',
      'publisher-cel': '',
      'publisher-phone': '',
      'publisher-state': '',
      'publisher-address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'publisher-mail': 'teste@scielo.org',
      'publisher-address_complement': '',
      'publisher-is_trashed': False,
    }

    publisher_attrs.update(dict_params)

    return publisher_attrs

def get_sample_issue_dataform(dict_params=None):
    """
    Missing attributes: ['update_date', 'title', 'publisher_fullname', 'creation_date',
        'section', 'use_license']
    """
    if dict_params is None:
        dict_params = {}

    issue_attrs = {
        'total_documents': 16,
        'ctrl_vocabulary': '',
        'number': '3',
        'volume': '29',
        'editorial_standard': '',
        'is_trashed': False,
        'is_press_release': False,
        'publication_date': '1998-09-01',
        'is_marked_up': False,
        'publisher_fullname': 'Publisher Fullname',
        'editorial_standard': 'other',

        #Title formset data
        'title-TOTAL_FORMS': 1,
        'title-INITIAL_FORMS': 0,
        'title-0-title': 'TITLE FORMSET TEST',

    }

    issue_attrs.update(dict_params)

    return issue_attrs

def get_sample_uselicense_dataform(**kwargs):

    uselicense_attrs = {
        'license_code': 'CC BY-NC-SA',
        'reference_url': 'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.pt',
        'disclaimer': r'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Licença Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />Este trabalho foi licenciado com uma Licença <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons - Atribuição - NãoComercial - CompartilhaIgual 3.0 Não Adaptada</a>.'
    }

    uselicense_attrs.update(kwargs)

    return uselicense_attrs

def get_sample_user_dataform(dict_params=None):

    if dict_params is None:
        dict_params = {}

    user_attrs = {
        'user-username': 'dummyuser_add',
        'user-first_name': 'Dummy',
        'user-last_name': 'User',
        'user-is_active': True,
        'user-is_superuser': True,
        'user-is_staff': True,
        'user-password': 'sha1$93d45$5f366b56ce0444bfea0f5634c7ce8248508c9799',
        'user-email': 'dev@scielo.org',

        #Collection formset data
        'usercollections-TOTAL_FORMS': 1,
        'usercollections-INITIAL_FORMS': 0,

        #User formset data
        'userprofile-0-email': 'dummyuser@dummymail.com',
        'userprofile-TOTAL_FORMS': 1,
        'userprofile-INITIAL_FORMS': 0

        }

    user_attrs.update(dict_params)

    return user_attrs

def get_sample_journal():
    """
    Journal object factory

    Returns a journal object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['sponsor', 'final_num', 'eletronic_issn', 'final_vol', 'copyrighter', 'creator',
       'url_journal', 'url_online_submission', 'next_title_id', 'final_year', 'collections',
       'use_license', 'previous_title_id', 'url_main_collection',
       'publisher', 'center', 'notes','pub_status_changed_by']
    """

    journal_attrs = {
      'ctrl_vocabulary': 'decs',
      'frequency': 'Q',
      'final_num': '',
      'validated': False,
      'eletronic_issn': '',
      'init_vol': '1',
      'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
      'title_iso': u'ABCD. Arquivos B. de C. D. (São Paulo)',
      'short_title': u'ABCD.(São Paulo)',
      'editorial_standard': 'vancouv',
      'scielo_issn': 'print',
      'secs_code': '6633',
      'init_year': '1986',
      'updated': '2012-01-19 15:44:21',
      'acronym': 'ABCD',
      'pub_level': 'CT',
      'init_num': '1',
      'created': '2012-01-19 15:44:21',
      'final_vol': '',
      'subject_descriptors': 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA',
      'pub_status': 'C',
      'pub_status_reason': 'Motivo da mudança é...',
      'print_issn': '0102-6720',
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

def get_sample_usercollections(user, collection):

    usercollections_attrs = {
      'is_manager': True,
      'is_default': False,
      'user': user,
      'collection': collection,
    }

    return models.UserCollections(**usercollections_attrs)


def get_sample_collection(validated = True):

    collection_attrs = {
      'url': 'http://www.scielo.br/',
      'validated': validated,
      'name': 'SciELO',
      'fax': '11 5555-4444',
      'address_number': '430',
      'country': 'Brasil',
      'state': 'São Paulo',
      'city': 'São Paulo',
      'address': u'Rua Machado Bittencourt',
      'mail': 'fapesp@scielo.org',
    }

    return models.Collection(**collection_attrs)

def get_sample_sponsor(validated = True):
    """
    Returns a sponsor object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['city', 'fax', 'address_number', 'cel', 'collection', 'phone', 'state', 'mail',
       'address_complement']
    """

    sponsor_attrs = {
      'city': '',
      'fax': '',
      'validated': validated,
      'name': u'Fundação de Amparo a Pesquisa do Estado de São Paulo',
      'address_number': '',
      'acronym': 'FAPESP',
      'country': '',
      'cel': '',
      'phone': '',
      'state': '',
      'address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'mail': '',
      'address_complement': '',
      'is_trashed': False,

    }

    return models.Sponsor(**sponsor_attrs)

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
      'is_trashed': False,

    }

    return models.Publisher(**publisher_attrs)

def get_sample_uselicense():

    uselicense_attrs = {
        'license_code': 'CC BY-NC-SA',
        'reference_url': 'http://creativecommons.org/licenses/by-nc-sa/3.0/deed.pt',
        'disclaimer': r'<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/"><img alt="Licença Creative Commons" style="border-width:0" src="http://i.creativecommons.org/l/by-nc-sa/3.0/88x31.png" /></a><br />Este trabalho foi licenciado com uma Licença <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/3.0/">Creative Commons - Atribuição - NãoComercial - CompartilhaIgual 3.0 Não Adaptada</a>.'
    }

    return models.UseLicense(**uselicense_attrs)

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
        'is_trashed': False,
        'is_press_release': False,
        'publication_date': '1998-09-01',
        'is_marked_up': False,
    }

    return models.Issue(**issue_attrs)

def get_sample_language():
    language_attrs = {
        'iso_code': 'pt',
        'name': 'Portuguese',
    }

    return models.Language(**language_attrs)
