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

class JournalImport:

    def __init__(self):
        self._publishers_pool = []
        self._summary = {}


    def charge_summary(self, attribute):
        """
        Function: charge_summary
        Carrega com +1 cada atributo passado para o metodo, se o attributo nao existir ele e criado.
        """
        if not self._summary.has_key(attribute):
            self._summary[attribute] = 0    
        
        self._summary[attribute] += 1

    def get_collection(self, collection_name):
        """
        Function: get_collection 
        Recupera objeto coleção de acordo com o nome da coleção passado por parametro
        """
        return Collection.objects.get(name=collection_name)

    def have_similar_publishers(self, match_string):
        """
        Function: have_similar_publishers
        Identifica se existe instituicao ja registrada com o mesmo nome, com o objetivo de filtrar
        instituticoes duplicadas.
        Retorna o id da instituicao se houver uma cadastrada com o mesmo nome, caso contrario Retorna
        False.
        """
        publisher_id=""

        if len(self._publishers_pool) > 0:
            for inst in self._publishers_pool:
                if inst["match_string"] == match_string:
                    publisher_id = inst["id"]
                    break
                else:
                    publisher_id = False
        else:
            publisher_id = False

        return publisher_id

    def load_publisher(self, collection, record):
        """
        Function: load_publisher
        Retorna um objeto Publisher() caso a gravação do mesmo em banco de dados for concluida
        """

        publisher = Publisher()
        # Publishers Import
        publisher.name = record['480'][0]
        publisher.collection = collection
        publisher.address = " ".join(record['63'])
        
        match_string=publisher.name
        
        similar_key =  self.have_similar_publishers(match_string)

        loaded_publisher=""

        if similar_key != False:
            similar_publisher=Publisher.objects.get(id=similar_key)
            similar_publisher.address += "\n"+publisher.address
            similar_publisher.save()
            self.charge_summary("publishers_duplication_fix")
            loaded_publisher = similar_publisher
        else:
            publisher.save(force_insert=True)
            self.charge_summary("publishers")
            loaded_publisher = publisher
            self._publishers_pool.append(dict({"id":publisher.id,"match_string":match_string}))

        return loaded_publisher

    def load_studyarea(self, journal, areas):
        
        for i in areas:
            studyarea = JournalStudyArea()
            studyarea.journal = journal
            studyarea.study_area = i
            studyarea.save(force_insert=True)
            self.charge_summary("studyarea")

    def load_journal(self, collection, loaded_publisher, record):
        """
        Function: load_journal
        Retorna um objeto journal() caso a gravação do mesmo em banco de dados for concluida
        """

        issn_type=""
        print_issn=""
        electronic_issn=""
        journal = Journal()

        if record['35'][0] == "PRINT":
            issn_type="print"
            print_issn = record['935'][0]
            if record['935'][0] != record['400'][0]:
                electronic_issn = record['400'][0]
        else:
            issn_type="electronic"
            electronic_issn = record['935'][0]
            if record['935'][0] != record['400'][0]:
                print_issn = record['400'][0]

        journal.title =  record['100'][0]
        journal.short_title =  record['150'][0]
        journal.acronym = record['930'][0]
        journal.scielo_issn = issn_type
        journal.print_issn = print_issn
        journal.eletronic_issn = electronic_issn
        journal.subject_descriptors = ', '.join(record['440'])

        if record.has_key('301'):
            journal.init_year = record['301'][0]
        if record.has_key('302'):
            journal.init_vol = record['302'][0]
        if record.has_key('303'):
            journal.init_num = record['303'][0]
        if record.has_key('304'): 
            journal.final_year = record['304'][0]
        if record.has_key('305'):
            journal.final_vol = record['305'][0]
        if record.has_key('306'):
            journal.final_num = record['306'][0]
        if record.has_key('380'):
            journal.frequency = record['380'][0]
        if record.has_key('50'):
            journal.pub_status = record['50'][0]
        if record.has_key('340'):
            journal.alphabet = record['340'][0]
        if record.has_key('430'):
            journal.classification = record['430'][0]
        if record.has_key('20'):
            journal.national_code = record['20'][0]
        if record.has_key('117'):
            journal.editorial_standard = record['117'][0]
        if record.has_key('85'):
            journal.ctrl_vocabulary = record['85'][0]
        if record.has_key('5'):
            journal.literature_type = record['5'][0]
        if record.has_key('6'):        
            journal.treatment_level = record['6'][0]
        if record.has_key('330'):
            journal.pub_level = record['330'][0]
        #journal.indexing_coverage.add(join(record['450'])) 
        if record.has_key('37'):
            journal.secs_code = record['37'][0]

        journal.publisher = loaded_publisher
        journal.creator_id = 1
        journal.save(force_insert=True)
        self.charge_summary("journals")
        journal.collections.add(collection)

        self.load_studyarea(journal,record['441'])

        return journal

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
            loaded_publisher = self.load_publisher(collection, record)
            loaded_journal = self.load_journal(collection, loaded_publisher, record)
        
    def get_summary(self):
        """
        Function: get_summary
        Retorna o resumo de carga de registros
        """
        return self._summary

import_journal = JournalImport()
import_result = import_journal.run_import('journal.json', 'Brasil')

print import_journal.get_summary()
