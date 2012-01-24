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
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    from sys import path
    path.append(BASE_PATH)
    import settings

setup_environ(settings)
from journalmanager.models import *

class IssueImport:

    def __init__(self):
        self._summary = {}

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


    def load_issue(self, record):
        """
        Function: load_issue
        Retorna model issue que foi registrado no banco de dados
        """

        issue = Issue()

        try:
            journal = Journal.objects.get(print_issn=record['35'][0])
        except ObjectDoesNotExist:
            try:
                journal = Journal.objects.get(eletronic_issn=record['35'][0])
            except ObjectDoesNotExist:
                print "Inconsistência de dados tentando encontrar periódico com ISSN:"+record['35'][0]

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
        if record.has_key('64'):

            f64 = subfield.CompositeField(subfield.expand(record['64'][0]))
            pub_date = f64['a']+'-'+f64['m']+'-01T01:01:01'
            issue.publication_date = datetime.strptime(pub_date, "%Y-%m-%dT%H:%M:%S")
        if record.has_key('91'):
            update = record['91'][0][0:4]+'-'+record['91'][0][4:6]+'-01T01:01:01'
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

        issue.save(force_insert=True)

        return issue
        
    def run_import(self, json_file):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """

        json_parsed={} 

        if __name__ == '__main__':
            issue_json_file = open(json_file,'r')
            issue_json_parsed = json.loads(issue_json_file.read())
        else:
            issue_json_parsed = issue_json_file # Para testes, carregado pelo unittest

        for record in issue_json_parsed:
            loaded_issue = self.load_issue(record)

import_issue = IssueImport()
import_result = import_issue.run_import('issue.json')

print import_section.get_summary()