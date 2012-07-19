#!/usr/bin/env python
#coding: utf-8
import json
import os
import re
import difflib
import subfield
from datetime import datetime
from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

try:
    from scielomanager import settings
except ImportError:
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    from sys import path
    path.append(BASE_PATH)
    import settings

setup_environ(settings)
from django.db.utils import IntegrityError
from django.db import transaction
from journalmanager.models import *

class IssueImport:

    def __init__(self):
        self._summary = {}
        self._journals = {}

        journal_json_parsed = json.loads(open('journal.json','r').read())

        self.load_journals(journal_json_parsed) # carregando dicionário de periódicos self._journals

    def charge_summary(self, attribute):
        """
        Function: charge_summary
        Carrega com +1 cada atributo passado para o metodo, se o attributo nao existir ele e criado.
        """
        if not self._summary.has_key(attribute):
            self._summary[attribute] = 0

        self._summary[attribute] += 1

    def get_summary(self):
        """
        Function: get_summary
        Retorna o resumo de carga de registros
        """
        return self._summary

    @transaction.commit_manually
    def load_use_license(self, journal_issn):
        use_license = UseLicense()
        exists = False
        if self._journals.has_key(journal_issn):
            license = self._journals[journal_issn]['use_license']
            if license:
                use_license.license_code = license['license_code']
                use_license.reference_url = license['reference_url']
                use_license.disclaimer = license['disclaimer']
                try:
                    use_license.save(force_insert=True)
                    self.charge_summary('licenses')
                except IntegrityError:
                    transaction.rollback()
                    self.charge_summary('duplicated_code_licenses')
                    use_license = UseLicense.objects.get(license_code=license['license_code'])
            else:
                return False
        else:
            return False

        transaction.commit()
        return use_license

    def load_sections(self, issue, record):
        import subfield

        issue_sections = []
        if record.has_key('49'):
            for code in record['49']:
                expanded = subfield.expand(code)
                parsed_subfields = dict(expanded)
                try:
                    section = Section.objects.get(code=parsed_subfields['c'])
                    issue.section.add(section)
                except ObjectDoesNotExist:
                    print "Inconsistência nos dados"
                
                

        return issue_sections


    def load_issue(self, record):
        """
        Function: load_issue
        Retorna model issue que foi registrado no banco de dados
        """

        issue = Issue()
        error = False

        try:
            journal = Journal.objects.get(print_issn=record['35'][0])
        except ObjectDoesNotExist:
            try:
                journal = Journal.objects.get(eletronic_issn=record['35'][0])
            except ObjectDoesNotExist:
                print u"Inconsistência de dados tentando encontrar periódico com ISSN: %s" % record['35'][0]
                error = True

        if error:
            return False

        issue.journal = journal
        issue.creation_date = datetime.now()

        if record.has_key('31'):
            issue.volume = record['31'][0]
        if record.has_key('32'):
            issue.number = record['32'][0]
        if record.has_key('33'):
            issue.title = record['33'][0]
        if record.has_key('41'):
            if record['41'][0] == 'pr':
                issue.is_press_release = True
        if record.has_key('33'):
            issue.title = record['33'][0]
        if record.has_key('65'):
            year = record['65'][0][0:4]
            month = record['65'][0][4:6]
            if month == '00':
                month = '01'

            issue.publication_start_month = month
            issue.publication_end_month = 0
            issue.publication_year = year
        else:
            print u'Fasciculo %s %s %s não possui data de publicação' % (record['35'][0],record['31'][0],record['32'][0])
            issue.publication_start_month = 0
            issue.publication_end_month = 0
            issue.publication_year = 0000

        if record.has_key('91'):
            update = u'%s-%s-01T01:01:01' % (record['91'][0][0:4],record['91'][0][4:6])
            issue.update_date = datetime.strptime(update, "%Y-%m-%dT%H:%M:%S")
        if record.has_key('42'):
            if int(record['42'][0]) == 1:
                issue.is_available = True
            else:
                issue.is_available = False
        if record.has_key('200'):
            if int(record['200'][0]) == 1:
                issue.is_marked_up = True
            else:
                issue.is_marked_up = False
        if record.has_key('62'):
            issue.publisher_fullname = record['62'][0]
        if record.has_key('122'):
            issue.total_documents = record['122'][0]
        if record.has_key('85'):
            issue.ctrl_vocabulary = record['85'][0]
        if record.has_key('117'):
            issue.editorial_standard = record['117'][0]

        license = self.load_use_license(record['35'][0])
        if license:
            issue.use_license = license

        issue.save(force_insert=True)

        self.load_sections(issue, record)

        self.charge_summary('issues')



        return issue

    def load_journals(self, json_file):
        """
        Function: load_journals
        Esse metodo cria um dicionário de periódicos com atributos necessários para a criação de
        fascículos. Alguns registros seram transferidos das bases de periódicos para a base de
        fascículos e nesses caso esse dicionário será utilizado para carregar esses dados.

        Os campos a serem carregados no dicionário são:
        540 - licensa de uso

        """
        for record in json_file:
            self._journals[record['400'][0]] = {}
            self._journals[record['935'][0]] = {} # Se for igual ao 400 ira sobrescrever

            if record.has_key('541'):
                f540 = subfield.CompositeField(subfield.expand(record['540'][0]))
                href_pattern = re.compile('href=\\"[^ \t\n\r\f\v]*\\"') #regex para encontrar url no texto de disclaimer

                url_match = href_pattern.search(f540['t'])
                if url_match:
                    reference_url = url_match.group()[6:-1]
                else:
                    reference_url = ''

                f540 = subfield.CompositeField(subfield.expand(record['540'][0]))

                self._journals[record['400'][0]]['use_license'] = {}
                self._journals[record['935'][0]]['use_license'] = {}
                self._journals[record['400'][0]]['use_license']['license_code'] = record['541'][0]
                self._journals[record['935'][0]]['use_license']['license_code'] = record['541'][0]
                self._journals[record['400'][0]]['use_license']['reference_url'] = reference_url
                self._journals[record['935'][0]]['use_license']['reference_url'] = reference_url
                self._journals[record['400'][0]]['use_license']['disclaimer'] = f540['t']
                self._journals[record['935'][0]]['use_license']['disclaimer'] = f540['t']
            else:
                self._journals[record['400'][0]]['use_license'] = False
                self._journals[record['935'][0]]['use_license'] = False


    def run_import(self, json_file):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """

        json_parsed={}

        issue_json_file = open(json_file,'r')
        issue_json_parsed = json.loads(issue_json_file.read())

        for record in issue_json_parsed:
            loaded_issue = self.load_issue(record)
