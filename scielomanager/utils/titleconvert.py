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

if __name__ == '__main__':
    json_file=open('journal.json','r')
    json_parsed=json.loads(json_file.read())

collection = Collection.objects.get(id=1)

institutions_pool = []

def have_similar_institutions(match_string, institutions_pool):
    institutions = Institution.objects.all()

    institution_id=""

    for inst in institutions_pool:
        if inst["match_string"] == match_string:
            institution_id = inst["id"]
            
    return institution_id



for reg in json_parsed:

    institution = Institution()
    journal = Journal()

    # Institutions Import
    institution.name = reg['480'][0]
    institution.acronym = reg['68'][0]
    institution.collection = collection
    institution.Address = " ".join(reg['63'])
    
    match_string=institution.name

    similar_key =  have_similar_institutions(match_string,institutions_pool)

    inst_relationship=""

    if similar_key != "":
        similar_institution=Institution.objects.get(id=similar_key)
        similar_institution.Address += "\n"+institution.Address
        similar_institution.save()
        inst_relationship = similar_institution
    else:
        institution.save(force_insert=True)
        institutions_pool.append(dict({"id":institution.id,"match_string":match_string}))
        inst_relationship = institution

    # Journal Import
    
    issn_type=""
    print_issn=""
    electronic_issn=""

    if reg['35'][0] == "PRINT":
        issn_type="print"
        print_issn = reg['935'][0]
        if reg['935'][0] != reg['400'][0]:
            electronic_issn = reg['400'][0]
    else:
        issn_type="electronic"
        electronic_issn = reg['935'][0]
        if reg['935'][0] != reg['400'][0]:
            print_issn = reg['400'][0]

    journal.title =  reg['100'][0]
    journal.short_title =  reg['150'][0]
    journal.acronym = reg['930'][0]
    journal.scielo_issn = issn_type
    journal.print_issn = print_issn
    journal.eletronic_issn = electronic_issn
    journal.subject_descriptors = ', '.join(reg['440'])
    journal.study_area = ', '.join(reg['441'])

    if reg.has_key('301'):
        journal.init_year = reg['301'][0]

    if reg.has_key('302'):
        journal.init_vol = reg['302'][0]

    if reg.has_key('303'):
        journal.init_num = reg['303'][0]

    if reg.has_key('304'): 
        journal.final_year = reg['304'][0]

    if reg.has_key('305'):
        journal.final_vol = reg['305'][0]

    if reg.has_key('306'):
        journal.final_num = reg['306'][0]

    if reg.has_key('380'):
        journal.frequency = reg['380'][0]

    if reg.has_key('50'):
        journal.pub_status = reg['50'][0]

    if reg.has_key('340'):
        journal.alphabet = reg['340'][0]

    if reg.has_key('430'):
        journal.classification = reg['430'][0]

    if reg.has_key('20'):
        journal.national_code = reg['20'][0]

    if reg.has_key('117'):
        journal.editorial_standard = reg['117'][0]

    if reg.has_key('85'):
        journal.ctrl_vocabulary = reg['85'][0]

    if reg.has_key('5'):
        journal.literature_type = reg['5'][0]

    if reg.has_key('6'):        
        journal.treatment_level = reg['6'][0]

    if reg.has_key('330'):
        journal.pub_level = reg['330'][0]

    #journal.indexing_coverage.add(join(reg['450'])) 
    if reg.has_key('37'):
        journal.secs_code = reg['37'][0]

    journal.institution = inst_relationship
    journal.creator_id = 1
    journal.save(force_insert=True)
    journal.collections.add(collection)

print "Done!"
