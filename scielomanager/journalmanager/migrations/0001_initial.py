# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('journalmanager_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('iso_code', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
        ))
        db.send_create_signal('journalmanager', ['Language'])

        # Adding model 'UserProfile'
        db.create_table('journalmanager_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('email_notifications', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tz', self.gf('django.db.models.fields.CharField')(default='America/Sao_Paulo', max_length=150)),
        ))
        db.send_create_signal('journalmanager', ['UserProfile'])

        # Adding model 'Collection'
        db.create_table('journalmanager_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('name_slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True, null=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('logo', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=16, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('address_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('address_complement', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
        ))
        db.send_create_signal('journalmanager', ['Collection'])

        # Adding model 'UserCollections'
        db.create_table('journalmanager_usercollections', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Collection'])),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_manager', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['UserCollections'])

        # Adding unique constraint on 'UserCollections', fields ['user', 'collection']
        db.create_unique('journalmanager_usercollections', ['user_id', 'collection_id'])

        # Adding model 'Institution'
        db.create_table('journalmanager_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('complement', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=16, blank=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('address_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('address_complement', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('cel', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('is_trashed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('journalmanager', ['Institution'])

        # Adding model 'Sponsor'
        db.create_table('journalmanager_sponsor', (
            ('institution_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.Institution'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('journalmanager', ['Sponsor'])

        # Adding M2M table for field collections on 'Sponsor'
        m2m_table_name = db.shorten_name('journalmanager_sponsor_collections')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sponsor', models.ForeignKey(orm['journalmanager.sponsor'], null=False)),
            ('collection', models.ForeignKey(orm['journalmanager.collection'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sponsor_id', 'collection_id'])

        # Adding model 'SubjectCategory'
        db.create_table('journalmanager_subjectcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
        ))
        db.send_create_signal('journalmanager', ['SubjectCategory'])

        # Adding model 'StudyArea'
        db.create_table('journalmanager_studyarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('study_area', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('journalmanager', ['StudyArea'])

        # Adding model 'Journal'
        db.create_table('journalmanager_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='editor_journal', null=True, to=orm['auth.User'])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('previous_title', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='prev_title', null=True, to=orm['journalmanager.Journal'])),
            ('use_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.UseLicense'])),
            ('national_code', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('current_ahead_documents', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3, null=True, blank=True)),
            ('previous_ahead_documents', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=3, null=True, blank=True)),
            ('twitter_user', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('title_iso', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('scielo_issn', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('print_issn', self.gf('django.db.models.fields.CharField')(max_length=9, db_index=True)),
            ('eletronic_issn', self.gf('django.db.models.fields.CharField')(max_length=9, db_index=True)),
            ('subject_descriptors', self.gf('django.db.models.fields.CharField')(max_length=1024)),
            ('init_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('init_vol', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('init_num', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('final_year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('final_vol', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('final_num', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('medline_title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('medline_code', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pub_level', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('secs_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('copyrighter', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('url_online_submission', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('url_journal', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=254, null=True, blank=True)),
            ('index_coverage', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cover', self.gf('scielomanager.custom_fields.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('logo', self.gf('scielomanager.custom_fields.ContentTypeRestrictedFileField')(max_length=100, null=True, blank=True)),
            ('is_trashed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('other_previous_title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('editor_name', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('editor_address', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('editor_address_city', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('editor_address_state', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('editor_address_zip', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('editor_address_country', self.gf('scielo_extensions.modelfields.CountryField')(max_length=2)),
            ('editor_phone1', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('editor_phone2', self.gf('django.db.models.fields.CharField')(max_length=32, null=True, blank=True)),
            ('editor_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('publisher_name', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('publisher_country', self.gf('scielo_extensions.modelfields.CountryField')(max_length=2)),
            ('publisher_state', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('publication_city', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('is_indexed_scie', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_indexed_ssci', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_indexed_aehci', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['Journal'])

        # Adding M2M table for field sponsor on 'Journal'
        m2m_table_name = db.shorten_name('journalmanager_journal_sponsor')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('sponsor', models.ForeignKey(orm['journalmanager.sponsor'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_id', 'sponsor_id'])

        # Adding M2M table for field languages on 'Journal'
        m2m_table_name = db.shorten_name('journalmanager_journal_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('language', models.ForeignKey(orm['journalmanager.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_id', 'language_id'])

        # Adding M2M table for field abstract_keyword_languages on 'Journal'
        m2m_table_name = db.shorten_name('journalmanager_journal_abstract_keyword_languages')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('language', models.ForeignKey(orm['journalmanager.language'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_id', 'language_id'])

        # Adding M2M table for field subject_categories on 'Journal'
        m2m_table_name = db.shorten_name('journalmanager_journal_subject_categories')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('subjectcategory', models.ForeignKey(orm['journalmanager.subjectcategory'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_id', 'subjectcategory_id'])

        # Adding M2M table for field study_areas on 'Journal'
        m2m_table_name = db.shorten_name('journalmanager_journal_study_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('studyarea', models.ForeignKey(orm['journalmanager.studyarea'], null=False))
        ))
        db.create_unique(m2m_table_name, ['journal_id', 'studyarea_id'])

        # Adding model 'Membership'
        db.create_table('journalmanager_membership', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Collection'])),
            ('status', self.gf('django.db.models.fields.CharField')(default='inprogress', max_length=16)),
            ('since', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('reason', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('journalmanager', ['Membership'])

        # Adding unique constraint on 'Membership', fields ['journal', 'collection']
        db.create_unique('journalmanager_membership', ['journal_id', 'collection_id'])

        # Adding model 'JournalTimeline'
        db.create_table('journalmanager_journaltimeline', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='statuses', to=orm['journalmanager.Journal'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Collection'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('since', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.TextField')(default='')),
            ('created_by', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('journalmanager', ['JournalTimeline'])

        # Adding model 'JournalTitle'
        db.create_table('journalmanager_journaltitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='other_titles', to=orm['journalmanager.Journal'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('journalmanager', ['JournalTitle'])

        # Adding model 'JournalMission'
        db.create_table('journalmanager_journalmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='missions', to=orm['journalmanager.Journal'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'], null=True)),
        ))
        db.send_create_signal('journalmanager', ['JournalMission'])

        # Adding model 'UseLicense'
        db.create_table('journalmanager_uselicense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('license_code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('reference_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('disclaimer', self.gf('django.db.models.fields.TextField')(max_length=512, null=True, blank=True)),
            ('is_default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['UseLicense'])

        # Adding model 'TranslatedData'
        db.create_table('journalmanager_translateddata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('translation', self.gf('django.db.models.fields.CharField')(max_length=512, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('model', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('journalmanager', ['TranslatedData'])

        # Adding model 'SectionTitle'
        db.create_table('journalmanager_sectiontitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(related_name='titles', to=orm['journalmanager.Section'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'])),
        ))
        db.send_create_signal('journalmanager', ['SectionTitle'])

        # Adding model 'Section'
        db.create_table('journalmanager_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=21, blank=True)),
            ('legacy_code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_trashed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal('journalmanager', ['Section'])

        # Adding model 'Issue'
        db.create_table('journalmanager_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publication_start_month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('publication_end_month', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('publication_year', self.gf('django.db.models.fields.IntegerField')()),
            ('is_marked_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.UseLicense'], null=True)),
            ('total_documents', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('is_trashed', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('label', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=64, null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')(blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(default='regular', max_length=15)),
            ('suppl_text', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
            ('spe_text', self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Issue'])

        # Adding M2M table for field section on 'Issue'
        m2m_table_name = db.shorten_name('journalmanager_issue_section')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['journalmanager.issue'], null=False)),
            ('section', models.ForeignKey(orm['journalmanager.section'], null=False))
        ))
        db.create_unique(m2m_table_name, ['issue_id', 'section_id'])

        # Adding model 'IssueTitle'
        db.create_table('journalmanager_issuetitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Issue'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('journalmanager', ['IssueTitle'])

        # Adding model 'PendedForm'
        db.create_table('journalmanager_pendedform', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('view_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('form_hash', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pending_forms', to=orm['auth.User'])),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['PendedForm'])

        # Adding model 'PendedValue'
        db.create_table('journalmanager_pendedvalue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.related.ForeignKey')(related_name='data', to=orm['journalmanager.PendedForm'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('value', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('journalmanager', ['PendedValue'])

        # Adding model 'DataChangeEvent'
        db.create_table('journalmanager_datachangeevent', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('event_type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Collection'])),
        ))
        db.send_create_signal('journalmanager', ['DataChangeEvent'])

        # Adding model 'PressRelease'
        db.create_table('journalmanager_pressrelease', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('doi', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['PressRelease'])

        # Adding model 'PressReleaseTranslation'
        db.create_table('journalmanager_pressreleasetranslation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('press_release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='translations', to=orm['journalmanager.PressRelease'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('journalmanager', ['PressReleaseTranslation'])

        # Adding model 'PressReleaseArticle'
        db.create_table('journalmanager_pressreleasearticle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('press_release', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['journalmanager.PressRelease'])),
            ('article_pid', self.gf('django.db.models.fields.CharField')(max_length=32, db_index=True)),
        ))
        db.send_create_signal('journalmanager', ['PressReleaseArticle'])

        # Adding model 'RegularPressRelease'
        db.create_table('journalmanager_regularpressrelease', (
            ('pressrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.PressRelease'], unique=True, primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='press_releases', to=orm['journalmanager.Issue'])),
        ))
        db.send_create_signal('journalmanager', ['RegularPressRelease'])

        # Adding model 'AheadPressRelease'
        db.create_table('journalmanager_aheadpressrelease', (
            ('pressrelease_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.PressRelease'], unique=True, primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(related_name='press_releases', to=orm['journalmanager.Journal'])),
        ))
        db.send_create_signal('journalmanager', ['AheadPressRelease'])

        # Adding model 'Article'
        db.create_table('journalmanager_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['journalmanager.Issue'])),
            ('front', self.gf('jsonfield.fields.JSONField')()),
            ('xml_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('pdf_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('images_url', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('journalmanager', ['Article'])


    def backwards(self, orm):
        # Removing unique constraint on 'Membership', fields ['journal', 'collection']
        db.delete_unique('journalmanager_membership', ['journal_id', 'collection_id'])

        # Removing unique constraint on 'UserCollections', fields ['user', 'collection']
        db.delete_unique('journalmanager_usercollections', ['user_id', 'collection_id'])

        # Deleting model 'Language'
        db.delete_table('journalmanager_language')

        # Deleting model 'UserProfile'
        db.delete_table('journalmanager_userprofile')

        # Deleting model 'Collection'
        db.delete_table('journalmanager_collection')

        # Deleting model 'UserCollections'
        db.delete_table('journalmanager_usercollections')

        # Deleting model 'Institution'
        db.delete_table('journalmanager_institution')

        # Deleting model 'Sponsor'
        db.delete_table('journalmanager_sponsor')

        # Removing M2M table for field collections on 'Sponsor'
        db.delete_table(db.shorten_name('journalmanager_sponsor_collections'))

        # Deleting model 'SubjectCategory'
        db.delete_table('journalmanager_subjectcategory')

        # Deleting model 'StudyArea'
        db.delete_table('journalmanager_studyarea')

        # Deleting model 'Journal'
        db.delete_table('journalmanager_journal')

        # Removing M2M table for field sponsor on 'Journal'
        db.delete_table(db.shorten_name('journalmanager_journal_sponsor'))

        # Removing M2M table for field languages on 'Journal'
        db.delete_table(db.shorten_name('journalmanager_journal_languages'))

        # Removing M2M table for field abstract_keyword_languages on 'Journal'
        db.delete_table(db.shorten_name('journalmanager_journal_abstract_keyword_languages'))

        # Removing M2M table for field subject_categories on 'Journal'
        db.delete_table(db.shorten_name('journalmanager_journal_subject_categories'))

        # Removing M2M table for field study_areas on 'Journal'
        db.delete_table(db.shorten_name('journalmanager_journal_study_areas'))

        # Deleting model 'Membership'
        db.delete_table('journalmanager_membership')

        # Deleting model 'JournalTimeline'
        db.delete_table('journalmanager_journaltimeline')

        # Deleting model 'JournalTitle'
        db.delete_table('journalmanager_journaltitle')

        # Deleting model 'JournalMission'
        db.delete_table('journalmanager_journalmission')

        # Deleting model 'UseLicense'
        db.delete_table('journalmanager_uselicense')

        # Deleting model 'TranslatedData'
        db.delete_table('journalmanager_translateddata')

        # Deleting model 'SectionTitle'
        db.delete_table('journalmanager_sectiontitle')

        # Deleting model 'Section'
        db.delete_table('journalmanager_section')

        # Deleting model 'Issue'
        db.delete_table('journalmanager_issue')

        # Removing M2M table for field section on 'Issue'
        db.delete_table(db.shorten_name('journalmanager_issue_section'))

        # Deleting model 'IssueTitle'
        db.delete_table('journalmanager_issuetitle')

        # Deleting model 'PendedForm'
        db.delete_table('journalmanager_pendedform')

        # Deleting model 'PendedValue'
        db.delete_table('journalmanager_pendedvalue')

        # Deleting model 'DataChangeEvent'
        db.delete_table('journalmanager_datachangeevent')

        # Deleting model 'PressRelease'
        db.delete_table('journalmanager_pressrelease')

        # Deleting model 'PressReleaseTranslation'
        db.delete_table('journalmanager_pressreleasetranslation')

        # Deleting model 'PressReleaseArticle'
        db.delete_table('journalmanager_pressreleasearticle')

        # Deleting model 'RegularPressRelease'
        db.delete_table('journalmanager_regularpressrelease')

        # Deleting model 'AheadPressRelease'
        db.delete_table('journalmanager_aheadpressrelease')

        # Deleting model 'Article'
        db.delete_table('journalmanager_article')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'journalmanager.aheadpressrelease': {
            'Meta': {'object_name': 'AheadPressRelease', '_ormbases': ['journalmanager.PressRelease']},
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'press_releases'", 'to': "orm['journalmanager.Journal']"}),
            'pressrelease_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.PressRelease']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.article': {
            'Meta': {'object_name': 'Article'},
            'front': ('jsonfield.fields.JSONField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['journalmanager.Issue']"}),
            'pdf_url': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'xml_url': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.collection': {
            'Meta': {'ordering': "['name']", 'object_name': 'Collection'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_collection'", 'to': "orm['auth.User']", 'through': "orm['journalmanager.UserCollections']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.datachangeevent': {
            'Meta': {'object_name': 'DataChangeEvent'},
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'event_type': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'journalmanager.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'complement': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.issue': {
            'Meta': {'ordering': "('created', 'id')", 'object_name': 'Issue'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_marked_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'label': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'order': ('django.db.models.fields.IntegerField', [], {'blank': 'True'}),
            'publication_end_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publication_start_month': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'publication_year': ('django.db.models.fields.IntegerField', [], {}),
            'section': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Section']", 'symmetrical': 'False', 'blank': 'True'}),
            'spe_text': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'suppl_text': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'total_documents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'regular'", 'max_length': '15'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']", 'null': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'})
        },
        'journalmanager.issuetitle': {
            'Meta': {'object_name': 'IssueTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Issue']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.journal': {
            'Meta': {'ordering': "('title', 'id')", 'object_name': 'Journal'},
            'abstract_keyword_languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'abstract_keyword_languages'", 'symmetrical': 'False', 'to': "orm['journalmanager.Language']"}),
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'through': "orm['journalmanager.Membership']", 'symmetrical': 'False'}),
            'copyrighter': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'cover': ('scielomanager.custom_fields.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enjoy_creator'", 'to': "orm['auth.User']"}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'current_ahead_documents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'editor_journal'", 'null': 'True', 'to': "orm['auth.User']"}),
            'editor_address': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'editor_address_city': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'editor_address_country': ('scielo_extensions.modelfields.CountryField', [], {'max_length': '2'}),
            'editor_address_state': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'editor_address_zip': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'editor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'editor_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'editor_phone1': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'editor_phone2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'eletronic_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_index': 'True'}),
            'final_num': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'final_vol': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'final_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_coverage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'init_num': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'init_vol': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'init_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'is_indexed_aehci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_indexed_scie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_indexed_ssci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Language']", 'symmetrical': 'False'}),
            'logo': ('scielomanager.custom_fields.ContentTypeRestrictedFileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medline_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'medline_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'other_previous_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'previous_ahead_documents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'previous_title': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prev_title'", 'null': 'True', 'to': "orm['journalmanager.Journal']"}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_index': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'publication_city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'publisher_country': ('scielo_extensions.modelfields.CountryField', [], {'max_length': '2'}),
            'publisher_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'publisher_state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scielo_issn': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'secs_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'db_index': 'True'}),
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'journal_sponsor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['journalmanager.Sponsor']"}),
            'study_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'journals_migration_tmp'", 'null': 'True', 'to': "orm['journalmanager.StudyArea']"}),
            'subject_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'journals'", 'null': 'True', 'to': "orm['journalmanager.SubjectCategory']"}),
            'subject_descriptors': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'title_iso': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'twitter_user': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_journal': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'url_online_submission': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']"})
        },
        'journalmanager.journalmission': {
            'Meta': {'object_name': 'JournalMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'missions'", 'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']", 'null': 'True'})
        },
        'journalmanager.journaltimeline': {
            'Meta': {'object_name': 'JournalTimeline'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'statuses'", 'to': "orm['journalmanager.Journal']"}),
            'reason': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'since': ('django.db.models.fields.DateTimeField', [], {}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'journalmanager.journaltitle': {
            'Meta': {'object_name': 'JournalTitle'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'other_titles'", 'to': "orm['journalmanager.Journal']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'journalmanager.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'journalmanager.membership': {
            'Meta': {'unique_together': "(('journal', 'collection'),)", 'object_name': 'Membership'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'since': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'inprogress'", 'max_length': '16'})
        },
        'journalmanager.pendedform': {
            'Meta': {'object_name': 'PendedForm'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'form_hash': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pending_forms'", 'to': "orm['auth.User']"}),
            'view_name': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'journalmanager.pendedvalue': {
            'Meta': {'object_name': 'PendedValue'},
            'form': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'data'", 'to': "orm['journalmanager.PendedForm']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'journalmanager.pressrelease': {
            'Meta': {'object_name': 'PressRelease'},
            'doi': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'journalmanager.pressreleasearticle': {
            'Meta': {'object_name': 'PressReleaseArticle'},
            'article_pid': ('django.db.models.fields.CharField', [], {'max_length': '32', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'press_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['journalmanager.PressRelease']"})
        },
        'journalmanager.pressreleasetranslation': {
            'Meta': {'object_name': 'PressReleaseTranslation'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']"}),
            'press_release': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'to': "orm['journalmanager.PressRelease']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'journalmanager.regularpressrelease': {
            'Meta': {'object_name': 'RegularPressRelease', '_ormbases': ['journalmanager.PressRelease']},
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'press_releases'", 'to': "orm['journalmanager.Issue']"}),
            'pressrelease_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.PressRelease']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.section': {
            'Meta': {'ordering': "('id',)", 'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '21', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'legacy_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'journalmanager.sectiontitle': {
            'Meta': {'ordering': "['title']", 'object_name': 'SectionTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'titles'", 'to': "orm['journalmanager.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor', '_ormbases': ['journalmanager.Institution']},
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'symmetrical': 'False'}),
            'institution_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Institution']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.studyarea': {
            'Meta': {'object_name': 'StudyArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'study_area': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.subjectcategory': {
            'Meta': {'object_name': 'SubjectCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        },
        'journalmanager.translateddata': {
            'Meta': {'object_name': 'TranslatedData'},
            'field': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'translation': ('django.db.models.fields.CharField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.uselicense': {
            'Meta': {'ordering': "['license_code']", 'object_name': 'UseLicense'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'license_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.usercollections': {
            'Meta': {'unique_together': "(('user', 'collection'),)", 'object_name': 'UserCollections'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'journalmanager.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email_notifications': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tz': ('django.db.models.fields.CharField', [], {'default': "'America/Sao_Paulo'", 'max_length': '150'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['journalmanager']