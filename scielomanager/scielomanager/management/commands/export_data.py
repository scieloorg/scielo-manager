# coding: utf-8
"""Exportação dos dados para JSON, salvos em arquivo"""
import os
import json
import logging
import sys
from optparse import make_option

from django.core import serializers
from django.core.management.base import BaseCommand, CommandError
from django.db.models import ForeignKey

from journalmanager import choices
from journalmanager.models import (
    Collection,
    Journal,
    Issue,
    Membership,
    Institution,
    Sponsor,
    JournalTimeline,
    UseLicense,
    SectionTitle,
    Section,
    Language,
)
from editorialmanager.models import (
    EditorialBoard,
    EditorialMember,
    RoleType,
    RoleTypeTranslation,
)


LOGGER = logging.getLogger(__name__)


JOURNALS_ATTRS = (
    ('section_set', 'journals_sections.json', 'Seções dos periódicos'),
    (
        'press_releases',
        'journals_aheadpressreleases.json',
        'Ahead Press Releases dos periódicos'
    ),
    ('other_titles', 'journals_titles.json', 'Títulos dos periódicos'),
    ('missions', 'journals_missions.json', 'Missões dos periódicos'),
    (
        'subject_categories',
        'journals_subjectcategories.json',
        'Áreas temáticas dos periódicos',
    ),
    (
        'study_areas',
        'journals_studyarea.json',
        'Áreas de Conhecimento dos periódicos',
    ),
)


ISSUES_ATTRS = (
    (
        'section',
        'issues_sections.json',
        'Seções dos Fascículos'
    ),
    (
        'press_releases',
        'issues_regularpressreleases.json',
        'Press Releases Regulares dos Fascículos'
    ),
    (
        'issuetitle_set',
        'issues_titles.json',
        'Títulos dos Fascículos'
    ),
)


