# coding: utf-8

import os
import sys

from django.core.management import setup_environ
from django.core.exceptions import ObjectDoesNotExist

import journalimport
import sectionimport
import issueimport

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

from django.contrib.auth.models import User
from journalmanager.models import Collection

collectionname = unicode(sys.argv[1], 'utf-8')
collectionurl = sys.argv[2]

user = User.objects.get(pk=1)

print u'Checking if Collection %s exists at JournalManager Database' % collectionname
collection = Collection.objects.get_or_create(name=collectionname, url=collectionurl)[0]
collection.save()
collectionname = collection.name

print u'Importing Journals and Institutions from SciELO %s' % (collectionname)
import_journal = journalimport.JournalImport()
import_result = import_journal.run_import('journal.json', collection, user)
conflicted_journals = import_journal.get_conflicted_journals()
print import_journal.get_summary()
print {'conflicted_journals': conflicted_journals}

print u'Importing sectionimportSections from SciELO %s' % (collectionname)
import_section = sectionimport.SectionImport()
import_result = import_section.run_import('section.json', collection, conflicted_journals)
print import_section.get_summary()

print u'Importing Issues from SciELO %s' % (collectionname)
import_issue = issueimport.IssueImport(collection, )
import_result = import_issue.run_import('issue.json', conflicted_journals)
print import_issue.get_summary()
