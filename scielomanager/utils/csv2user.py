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

from django.contrib.auth.models import User, Group
from scielomanager.journalmanager import models
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

'''
    CSV format
    1 = Nome
    2 = Login
    3 = Email
    4 = collection
    5 = group
    Format example: "antonietayanez","myanez@conicyt.cl","yanez","Chile"
    IMPORT: CAN NOT EXIST SPACES BETWEEN COMMA ON CSV FILE.
'''

try:
    filename = sys.argv[1]
except IndexError:
    sys.exit("Please, informe the CSV file path.")

try:
    with open(filename, 'rb') as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')
        for row in reader:
            try:
                if not User.objects.filter(username=row[0]):
                    user = User.objects.create_user(username=row[0], email=row[1], password=row[2])
                    user_collection = models.UserCollections(user=user,
                                        collection=models.Collection.objects.get(name=row[3]))
                    user_collection.save()
                    try:
                        group_id = Group.objects.get(name=row[4]).id
                        user.groups.add(Group.objects.get(name=row[4]).id)
                    except (ObjectDoesNotExist) as e:
                        print "Group not set to user: %s, line %d: %s" % (row[0], reader.line_num, e)

                    print "Create User ID: " + str(user.id) + ", Name: " + row[0]
                else:
                    print "User " + row[0] + " already exist."
            except (IndexError, IntegrityError) as e:
                sys.exit("Error in the file format %s, line %d: %s" % (filename, reader.line_num, e))
except IOError:
    print "CSV file not found."