class Command(BaseCommand):
    help = 'Export data to files in JSON format.'
    option_list = BaseCommand.option_list + (
        make_option(
            '-c','--collection',
            action="store",
            type="string",
            dest="collection_slugname",
            help='Collection slug name to export, e.g., saude-publica'),
        make_option(
            '-o','--output',
            action="store",
            type="string",
            default="json",
            help='Output path. Default is ./json/'),
        make_option(
            '-l','--loglevel',
            action="store",
            type="choice",
            choices=["DEBUG", "INFO", "WARNING", "ERROR"],
            default="INFO",
            help='Log level. Default is INFO'),
        )

    def handle(self, *args, **options):
        if not options.get('collection_slugname'):
            raise CommandError('Collection is mandatory')

        LOGGER.setLevel(options['loglevel'])
        self.json_base_path = options['output']
        self.resolve_json_path()
        self.json_serializer = serializers.get_serializer('json')()
        self.export_data(options['collection_slugname'])
        self.export_choices()

    def resolve_json_path(self):
        if not os.path.exists(self.json_base_path):
            try:
                os.makedirs(self.json_base_path)
            except os.error:
                error_msg = "ERRO ao criar diretório %s" % self.json_base_path
                raise CommandError(error_msg)

    def export_model(self, model, json_filename, filter, ordered_by, msg):
        model_objects = model.objects.filter(**filter)
        if model_objects:
            if ordered_by:
                model_objects = model_objects.order_by(ordered_by)
            with open(os.path.join(self.json_base_path, json_filename), 'w') as fp:
                LOGGER.info("Salvando %s: %d" % (msg, len(model_objects)))
                self.json_serializer.serialize(model_objects, stream=fp)
        return model_objects

    def export_model_attr(self, queryset, attrib, json_filename, msg):
        try:
            objects = list({
                attr_object
                for query_obj in queryset
                for attr_object in getattr(query_obj, attrib).all()
            })
        except AttributeError as exc:
            LOGGER.error("ERRO %s: %s" % (msg, str(exc)))
        else:
            with open(os.path.join(self.json_base_path, json_filename), 'w') as fp:
                LOGGER.info("Salvando %s: %d" % (msg, len(objects)))
                self.json_serializer.serialize(objects, stream=fp)

    def export_collection_data(self, collection_slugname):
        query = self.export_model(
            Collection,
            'collection.json',
            {'name_slug': collection_slugname},
            None,
            'Coleção %s' % collection_slugname
        )
        if not query:
            raise CommandError('Collection %s not found' % collection_slugname)
        return query[0]

    def export_journals_data(self, collection):
        journals = self.export_model(
            Journal, 'journals.json', {'collections': collection}, None, 'Periódicos',
        )
        for journals_attr in JOURNALS_ATTRS:
            self.export_model_attr(journals, *journals_attr)
        return journals

    def export_issues_data(self, journals):
        issues = self.export_model(
            Issue, 'issues.json', {'journal__in': journals}, None, 'Fascículos',
        )
        for issues_attr in ISSUES_ATTRS:
            self.export_model_attr(issues, *issues_attr)
        return issues

    def export_editorial_boards_data(self, issues):
        editorial_boards = self.export_model(
            EditorialBoard,
            'editorial_boards.json',
            {'issue__in': issues},
            'issue',
            'Equipe editorial dos fascículos',
        )
        self.export_model_attr(
            editorial_boards,
            'editorialmember_set',
            'editorial_members.json',
            'Membros da equipe editorial dos fascículos',
        )
        return editorial_boards

    def export_collection_membership(self, collection):
        self.export_model(
            Membership,
            'membership.json',
            {'collection': collection},
            None,
            'Dados dos periódicos na coleção'
        )

    def export_collection_sponsors(self, collection):
        self.export_model(
            Institution,
            'collection_sponsors.json',
            {
                'pk__in': [
                    sponsor.pk
                    for sponsor in Sponsor.objects.filter(
                        collections=collection)
                ]
            },
            None,
            'Patrocinadores da coleção',
        )

    def export_collection_journals_timelines(self, collection):
        self.export_model(
            JournalTimeline,
            'journals_timelines.json',
            {'collection': collection},
            'journal',
            'Timelines dos periódicos'
        )

    def export_journals_sponsors(self, journals):
        self.export_model(
            Institution,
            'journals_sponsors.json',
            {
                'pk__in': [
                    sponsor.pk
                    for sponsor in Sponsor.objects.select_related().filter(
                        journal_sponsor__in=journals)
                ]
            },
            None,
            'Patrocinadores dos periódicos',
        )

    def export_journals_use_licenses(self, journals):
        self.export_model(
            UseLicense,
            'journals_use_license.json',
            {'pk__in': [journal.use_license.pk for journal in journals]},
            None,
            'Licenças de uso dos periódicos',
        )

    def export_journals_sections_titles(self, journals):
        self.export_model(
            SectionTitle,
            'journals_sectiontitles.json',
            {
                'section__in': [
                    journal_section
                    for journal_section in Section.objects.filter(
                        journal__in=journals)
                ]
            },
            'section',
            'Títulos de Seções dos periódicos'
        )

    def export_issues_sections_titles(self, issues):
        self.export_model(
            SectionTitle,
            'issues_sectiontitles.json',
            {
                'pk__in': list({
                    title.pk
                    for issue in issues
                    for issue_section in issue.section.all()
                    for title in issue_section.titles.all()
                })
            },
            'section',
            'Títulos de Seções dos fascículos'
        )

    def export_data(self, collection_slugname):
        collection = self.export_collection_data(collection_slugname)
        if not collection:
            raise CommandError('No collection found')

        models_args = [
            (
                Language,
                'languages.json',
                {},
                None,
                'Idiomas',
            ),
        ]

        self.export_collection_sponsors(collection)
        journals = self.export_journals_data(collection)
        if journals:
            issues = self.export_issues_data(journals)
            editorial_boards = self.export_editorial_boards_data(issues)
            self.export_collection_membership(collection)
            self.export_collection_journals_timelines(collection)
            self.export_journals_sponsors(journals)
            self.export_journals_use_licenses(journals)
            self.export_journals_sections_titles(journals)
            self.export_issues_sections_titles(issues)
            if editorial_boards:
                models_args = models_args + [
                    (
                        RoleType,
                        'editorial_roletype.json',
                        {},
                        None,
                        'Cargos Editoriais',
                    ),
                    (
                        RoleTypeTranslation,
                        'editorial_roletypetranslation.json',
                        {},
                        None,
                        'Traduções de Cargos Editoriais',
                    ),
                ]
        for model_args in models_args:
            self.export_model(*model_args)

    def export_choices(self):
        json_choices = {
            choice: {
                key: str(value)
                for key, value in getattr(choices, choice)
            }
            for choice in dir(choices) if choice.isupper()
        }
        with open(os.path.join(self.json_base_path, 'choices.json'), 'w') as fp:
            LOGGER.info("Salvando choices")
            json.dump(json_choices, fp)
    