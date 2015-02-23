#!/usr/bin/python
#coding: utf-8

import sys, os, csv
from django.core.management import setup_environ

try:
    from scielomanager import settings
except ImportError:
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__),'../..'))
    from sys import path
    path.append(BASE_PATH)
    import scielomanager.settings

setup_environ(scielomanager.settings)

'''
    CSV format
    Column 0 = role EN
    Column 1 = role PT
    Column 2 = role ES
    Format example: Editor-in-Chief;EditorChefe;Editor jefe
'''

from editorialmanager import models
from journalmanager.models import Language

filename = sys.argv[1]
delimiter = sys.argv[2]

with open(filename, 'rb') as f:
    reader = csv.reader(f, delimiter=delimiter)
    try:
        for row in reader:
            role = models.RoleType(name=row[0])
            role.save()

            #Add PT translate to role
            trans_role = models.RoleTypeTranslation(name=row[1],
                                                    language= Language.objects.get(iso_code='pt'))
            trans_role.role = role
            trans_role.save()

            #Add ES translate to role
            trans_role = models.RoleTypeTranslation(name=row[2],
                                                    language= Language.objects.get(iso_code='es'))
            trans_role.role = role
            trans_role.save()

    except Exception as e:
        sys.exit('file %s, line %d, error %s' % (filename, reader.line_num, e))
