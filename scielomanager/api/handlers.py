from piston.handler import AnonymousBaseHandler
from django.db.models import Q

from scielomanager.journalmanager import models

class Journal(AnonymousBaseHandler):
    model = models.Journal
    allow_methods = ('GET',)
    fields = (
        'title',
        ('collections', ()),
        ('publisher', ('name',)),
        ('sponsor', ('name',)),
        'previous_title',
        ('use_license', ('license_code', 'disclaimer')),
        ('languages', ('iso_code',)),
        'title_iso',
        'short_title',
        'acronym',
        'scielo_issn',
        'print_issn',
        'eletronic_issn',
        'subject_descriptors',
        'init_year',
        'init_vol',
        'init_num',
        'final_year',
        'final_vol',
        'final_num',
        'frequency',
        'pub_status',
        'editorial_standard',
        'ctrl_vocabulary',
        'pub_level',
        'secs_code',
        'copyrighter',
        'url_online_submission',
        'url_journal',
        'index_coverage',
        'cover',
        'other_previous_title',
    )

    def read(self, request, collection, issn=None):
        try:
            if issn:
                return models.Journal.objects.get(Q(print_issn=issn) | Q(eletronic_issn=issn),
                    collections__name_slug=collection)
            else:
                return models.Journal.objects.filter(collections__name_slug=collection)
        except models.Journal.DoesNotExist:
            return []

class Collection(AnonymousBaseHandler):
    model = models.Collection
    allow_methods = ('GET',)
    fields = (
        'name',
        'name_slug',
        'acronym',
        'address',
        'address_number',
        'address_complement',
        'city',
        'state',
        'country',
        'zip_code',
        'fax',
        'phone',
        'url',
        'mail',
    )

    def read(self, request, name_slug=None):
        try:
            if name_slug:
                return models.Collection.objects.get(name_slug=name_slug)
            else:
                return models.Collection.objects.all()
        except models.Collection.DoesNotExist:
            return []

class Issue(AnonymousBaseHandler):
    model = models.Issue
    allowed_methods = ('GET',)

    def read(self, request, journal, collection, issue_id=None):
        try:
            if issue_id:
                return models.Issue.object.get(Q(print_issn=journal) | Q(eletronic_issn=journal), 
                    collection__name_slug=collection, id = issue_id)
            else:
                return models.Issue.object.filter(Q(print_issn=journal) | Q(eletronic_issn=journal), 
                    collection__name_slug=collection)
        except models.Issue.DoesNotExist:
                return []