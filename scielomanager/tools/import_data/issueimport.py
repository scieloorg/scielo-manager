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
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    BASE_PATH_APP = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'scielomanager'))
    from sys import path
    path.append(BASE_PATH)
    path.append(BASE_PATH_APP)

    import settings

setup_environ(settings)
from django.db.utils import IntegrityError, DatabaseError
from django.db import transaction
from journalmanager.models import *


class IssueImport:

    def __init__(self, collection):
        self._summary = {}
        self._journals = {}
        self._sections = {}
        self._collection = collection

        self._monthtoindex = {
            '': 0, 'mar': 3, 'sep': 9, 'may': 5, 'jun': 6, 'jul': 7, 'set': 9,
            'mai': 5, 'nov': 11, 'out': 10, 'ago': 8, 'fev': 2, 'dez': 12, 'feb': 2, 'ene': 1,
            'aug': 8, 'dic': 12, 'jan': 1, 'apr': 4, 'abr': 4, 'dec': 12, 'oct': 10
            }

        journal_json_parsed = json.loads(open('journal.json', 'r').read())
        self.load_journal_sections()
        self.load_journals(journal_json_parsed)  # carregando dicionário de periódicos self._journals

    def load_journal_sections(self):
        """
        Load all the journals sections into a dictionary, that will be used during the issue import to
        asign the correct section id to an issue. This must be done to avoid mistakes because Journal
        Manager handle same journals for different collections.
        """
        journals_sections = [i.section_set.all() for i in Journal.objects.filter(collections=self._collection)]
        self._sections = {}
        for journal in journals_sections:
            for section in journal:
                self._sections[section.legacy_code] = section.id

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

    @transaction.commit_manually
    def load_use_license(self, journal_issn):
        use_license = UseLicense()

        if journal_issn in self._journals:
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

        issue_sections = []

        if '49' in record:
            for code in record['49']:
                expanded = subfield.expand(code)
                parsed_subfields = dict(expanded)
                if parsed_subfields['c'] in self._sections:
                    section_id = self._sections[parsed_subfields['c']]
                    section = Section.objects.get(id=section_id)
                    try:
                        issue.section.add(section)
                    except ObjectDoesNotExist:
                        print "Inconsistência nos dados carregando seção"

        return issue_sections

    def issue_type(self, record):
        data = record.get('31', ' ')[0]
        data += record.get('32', ' ')[0]

        if '131' in record or '132' in record:
            return 'supplement'

        if 'spe' in data:
            return 'special'

        return 'regular'

    def load_issue(self, record):
        """
        Function: load_issue
        Retorna model issue que foi registrado no banco de dados
        """

        issue = Issue()
        error = False

        try:
            journal = Journal.objects.get(print_issn=record['35'][0], collections=self._collection.id)
        except ObjectDoesNotExist:
            try:
                journal = Journal.objects.get(eletronic_issn=record['35'][0], collections=self._collection.id)
            except ObjectDoesNotExist:
                print u"Inconsistência de dados tentando encontrar periódico com ISSN: %s" % record['35'][0]
                error = True

        if error:
            return False

        issue_type = self.issue_type(record)
        issue.type = issue_type

        issue.volume = record.get('31', ' ')[0].strip()

        number = record.get('32', ' ')[0].strip()
        if 'spe' in number:
            issue.spe_text = number.lower().replace('spe', '')
        else:
            issue.number = number

        suppl_volume = suppl_number = ''
        suppl_text = []
        if '131' in record:
            suppl_text.append(record['131'][0].strip())

        if '132' in record:
            suppl_text.append(record['132'][0].strip())

        if len(suppl_text) > 0:
            issue.suppl_text = ' '.join(suppl_text)

        if '41' in record:
            if record['41'][0] == 'pr':
                issue.is_press_release = True

        if '43' in record:
            expanded = subfield.expand(record['43'][0])
            month_start = dict(expanded)
            if 'm' in month_start:
                month_start = month_start['m'][:3].lower()
                if month_start in self._monthtoindex:
                    month_start = self._monthtoindex[month_start]
                else:
                    month_start = 0
            else:
                month_start = 0

        if '122' in record:
            issue.total_documents = record['122'][0]
        else:
            issue.total_documents = 0

        if '65' in record:
            year = record['65'][0][0:4]
            month_end = record['65'][0][4:6]
            if month_end == '00':
                month_end = '01'
            issue.publication_start_month = month_start
            issue.publication_end_month = month_end
            issue.publication_year = int(year)
        else:
            print u'Fasciculo %s %s %s não possui data de publicação' % (record['35'][0], record['31'][0], record['32'][0])
            issue.publication_start_month = 0
            issue.publication_end_month = 0
            issue.publication_year = 0000

        current_year = datetime.date(datetime.now()).year
        previous_year = current_year - 1
        if issue.number.lower() == 'ahead':
            if int(issue.publication_year) == int(current_year):
                journal.current_ahead_documents = issue.total_documents
                print u"ahead {0} de {1} removido da lista de issues, o total ({2}) de documentos foi transferido para models.journal.current_ahead_documents".format(journal.title, issue.publication_year, issue.total_documents)

            if int(issue.publication_year) == int(previous_year):
                journal.previous_ahead_documents = issue.total_documents
                print u"ahead {0} de {1} removido da lista de issues, o total ({2}) de documentos foi transferido para models.journal.previous_ahead_documents".format(journal.title, issue.publication_year, issue.total_documents)
            journal.save()
            return False

        issue.journal = journal
        issue.creation_date = datetime.now()

        if '33' in record:
            issue.title = record['33'][0]

        if '36' in record:
            try:
                issue.order = int(str(record['36'][0])[4:])
            except ValueError:
                print record
        if '200' in record:
            if int(record['200'][0]) == 1:
                issue.is_marked_up = True
            else:
                issue.is_marked_up = False
        if '62' in record:
            issue.publisher_fullname = record['62'][0]
        if '85' in record:
            issue.ctrl_vocabulary = record['85'][0]
        if '117' in record:
            issue.editorial_standard = record['117'][0]

        license = self.load_use_license(record['35'][0])
        if license:
            issue.use_license = license

        try:
            issue.save(force_insert=True)
        except DatabaseError as e:
            print "error({0}), input data: {1}".format(e.message, issue.__dict__)

        if '91' in record:
            created = u'%s-%s-01T01:01:01' % (record['91'][0][0:4], record['91'][0][4:6])
            issue.created = datetime.strptime(created, "%Y-%m-%dT%H:%M:%S")

        issue.save()

        if '33' in record:
            for subtitle in record['33']:
                expanded = subfield.expand(subtitle)
                parsed_subfields = dict(expanded)

                title = parsed_subfields['_']
                lang = parsed_subfields['l']

                language = Language.objects.get(iso_code=lang)
                issuetitle = IssueTitle()
                issuetitle.title = title
                issuetitle.issue = issue
                issuetitle.language = language
                issuetitle.save(force_insert=True)

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
            if '935' in record:
                self._journals[record['935'][0]] = {}  # Se for igual ao 400 ira sobrescrever

            if '541' in record:
                f540 = subfield.CompositeField(subfield.expand(record['540'][0]))
                href_pattern = re.compile('href=\\"[^ \t\n\r\f\v]*\\"')  # regex para encontrar url no texto de disclaimer

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
                if '935' in record:
                    self._journals[record['935'][0]]['use_license'] = {}
                    self._journals[record['935'][0]]['use_license']['license_code'] = record['541'][0]
                    self._journals[record['935'][0]]['use_license']['reference_url'] = reference_url
                    self._journals[record['935'][0]]['use_license']['disclaimer'] = f540['t']

            else:
                self._journals[record['400'][0]]['use_license'] = False
                if '935' in record:
                    self._journals[record['935'][0]]['use_license'] = False

    def run_import(self, json_file, conflicted_journals):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """

        issue_json_file = open(json_file, 'r')
        issue_json_parsed = json.loads(issue_json_file.read())

        for record in issue_json_parsed:
            if record['35'][0] in conflicted_journals:
                continue
            self.load_issue(record)
