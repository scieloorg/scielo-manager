#!/usr/bin/env python
#coding: utf-8
import json
import os
import difflib
import subfield
from datetime import datetime
from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

try:
    from scielomanager import settings
except ImportError:
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scielomanager'))
    from sys import path
    path.append(BASE_PATH)
    import settings

setup_environ(settings)
from journalmanager.models import *

LANG_DICT = {'pt': 'Portuguese',
             'en': 'English',
             'es': 'Spanish',
             'de': 'German',
             'it': 'Italian',
             'fr': 'French',
             'la': 'Latin'}


class SectionImport:

    def __init__(self):
        self._summary = {}

    def charge_summary(self, attribute):
        """
        Function: charge_summary
        Carrega com +1 cada atributo passado para o metodo, se o attributo nao existir ele e criado.
        """
        if not attribute in self._summary:
            self._summary[attribute] = 0

        self._summary[attribute] += 1

    def get_summary(self):
        """
        Function: get_summary
        Retorna o resumo de carga de registros
        """
        return self._summary

    def load_journal(self, issn, collection):
        try:
            journal = Journal.objects.get(eletronic_issn=issn, collection=collection.id)
        except ObjectDoesNotExist:
            try:
                journal = Journal.objects.get(print_issn=issn, collection=collection.id)
            except ObjectDoesNotExist:
                return None

        return journal

    def load_section(self, record, collection):
        section = ""
        section_by_language = {}

        journal = self.load_journal(record['35'][0], collection=collection)

        if '49' in record:
            for sec in record['49']:  # Criando dicionário organizado de secoes
                parsed_subfields = subfield.CompositeField(subfield.expand(sec))
                if not parsed_subfields['c'] in section_by_language:
                    section_by_language[parsed_subfields['c']] = {}  # Criando Secao
                if not parsed_subfields['l'] in section_by_language[parsed_subfields['c']]:
                    section_by_language[parsed_subfields['c']][parsed_subfields['l']] = parsed_subfields['t']
        else:
            print u"Periódico %s não tem seções definidas" % record['35'][0]
            self.charge_summary('journals_without_sections')

        for sec_key, sec in section_by_language.items():
            if journal is None:
                print('Invalid Journal: {}'.format(record['35'][0]))
                continue

            section = Section()
            if 'pt' in sec:
                section.title = sec['pt']
            elif 'en' in sec:
                section.title = sec['en']
            elif 'es' in sec:
                section.title = sec['es']
            else:
                section.title = ''
            section.legacy_code = sec_key
            section.journal = journal
            section.creation_date = datetime.now()
            section.save(force_insert=True)
            self.charge_summary('sections')

            lang_dict = LANG_DICT

            for trans_key, trans in sec.items():
                try:
                    language = Language.objects.get(iso_code=trans_key)
                except Language.DoesNotExist:
                    language = Language.objects.create(iso_code=trans_key, name=lang_dict.get(trans_key, '###NOT FOUND###'))

                section_title = SectionTitle(section=section, title=trans, language=language)
                section_title.save()

                self.charge_summary('translations')

        return section

    def run_import(self, json_file, collection):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """
        section_json_file = open(json_file, 'r')
        section_json_parsed = json.loads(section_json_file.read())

        for record in section_json_parsed:
            loaded_section = self.load_section(record, collection)
