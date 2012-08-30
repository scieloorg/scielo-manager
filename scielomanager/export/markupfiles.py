# coding: utf-8
from scielomanager.export import bundle
from django.conf import settings


MEDIA_ROOT = settings.MEDIA_ROOT + '/export/'
MEDIA_URL = settings.MEDIA_URL + '/export/'


class GenerationError(Exception):
    def __init__(self, *args, **kwargs):
        super(GenerationError, self).__init__(*args, **kwargs)


class Automata(object):
    """
    Represents the automata.mds file
    http://ref.scielo.org/2qx6fb
    """
    # {dbvalue: (citat, norma)}
    standards = {
        'iso690': ('icitat', 'iso'),
        'nbr6023': ('acitat', 'abnt'),
        'other': ('ocitat', 'other'),
        'vancouv': ('vcitat', 'vanc'),
        'apa': ('pcitat', 'apa'),
    }
    # {dbvalue: journalmethod}
    issns = {
        'print': 'print_issn',
        'electronic': 'electronic_issn',
    }

    def __init__(self, journal):
        self._journal = journal

    @property
    def citat(self):
        tags = self.standards.get(self._journal.editorial_standard, None)
        if not tags:
            raise AttributeError()

        return tags[0]

    @property
    def norma(self):
        tags = self.standards.get(self._journal.editorial_standard, None)
        if not tags:
            raise AttributeError()

        return tags[1]

    @property
    def issn(self):
        pid_issn_field = self._journal.scielo_issn
        pid_issn = getattr(self._journal, self.issns[pid_issn_field], None)
        if not pid_issn:
            raise AttributeError()

        return pid_issn

    @property
    def acron(self):
        return self._journal.acronym

    def __unicode__(self):
        return '{0};{1};{2}.amd;tg{3}.amd'.format(self.issn,
            self.citat, self.acron, self.norma)


class Issue(object):
    def __init__(self, issue):
        self._issue = issue

    def __unicode__(self):
        legend = '{0} {1}'.format(self._issue.journal.title_iso, unicode(self._issue))
        period = '%02d/%02d' % (self._issue.publication_start_month, self._issue.publication_end_month)

        rows = '\n'.join([legend, period, str(self._issue.order), '', ''])
        return rows


def generate(journal, issue):
    automata = Automata(journal)
    issue = Issue(issue)

    try:
        packmeta = [
            ('automata.mds', unicode(automata)),
            ('issue.mds', unicode(issue)),
        ]
    except AttributeError as exc:
        raise GenerationError('it was impossible to generate automata.mds for %s. %s' % (journal.pk, exc))
    else:
        pkg = bundle.Bundle(*packmeta)

    pkg_filename = bundle.generate_filename('markupfiles')

    pkg.deploy(MEDIA_ROOT + pkg_filename)
    return MEDIA_URL + pkg_filename
