#!/usr/bin/env python

import json
import os
import difflib
from django.core.management import setup_environ
import settings
setup_environ(settings)
from journalmanager.models import *

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
    
    journal.title =  reg['100'][0]
    journal.institution = inst_relationship
    journal.creator_id = 1
    journal.collection = collection

    journal.save(force_insert=True)

print Done!
