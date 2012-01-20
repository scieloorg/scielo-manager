#!/usr/bin/env python
#coding: utf-8
import json
import os
import difflib

from django.core.management import setup_environ

try:
    from scielomanager import settings
except ImportError:
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
    from sys import path
    path.append(BASE_PATH)
    import settings

setup_environ(settings)
from journalmanager.models import *

class SectionImport:

    def __init__(self):
        self.summary{}

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
        
    def run_import(self, json_file, collection):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """

        json_parsed={} 
        collection = self.get_collection(collection)

        if __name__ == '__main__':
            json_file = open(json_file,'r')
            json_parsed = json.loads(json_file.read())
        else:
            json_parsed = json_file # Para testes, carregado pelo unittest

        for record in json_parsed:
            loaded_section = self.load_section(collection, record)

import_journal = JournalImport()
import_result = import_journal.run_import('section.json', 'Brasil')

print import_journal.get_summary()