from piston.handler import AnonymousBaseHandler
from piston import doc

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
            return models.Journal.objects.get(collections__name=collection, print_issn=issn)
        except models.Journal.DoesNotExist:
            return []
