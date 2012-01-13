#!/usr/bin/env python

import json
import os
from django.core.management import setup_environ
import settings
setup_environ(settings)
from journalmanager.models import *

json_file=open('journal.json','r')
json_parsed=json.loads(json_file.read())

collection = Collection.objects.get(id=1)

for reg in json_parsed:
    institution = Institution()
    institution.name = reg['480'][0]
    institution.acronym = reg['68'][0]
    institution.collection = collection
    institution.Address = " ".join(reg['63'])
    institution.save(force_insert=True)

print "Done!!!"
