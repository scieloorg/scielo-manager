import journalimport
import sectionimport
import issueimport

import sys

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
from journalmanager.models import Collection

collectionname = sys.argv[1]



print 'Checking if Collection %s exists at JournalManager Database' % (collectionname)

try:
    collection = Collection.objects.get(name=collectionname)
    collectionname = collection.name
except ObjectDoesNotExist:
    print 'Collection %s does not exists' % (collectionname)
except NameError:
    print 'Collection %s does not exists' % (collectionname)
else:
    print 'Collection %s exists' % (collectionname)

    print 'Importing Journals and Institutions from SciELO %s' % (collectionname)
    import_journal = journalimport.JournalImport()
    import_result = import_journal.run_import('journal.json', collection)
    print import_journal.get_summary()

    print 'Importing Sections from SciELO %s' % (collection.name)
    print 'Importing sectionimportSections from SciELO %s' % (collectionname)
    import_section = sectionimport.SectionImport()
    import_result = import_section.run_import('section.json')
    print import_section.get_summary()

    print 'Importing Issues from SciELO %s' % (collectionname)
    import_issue = issueimport.IssueImport()
    import_result = import_issue.run_import('issue.json')
    print import_issue.get_summary()