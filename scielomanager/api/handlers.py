from piston.handler import AnonymousBaseHandler
from django.db.models import Q

from scielomanager.journalmanager import models

class Journal(AnonymousBaseHandler):
    model = models.Journal
    allow_methods = ('GET',)
    fields = (
        'title',
        ('collections', ('name',)),
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

    def read(self, request, collection, issn):
        try:
            return models.Journal.objects.get(Q(print_issn=issn) | Q(eletronic_issn=issn),
                collections__name_slug=collection)
        except models.Journal.DoesNotExist:
            return []

class Collection(AnonymousBaseHandler):
    model = models.Collection
    allow_methods = ('GET',)
    fields = (
        'name',
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