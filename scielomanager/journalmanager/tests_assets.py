#coding: utf-8
"""
Collection of domain object factories to make testing easier.
"""
from django.contrib.auth.models import User

from scielomanager.journalmanager import models


def get_sample_journal():
    """
    Journal object factory

    Returns a journal object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['classification', 'final_num', 'eletronic_issn', 'final_vol', 'copyrighter', 'creator',
       'url_journal', 'url_online_submission', 'next_title_id', 'final_year', 'collections',
       'indexing_coverage', 'use_license', 'previous_title_id', 'url_main_collection',
       'id_provided_by_the_center', 'institution', 'center', 'notes',]
    """

    journal_attrs = {
      'classification': '',
      'ctrl_vocabulary': 'decs',
      'national_code': '083653-2',
      'frequency': 'Q',
      'final_num': '',
      'validated': False,
      'treatment_level': 'c',
      'eletronic_issn': '',
      'init_vol': '1',
      'title': u'ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)',
      'study_area': 'Health Sciences',
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
      'short_title': 'ABCD, arq. bras. cir. dig.',
      'subject_descriptors': 'MEDICINA, CIRURGIA, GASTROENTEROLOGIA, GASTROENTEROLOGIA',
      'subscription': 'na',
      'pub_status': 'C',
      'alphabet': 'B',
      'pdf_access': 'art',
      'print_issn': '0102-6720'
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

def get_sample_institution(validated = True):
    """
    Returns a institution object, without the following attributes (non mandatory or need to be bound
    to another model object):
    - ['city', 'fax', 'Address_number', 'cel', 'collection', 'phone', 'state', 'mail',
       'Address_complement']
    """

    institution_attrs = {
      'city': '',
      'fax': '',
      'validated': validated,
      'name': u'Associação Nacional de História - ANPUH',
      'Address_number': '',
      'acronym': 'rbh',
      'country': '',
      'cel': '',
      'phone': '',
      'state': '',
      'Address': u'Av. Professor Lineu Prestes, 338 Cidade Universitária Caixa Postal 8105 05508-900 São Paulo SP Brazil Tel. / Fax: +55 11 3091-3047',
      'mail': '',
      'Address_complement': ''
    }

    return models.Institution(**institution_attrs)