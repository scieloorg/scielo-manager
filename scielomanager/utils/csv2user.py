#!/usr/bin/python
#coding: utf-8

import sys
import os
import csv
from django.core.management import setup_environ

try:
    from scielomanager import settings
except ImportError:
    BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    from sys import path
    path.append(BASE_PATH)
    import settings

setup_environ(settings)

from django.contrib.auth.models import User
from scielomanager.journalmanager import models

'''
    CSV format
    0 = ID
    1 = Nome
    2 = Login
    3 = Email
    4 = collection
    Format example: "antonietayanez","myanez@conicyt.cl","yanez","Chile"
    IMPORT: CAN NOT EXIST SPACES BETWEEN COMMA ON CSV FILE.
'''

filename = sys.argv[1]

try:
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            try:
                user = User.objects.get(username=row[0])
                user.username = row[0]
                user.email = row[1]
                user.set_password(row[2])
                models.UserCollections.objects.filter(user=user).delete()
                user_collection = models.UserCollections(user=user, collection=models.Collection.objects.get(name=row[3]))
                user_collection.save()
                print "Update User ID: " + str(user.id) + ", name: " + row[0]
            except:
                user = User.objects.create_user(username=row[0], email=row[1], password=row[2])
                user_collection = models.UserCollections(user=user, collection=models.Collection.objects.get(name=row[3]))
                user_collection.save()
                user.save()
                print "Create User ID: " + str(user.id) + ", name: " + row[0]
except csv.Error, e:
    sys.exit('file %s, line %d: %s' % (filename, reader.line_num, e))
