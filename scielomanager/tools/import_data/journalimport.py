#!/usr/bin/env python
#coding: utf-8
import json
import os
import subfield
import datetime
from datetime import date

from django.core.management import setup_environ
from django.core import exceptions

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

from journalmanager.models import *


class JournalImport:

    def __init__(self):
        self._publishers_pool = []
        self._sponsors_pool = []
        self._summary = {}
        self.trans_pub_status = {'c': 'current',
            'd': 'deceased',
            's': 'suspended',
            '?': 'inprogress',
            }

    def iso_format(self, dates, string='-'):
        day = dates[6:8]
        if day == "00":
            day = "01"

        month = dates[4:6]
        if month == "00":
            month = "01"

        dateformated = "%s-%s-%s" % (dates[0:4], month,day)

        return dateformated

    def charge_summary(self, attribute):
        """
        Function: charge_summary
        Carrega com +1 cada atributo passado para o metodo, se o attributo nao existir ele e criado.
        """
        if not self._summary.has_key(attribute):
            self._summary[attribute] = 0

        self._summary[attribute] += 1

    def have_similar_sponsors(self, match_string):
        """
        Function: have_similar_sponsors
        Identifica se existe instituicao ja registrada com o mesmo nome, com o objetivo de filtrar
        instituticoes duplicadas.
        Retorna o id da instituicao se houver uma cadastrada com o mesmo nome, caso contrario Retorna
        False.
        """
        sponsor_id = ""

        if len(self._sponsors_pool) > 0:
            for inst in self._sponsors_pool:
                if inst["match_string"] == match_string:
                    sponsor_id = inst["id"]
                    break
                else:
                    sponsor_id = False
        else:
            sponsor_id = False

        return sponsor_id

    def load_sponsor(self, collection, record):
        """
        Function: load_sponsor
        Retorna um objeto Sponsor() caso a gravação do mesmo em banco de dados for concluida
        """

        sponsor = Sponsor()

        # Sponsors Import
        if not record.has_key('140'):
            return []

        sponsor.name = record['140'][0]

        match_string=sponsor.name.strip()

        similar_key =  self.have_similar_sponsors(match_string)

        loaded_sponsor=""

        if similar_key != False:
            similar_sponsor=Sponsor.objects.get(id=similar_key)
            self.charge_summary("sponsors_duplication_fix")
            loaded_sponsor = similar_sponsor
        else:
            sponsor.save(force_insert=True)
            sponsor.collections.add(collection)
            self.charge_summary("sponsors")
            loaded_sponsor = sponsor
            self._sponsors_pool.append(dict({"id":sponsor.id,"match_string":match_string.strip()}))

        return [loaded_sponsor,]

    def load_studyarea(self, journal, areas):

        for i in areas:
            try:
                studyarea = StudyArea.objects.get(study_area=i)
                journal.study_areas.add(studyarea)
                self.charge_summary("studyarea")
            except:
                self.charge_summary("studyarea_{0}_notdefined".format(i))

    def load_textlanguage(self, journal, langs):

        from sectionimport import LANG_DICT as lang_dict
        for i in langs:
            language = Language.objects.get_or_create(iso_code = i, name = lang_dict.get(i, '###NOT FOUND###'))[0]

            journal.languages.add(language)
            self.charge_summary("language_%s" % i)

    def load_abstractlanguage(self, journal, langs):

        from sectionimport import LANG_DICT as lang_dict
        for i in langs:
            language = Language.objects.get_or_create(iso_code = i, name = lang_dict.get(i, '###NOT FOUND###'))[0]

            journal.abstract_keyword_languages.add(language)
            self.charge_summary("language_%s" % i)

    def load_mission(self, journal, missions):
        from sectionimport import LANG_DICT as lang_dict

        for i in missions:
            parsed_subfields = subfield.CompositeField(subfield.expand(i))
            mission = JournalMission()
            try:
                language = Language.objects.get_or_create(iso_code = parsed_subfields['l'], name = lang_dict.get(parsed_subfields['l'], '###NOT FOUND###'))[0]
                mission.language = language
            except:
                pass
            mission.description = parsed_subfields['_']
            journal.missions.add(mission)
            self.charge_summary("mission")

    def load_historic(self, collection, journal, historicals):

        lifecycles = {}

        for i in historicals:
            expanded = subfield.expand(i)
            parsed_subfields = dict(expanded)
            try:
                lifecycles[self.iso_format(parsed_subfields['a'])] = parsed_subfields['b']
            except KeyError:
                self.charge_summary("history_error_field")

            try:
                lifecycles[self.iso_format(parsed_subfields['c'])] = parsed_subfields['d']
            except KeyError:
                self.charge_summary("history_error_field")

        for cyclekey, cyclevalue in iter(sorted(lifecycles.iteritems())):
            try:
                journalhist = JournalPublicationEvents()

                # If journal doesnt have history set ''inprogress''
                journalhist.status = self.trans_pub_status.get(cyclevalue.lower(), 'inprogress')

                journalhist.changed_by_id = 1
                journalhist.save()

                journalhist.created_at = cyclekey
                journalhist.save()

                self.charge_summary("publication_events")
            except exceptions.ValidationError:
                # If date is invalid: set the ``created_at`` to now and promove the journal to ``inprogress`` status
                journalhist.status = 'inprogress'
                journalhist.created_at = datetime.datetime.now()
            finally:
                journalhist.save()  # Updating to real date, once when saving the model is given a automatica value

                # Create a third entity StatusParty
                sparty = StatusParty()
                sparty.publication_status = journalhist
                sparty.collection = collection
                sparty.journal = journal
                sparty.save()

        return True

    def get_last_status(self, historicals):

        lifecycles = {}

        for i in historicals:
            expanded = subfield.expand(i)
            parsed_subfields = dict(expanded)
            try:
                lifecycles[self.iso_format(parsed_subfields['a'])] = parsed_subfields['b']
            except KeyError:
                self.charge_summary("history_error_field")

            try:
                lifecycles[self.iso_format(parsed_subfields['c'])] = parsed_subfields['d']
            except KeyError:
                self.charge_summary("history_error_field")

        return sorted(lifecycles.iteritems())[-1][1]

    def load_title(self, journal, titles, category):

        for i in titles:
            title = JournalTitle()
            title.title = i
            title.category = category
            journal.other_titles.add(title)
            self.charge_summary("title")

    def load_use_license(self, code, disclaimer):

        expanded_disclaimer = subfield.expand(disclaimer)
        parsed_subfields_disclaimer = dict(expanded_disclaimer)

        use_license = UseLicense.objects.get_or_create(license_code=code)[0]

        if parsed_subfields_disclaimer.has_key('t'):
            use_license.disclaimer = parsed_subfields_disclaimer['t']

        use_license.save()

        return use_license

    def load_journal(self, collection, loaded_sponsor, record):
        """
        Function: load_journal
        Retorna um objeto journal() caso a gravação do mesmo em banco de dados for concluida
        """

        issn_type = ""
        print_issn = ""
        electronic_issn = ""

        # Creating use license codes.
        license_code = ""
        license_disclaimer = ""

        if '541' in record:
            license_code = record['541'][0]

        if '540' in record:
            license_disclaimer = record['540'][0]

        use_license = self.load_use_license(license_code, license_disclaimer)

        journal = Journal()

        # ISSN and Other Complex Stuffs from the old version
        if not '935' in record:  # Old fashion ISSN persistance style
            if record['35'][0] == "PRINT":
                issn_type = "print"
                print_issn = record['400'][0]
            else:
                issn_type = "electronic"
                electronic_issn = record['400'][0]
        else:  # New ISSN persistance style
            if '35' in record:
                if record['35'][0] == "PRINT":
                    issn_type = "print"
                    print_issn = record['935'][0]
                    if record['935'][0] != record['400'][0]:
                        issn_type = "electronic"
                        electronic_issn = record['400'][0]
                else:
                    issn_type = "electronic"
                    electronic_issn = record['935'][0]
                    if record['935'][0] != record['400'][0]:
                        issn_type = "print"
                        print_issn = record['400'][0]

        journal.scielo_issn = issn_type
        journal.print_issn = print_issn
        journal.eletronic_issn = electronic_issn

        # Journal Original Title
        journal.title = record['100'][0]

        # Short Title
        journal.short_title = record['150'][0]

        # Acronym
        journal.acronym = record['930'][0]

        # Use License
        journal.use_license = use_license

        # Subject Descriptors
        if '440' in record:
            journal.subject_descriptors = '\n'.join(record['440']).lower()

        # Indexing Coverage
        if '450' in record:
            journal.index_coverage = '\n'.join(record['450']).lower()

        # Copyright
        if '62' in record:
            journal.copyrighter = record['62'][0]

        # Initial Year
        if '301' in record:
            journal.init_year = record['301'][0][0:4]

        # Initial Volume
        if '302' in record:
            journal.init_vol = record['302'][0]

        # Initial Number
        if '303' in record:
            journal.init_num = record['303'][0]

        # Final Year
        if '304' in record:
            journal.final_year = record['304'][0][0:4]

        # Final Volumen
        if '305' in record:
            journal.final_vol = record['305'][0]

        # Final Number
        if '306' in record:
            journal.final_num = record['306'][0]

        # National Code
        if '20' in record:
            journal.national_code = record['20'][0]

        # Publication Frequency
        if '380' in record:
            journal.frequency = record['380'][0]

        if '692' in record:
            journal.url_online_submission = record['692'][0]

        if '69' in record:
            journal.url_journal = record['69'][0]

        if '51' in record:
            journal.pub_status = self.trans_pub_status.get(self.get_last_status(record['51']).lower(), 'inprogress')

        if '340' in record:
            journal.alphabet = record['340'][0]

        if '20' in record:
            journal.national_code = record['20'][0]

        if '117' in record:
            journal.editorial_standard = record['117'][0]

        if '85' in record:
            journal.ctrl_vocabulary = record['85'][0]

        if '5' in record:
            journal.literature_type = record['5'][0]

        if '6' in record:
            journal.treatment_level = record['6'][0]

        if '330' in record:
            journal.pub_level = record['330'][0]

        if '37' in record:
            journal.secs_code = record['37'][0]

        if '151' in record:
            journal.title_iso = record['151'][0]

        if '310' in record:
            journal.publisher_country = record['310'][0]

        if '320' in record:
            journal.publisher_state = record['320'][0]

        if '480' in record:
            journal.publisher_name = record['480'][0]

        if '490' in record:
            journal.publication_city = record['490'][0]

        if '63' in record:
            journal.editor_address = ", ".join(record['63']).replace('<br>', '')

        if '64' in record:
            journal.editor_email = record['64'][0]

        journal.pub_status_changed_by_id = 1
        journal.creator_id = 1

        journal.save(force_insert=True)

        self.charge_summary("journals")

        journal.sponsor = loaded_sponsor

        # created date
        if '940' in record:
            journal.created = self.iso_format(record['940'][0])

        # updated date
        if '941' in record:
            journal.updated = self.iso_format(record['941'][0])

        # text language
        if '350' in record:
            self.load_textlanguage(journal, record['350'])

        # abstract language
        if '360' in record:
            self.load_abstractlanguage(journal, record['360'])

        # study area
        if '441' in record:
            self.load_studyarea(journal, record['441'])

        # mission
        if '901' in record:
            self.load_mission(journal, record['901'])

        # historic - JournalPublicationEvents
        if '51' in record:
            self.load_historic(collection, journal, record['51'])

        # titles
        if '421' in record:
            self.load_title(journal, record['421'], 'other')

        if '240' in record:
            self.load_title(journal, record['240'], 'other')

        if '230' in record:
            self.load_title(journal, record['230'], 'paralleltitle')

        journal.save()

        return journal

    def try_update_previous_title(self, json_file, collection):
        """
        Field 710 is the next journal title.
        This function get the previous journal by title and update the previous
        title of next journal set in the 710 field.
        """
        for record in json_file:
            if '710' in record:

                previous_journal = Journal.objects.filter(title__exact=record['100'][0],
                                                          collections__in=[collection]).distinct()
                if previous_journal:
                    Journal.objects.filter(title__exact=record['710'][0],
                                           collections__in=[collection]).distinct().update(
                                           previous_title=previous_journal[0].id)
                else:
                    print "Not possible to update the previous title of the journal"

    def run_import(self, json_file, collection):
        """
        Function: run_import
        Dispara processo de importacao de dados
        """
        json_parsed = {}

        json_file = open(json_file, 'r')
        json_parsed = json.loads(json_file.read())

        for record in json_parsed:
            loaded_sponsor = self.load_sponsor(collection, record)
            self.load_journal(collection, loaded_sponsor, record)

        # Try to update the previous title
        self.try_update_previous_title(json_parsed, collection)

        # Cleaning data
        JournalPublicationEvents.objects.filter(created_at__month=date.today().month, created_at__year=date.today().year).delete()

    def get_summary(self):
        """
        Function: get_summary
        Retorna o resumo de carga de registros
        """
        return self._summary
