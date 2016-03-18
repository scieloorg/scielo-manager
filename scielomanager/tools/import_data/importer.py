# coding: utf-8
import os
from datetime import date

from django.core.management import setup_environ

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
from django.core import exceptions
from django.db.utils import DatabaseError, IntegrityError
from django.db import transaction
from django.db.models import Q
from django.contrib.auth.models import User
from journalmanager.models import *

import choices

logger = logging.getLogger(__name__)


def _config_logging(logging_level='INFO', logging_file=None):

    allowed_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    logger.setLevel(allowed_levels.get(logging_level, 'INFO'))

    if logging_file:
        hl = logging.FileHandler(logging_file, mode='a')
    else:
        hl = logging.StreamHandler()

    hl.setFormatter(formatter)
    hl.setLevel(allowed_levels.get(logging_level, 'INFO'))

    logger.addHandler(hl)

    return logger


class Catalog(object):

    def __init__(self, collection, user=None):
        """
        data must be a Xylose object
        """
        self.user = User.objects.get(pk=1) if user is None else user
        try:
            self.collection = Collection.objects.get(acronym=collection)
        except:
            raise ValueError('Collection do no exists: %s' % collection)

    def _load_language(self, language):

        language = Language.objects.get_or_create(
            iso_code=language,
            name=choices.LANG_DICT.get(language, '###NOT FOUND###')
        )[0]

        return language

    def _load_journal_mission(self, journal, missions):
        if missions is None:
            return

        for language, description in missions.items():
            mission = JournalMission()
            language = self._load_language(language)
            mission.language = language
            mission.description = description
            journal.missions.add(mission)

    def _load_journal_subject_areas(self, journal, areas):
        if areas is None:
            return

        for area in areas:
            try:
                studyarea = StudyArea.objects.get(study_area=area)
            except:
                logger.warning('Invalid study area (%s) for the journal (%s), nothing was assigned' % (
                    area, journal.title)
                )

            journal.study_areas.add(studyarea)

    def _load_journal_textlanguage(self, journal, languages):
        if languages is None:
            return

        for language in languages:
            language = self._load_language(language)
            journal.languages.add(language)

    def _load_journal_abstractlanguage(self, journal, languages):
        if languages is None:
            return

        for language in languages:
            language = self._load_language(language)
            journal.abstract_keyword_languages.add(language)

    def _load_journal_status_history(self, journal, status_history):

        ## cleanup before deploy the new status history
        timeline = JournalTimeline.objects.filter(
            journal=journal,
            collection=self.collection
        ).delete()

        if status_history is None:
            return

        for st_date, status, reason in status_history:

            if len(st_date) == 4:
                st_date += '-01-01'

            if len(st_date) == 7:
                st_date += '-01'

            defaults = {
                'created_by': self.user,
            }

            try:
                timeline = JournalTimeline.objects.get_or_create(
                    journal=journal,
                    collection=self.collection,
                    since=st_date,
                    status=status,
                    reason=reason,
                    defaults=defaults)[0]
            except exceptions.ValidationError:
                logger.warning('Invalid timeline (%s) for the journal (%s), nothing was assigned' % (
                    ', '.join([st_date, status, reason]), journal.title)
                )

        try:
            membership = Membership.objects.get_or_create(
                journal=journal,
                collection=self.collection,
                since=st_date,
                status=status,
                reason=reason,
                defaults=defaults
            )
        except IntegrityError:
            logger.warning('Invalid membership (%s) for the journal (%s), nothing was assigned' % (
                ', '.join([st_date, status, reason]), journal.title)
            )

        """
        models.Membership sempre replica o registro salvo para o
        JournalTimeline. No momento da importação esse comportamento é
        indesejado, para contorná-lo é realizada a exclusão dos registros
        inseridos verificando a data da execução da importação
        """
        JournalTimeline.objects.filter(
            journal=journal,
            collection=self.collection,
            since__month=date.today().month,
            since__year=date.today().year).delete()

    def _load_journal_other_titles(self, journal, data):

        for title in data.other_titles or []:
            title = JournalTitle()
            title.title = title
            title.category = 'other'
            journal.other_titles.add(title)

        # NLM/Medline Title
        if data.title_nlm:
            title = JournalTitle()
            title.title = data.title_nlm
            title.category = 'abbrev_nlm'
            journal.other_titles.add(title)

    def _load_journal_use_license(self, journal, permission):

        if permission is None:
            return

        use_license = UseLicense.objects.get_or_create(
            license_code=permission['id'].upper())[0]

        if 'text' in permission and permission['text']:
            use_license.disclaimer = permission['text']

        if 'url' in permission and permission['url']:
            use_license.reference_url = permission['url']

        use_license.save()

        journal.use_license = use_license

    def _load_journal_sponsor(self, journal, data):
        """
        Function: load_sponsor
        Retorna um objeto Sponsor() caso a gravação do mesmo em banco de dados for concluida
        """
        if data.sponsors is None:
            return

        for sponsor in data.sponsors:

            db_sponsor = Sponsor.objects.get_or_create(name=sponsor)[0]
            db_sponsor.collections.add(self.collection)
            db_sponsor.save()
            journal.sponsor.add(db_sponsor)

    def _load_journal_membership(self, journal):

        if journal.is_member(self.collection):
            return

        journal.join(self.collection, self.user)

    def _post_save_journal(self, journal, data):
        """
        Este método existe para dados que só podem ser associados a um
        journal já persisitido, como por exemplo métodos que dependem da
        existência de um PK definido.
        """

        journal.created = data.creation_date or data.processing_date
        journal.updated = data.update_date
        self._load_journal_textlanguage(journal, data.languages)
        self._load_journal_abstractlanguage(journal, data.abstract_languages)
        self._load_journal_subject_areas(journal, data.subject_areas)
        self._load_journal_mission(journal, data.mission)
        self._load_journal_other_titles(journal, data)
        self._load_journal_status_history(journal, data.status_history)
        self._load_journal_use_license(journal, data.permissions)
        self._load_journal_sponsor(journal, data)
        self._load_journal_membership(journal)

        try:
            journal.save()
        except DatabaseError as e:
            logger.error(e.message)
            transaction.rollback()
        except IntegrityError as e:
            logger.error(e.message)
            transaction.rollback()

    @transaction.commit_on_success
    def load_journal(self, data):

        issns = set()
        issns.add(data.scielo_issn)
        issns.add(data.print_issn)
        issns.add(data.electronic_issn)

        try:
            journal = Journal.objects.get(
                Q(print_issn__in=issns) |
                Q(eletronic_issn__in=issns))
            logger.info('Journal already exists, skiping journal creation')
            return journal
        except exceptions.ObjectDoesNotExist:
            logger.info('Journal do no exists, creating journal')

        logger.info('Importing Journal (%s)' % data.title)

        journal = Journal()

        journal.creator_id = self.user.pk
        journal.collection = self.collection
        journal.scielo_issn = 'electronic' if data.scielo_issn == data.electronic_issn else 'print'
        journal.print_issn = data.print_issn or ''
        journal.eletronic_issn = data.electronic_issn or ''
        journal.title = data.title or ''
        journal.title_iso = data.abbreviated_iso_title or ''
        journal.short_title = data.abbreviated_title or ''
        journal.medline_title = data.title_nlm or ''
        journal.acronym = data.acronym
        journal.subject_descriptors = '\n'.join(data.subject_descriptors or [])
        journal.index_coverage = '\n'.join(data.subject_descriptors or [])
        journal.copyrighter = data.copyrighter or ''
        journal.init_year = data.first_year or ''
        journal.init_vol = data.first_volume or ''
        journal.init_num = data.first_number or ''
        journal.final_year = data.last_year or ''
        journal.final_vol = data.last_volume or ''
        journal.final_num = data.last_number or ''
        journal.cnn_code = data.cnn_code or ''
        journal.frequency = data.periodicity[0] if data.periodicity else ''
        journal.url_online_submission = data.submission_url or ''
        journal.url_journal = data.institutional_url or data.url() or ''
        journal.pub_status = data.current_status or ''
        journal.editorial_standard = data.editorial_standard[0] if data.editorial_standard else ''
        journal.ctrl_vocabulary = data.controlled_vocabulary[0] if data.controlled_vocabulary else ''
        journal.pub_level = data.publication_level[0] if data.publication_level else ''
        journal.secs_code = data.secs_code or ''
        journal.publisher_name = '; '.join(data.publisher_name) if data.publisher_name else ''
        journal.publisher_country = data.publisher_country[0] if data.publisher_country else ''
        journal.publisher_state = data.publisher_state or ''
        journal.publisher_city = data.publisher_city or ''
        journal.editor_address = data.editor_address or ''
        journal.editor_email = data.editor_email or ''
        journal.is_indexed_scie = data.is_indexed_in_scie
        journal.is_indexed_ssci = data.is_indexed_in_ssci
        journal.is_indexed_aehci = data.is_indexed_in_ahci

        try:
            journal.save(force_insert=True)
        except DatabaseError as e:
            logger.error(e.message)
            logger.error('Journal (%s) not imported' % (data.title))
            transaction.rollback()
            return
        except IntegrityError as e:
            logger.error(e.message)
            logger.error('Journal (%s) not imported' % (data.title))
            transaction.rollback()
            return

        self._post_save_journal(journal, data)

        logger.info('Journal (%s) created' % data.title)

        return journal

    def _load_issue_sections(self, issue, sections):

        if sections is None:
            return None

        for code, texts in sections.items():
            for language, text in texts.items():
                language = self._load_language(language)
                try:
                    section = Section.objects.get(
                        journal=issue.journal,
                        legacy_code=code,

                    )
                    sectiontitle = SectionTitle.objects.get_or_create(
                        section=section,
                        language=language,
                        title=text
                    )
                except exceptions.ObjectDoesNotExist:
                    section = Section()
                    section.legacy_code = code
                    section.journal = issue.journal
                    section.save(force_insert=True)
                    sectiontitle = SectionTitle.objects.get_or_create(
                        section=section,
                        language=language,
                        title=text
                    )

                issue.section.add(section)

    def _load_issue_titles(self, issue, titles):

        if titles is None:
            return None

        for language, title in titles.items():
            language = self._load_language(language)
            issuetitle = IssueTitle()
            issuetitle.title = title
            issuetitle.issue = issue
            issuetitle.language = language
            issuetitle.save(force_insert=True)

    def _load_issue_use_license(self, issue, permission):

        if permission is None:
            return None

        use_license = UseLicense.objects.get_or_create(
            license_code=permission['id'].upper())[0]

        if 'text' in permission and permission['text']:
            use_license.disclaimer = permission['text']

        if 'url' in permission and permission['url']:
            use_license.reference_url = permission['url']

        use_license.save()

        issue.use_license = use_license

    def _post_save_issue(self, issue, data):

        issue.order = int(data.order)
        issue.created = data.creation_date or data.processing_date
        issue.updated = data.update_date
        self._load_issue_titles(issue, data.titles)
        self._load_issue_sections(issue, data.sections)
        self._load_issue_use_license(issue, data.permissions)

        try:
            issue.save(auto_order=False)
        except DatabaseError as e:
            logger.error(e.message)
            transaction.rollback()
        except IntegrityError as e:
            transaction.rollback()
            logger.error(e.message)
            transaction.rollback()

    def _issue_exists(self, journal, data):
        spe = data.number.replace('spe', '') if data.type == 'special' else None
        suppl = ' '.join([
                data.supplement_volume or '',
                data.supplement_number or ''
            ]).strip() if data.type == 'supplement' else None
        try:
            issue = Issue.objects.get(
                journal=journal,
                publication_year=data.publication_date[:4],
                volume=data.volume or '',
                number=data.number or '',
                type=data.type,
                spe_text=spe,
                suppl_text=suppl)
            logger.info('Issue already exists, skiping issue creation')
            return issue
        except exceptions.ObjectDoesNotExist:
            logger.info('Issue do not exists, creating issue')

        return None

    @transaction.commit_on_success
    def load_issue(self, data):

        if data.type == 'ahead':
            logger.info('Issue (Ahead) will not be imported')
            return

        journal = self.load_journal(data.journal)

        if not journal:
            return

        self._load_journal_status_history(journal, data.journal.status_history)

        logger.info('Importing Issue (%s)' % (data.label))

        try:
            issue = self._issue_exists(journal, data) or Issue()
        except exceptions.MultipleObjectsReturned as e:
            logger.error('Multiple issues found this new issue will not be created')
            transaction.rollback()
            return

        spe = data.number.replace('spe', '') if data.type == 'special' else None
        suppl = ' '.join([
                data.supplement_volume or '',
                data.supplement_number or ''
            ]).strip() if data.type == 'supplement' else None

        issue.journal = journal
        issue.publication_year = data.publication_date[:4]
        issue.volume = data.volume or ''
        issue.number = data.number or ''
        issue.type = data.type
        if data.type == 'special':
            issue.number = data.number.replace('spe', '') if data.number else ''
            issue.spe_text = spe
        if data.type == 'supplement' and suppl:
            issue.suppl_text = suppl
        issue.is_press_release = data.is_press_release
        issue.total_documents = data.total_documents or 0
        issue.publication_start_month = data.start_month or 0
        issue.publication_end_month = data.end_month or 0
        issue.is_marked_up = data.is_marked_up
        issue.ctrl_vocabulary = data.controlled_vocabulary[0] if data.controlled_vocabulary else ''
        issue.editorial_standard = data.editorial_standard[0] if data.editorial_standard else ''

        try:
            issue.save(force_insert=True)
        except DatabaseError as e:
            logger.error(e.message)
            logger.error('Issue (%s) not imported' % (data.label))
            transaction.rollback()
            return
        except IntegrityError as e:
            logger.error(e.message)
            logger.error('Issue (%s) not imported' % (data.label))
            transaction.rollback()
            return

        self._post_save_issue(issue, data)

        logger.info('Issue (%s) created' % (data.label))
