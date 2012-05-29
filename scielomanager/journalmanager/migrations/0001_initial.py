# encoding: utf-8
import datetime
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
            ('email', self.gf('django.db.models.fields.EmailField')(unique=True, max_length=75)),
        ))
        db.send_create_signal('journalmanager', ['UserProfile'])

        # Adding model 'Collection'
        db.create_table('journalmanager_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
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
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
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

        # Adding model 'Institution'
        db.create_table('journalmanager_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
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
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('journalmanager', ['Institution'])

        # Adding model 'Publisher'
        db.create_table('journalmanager_publisher', (
            ('institution_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.Institution'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('journalmanager', ['Publisher'])

        # Adding M2M table for field collections on 'Publisher'
        db.create_table('journalmanager_publisher_collections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('publisher', models.ForeignKey(orm['journalmanager.publisher'], null=False)),
            ('collection', models.ForeignKey(orm['journalmanager.collection'], null=False))
        ))
        db.create_unique('journalmanager_publisher_collections', ['publisher_id', 'collection_id'])

        # Adding model 'Sponsor'
        db.create_table('journalmanager_sponsor', (
            ('institution_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.Institution'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('journalmanager', ['Sponsor'])

        # Adding M2M table for field collections on 'Sponsor'
        db.create_table('journalmanager_sponsor_collections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sponsor', models.ForeignKey(orm['journalmanager.sponsor'], null=False)),
            ('collection', models.ForeignKey(orm['journalmanager.collection'], null=False))
        ))
        db.create_unique('journalmanager_sponsor_collections', ['sponsor_id', 'collection_id'])

        # Adding model 'Journal'
        db.create_table('journalmanager_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('previous_title', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='prev_title', null=True, to=orm['journalmanager.Journal'])),
            ('use_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.UseLicense'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('title_iso', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('scielo_issn', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('print_issn', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('eletronic_issn', self.gf('django.db.models.fields.CharField')(max_length=9)),
            ('subject_descriptors', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('init_year', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('init_vol', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('init_num', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('final_year', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('final_vol', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('final_num', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('pub_status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pub_level', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('secs_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('copyrighter', self.gf('django.db.models.fields.CharField')(max_length=254)),
            ('url_online_submission', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('url_journal', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(max_length=254, null=True, blank=True)),
            ('index_coverage', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Journal'])

        # Adding M2M table for field publisher on 'Journal'
        db.create_table('journalmanager_journal_publisher', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('publisher', models.ForeignKey(orm['journalmanager.publisher'], null=False))
        ))
        db.create_unique('journalmanager_journal_publisher', ['journal_id', 'publisher_id'])

        # Adding M2M table for field sponsor on 'Journal'
        db.create_table('journalmanager_journal_sponsor', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('sponsor', models.ForeignKey(orm['journalmanager.sponsor'], null=False))
        ))
        db.create_unique('journalmanager_journal_sponsor', ['journal_id', 'sponsor_id'])

        # Adding M2M table for field collections on 'Journal'
        db.create_table('journalmanager_journal_collections', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('collection', models.ForeignKey(orm['journalmanager.collection'], null=False))
        ))
        db.create_unique('journalmanager_journal_collections', ['journal_id', 'collection_id'])

        # Adding M2M table for field languages on 'Journal'
        db.create_table('journalmanager_journal_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False)),
            ('language', models.ForeignKey(orm['journalmanager.language'], null=False))
        ))
        db.create_unique('journalmanager_journal_languages', ['journal_id', 'language_id'])

        # Adding model 'JournalPublicationEvents'
        db.create_table('journalmanager_journalpublicationevents', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['JournalPublicationEvents'])

        # Adding model 'JournalStudyArea'
        db.create_table('journalmanager_journalstudyarea', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('study_area', self.gf('django.db.models.fields.CharField')(max_length=256)),
        ))
        db.send_create_signal('journalmanager', ['JournalStudyArea'])

        # Adding model 'JournalTitle'
        db.create_table('journalmanager_journaltitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('journalmanager', ['JournalTitle'])

        # Adding model 'JournalMission'
        db.create_table('journalmanager_journalmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
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
            ('section', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Section'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'])),
        ))
        db.send_create_signal('journalmanager', ['SectionTitle'])

        # Adding model 'Section'
        db.create_table('journalmanager_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('journalmanager', ['Section'])

        # Adding model 'Issue'
        db.create_table('journalmanager_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('is_press_release', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateField')()),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('is_marked_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('use_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.UseLicense'], null=True)),
            ('publisher_fullname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('total_documents', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('cover', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Issue'])

        # Adding M2M table for field section on 'Issue'
        db.create_table('journalmanager_issue_section', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['journalmanager.issue'], null=False)),
            ('section', models.ForeignKey(orm['journalmanager.section'], null=False))
        ))
        db.create_unique('journalmanager_issue_section', ['issue_id', 'section_id'])

        # Adding model 'IssueTitle'
        db.create_table('journalmanager_issuetitle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('issue', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Issue'])),
            ('language', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Language'], null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('journalmanager', ['IssueTitle'])

        # Adding model 'Supplement'
        db.create_table('journalmanager_supplement', (
            ('issue_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.Issue'], unique=True, primary_key=True)),
            ('suppl_label', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Supplement'])


    def backwards(self, orm):
        
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

        # Deleting model 'Publisher'
        db.delete_table('journalmanager_publisher')

        # Removing M2M table for field collections on 'Publisher'
        db.delete_table('journalmanager_publisher_collections')

        # Deleting model 'Sponsor'
        db.delete_table('journalmanager_sponsor')

        # Removing M2M table for field collections on 'Sponsor'
        db.delete_table('journalmanager_sponsor_collections')

        # Deleting model 'Journal'
        db.delete_table('journalmanager_journal')

        # Removing M2M table for field publisher on 'Journal'
        db.delete_table('journalmanager_journal_publisher')

        # Removing M2M table for field sponsor on 'Journal'
        db.delete_table('journalmanager_journal_sponsor')

        # Removing M2M table for field collections on 'Journal'
        db.delete_table('journalmanager_journal_collections')

        # Removing M2M table for field languages on 'Journal'
        db.delete_table('journalmanager_journal_languages')

        # Deleting model 'JournalPublicationEvents'
        db.delete_table('journalmanager_journalpublicationevents')

        # Deleting model 'JournalStudyArea'
        db.delete_table('journalmanager_journalstudyarea')

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
        db.delete_table('journalmanager_issue_section')

        # Deleting model 'IssueTitle'
        db.delete_table('journalmanager_issuetitle')

        # Deleting model 'Supplement'
        db.delete_table('journalmanager_supplement')


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
        'journalmanager.collection': {
            'Meta': {'ordering': "['name']", 'object_name': 'Collection'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'user_collection'", 'to': "orm['auth.User']", 'through': "orm['journalmanager.UserCollections']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.issue': {
            'Meta': {'object_name': 'Issue'},
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_marked_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_press_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher_fullname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'section': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Section']", 'symmetrical': 'False'}),
            'total_documents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']", 'null': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'journalmanager.issuetitle': {
            'Meta': {'object_name': 'IssueTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Issue']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']", 'null': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'journalmanager.journal': {
            'Meta': {'ordering': "['title']", 'object_name': 'Journal'},
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'symmetrical': 'False'}),
            'copyrighter': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enjoy_creator'", 'to': "orm['auth.User']"}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'eletronic_issn': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'final_num': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'final_vol': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'final_year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_coverage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'init_num': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'init_vol': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'init_year': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Language']", 'symmetrical': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'previous_title': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prev_title'", 'null': 'True', 'to': "orm['journalmanager.Journal']"}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'publisher': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'journal_institution'", 'symmetrical': 'False', 'to': "orm['journalmanager.Publisher']"}),
            'scielo_issn': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'secs_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'db_index': 'True'}),
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'journal_sponsor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['journalmanager.Sponsor']"}),
            'subject_descriptors': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'title_iso': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_journal': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'url_online_submission': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']"}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'journalmanager.journalmission': {
            'Meta': {'object_name': 'JournalMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']", 'null': 'True'})
        },
        'journalmanager.journalpublicationevents': {
            'Meta': {'object_name': 'JournalPublicationEvents'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'journalmanager.journalstudyarea': {
            'Meta': {'object_name': 'JournalStudyArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'study_area': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.journaltitle': {
            'Meta': {'object_name': 'JournalTitle'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'journalmanager.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'journalmanager.publisher': {
            'Meta': {'ordering': "['name']", 'object_name': 'Publisher', '_ormbases': ['journalmanager.Institution']},
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'symmetrical': 'False'}),
            'institution_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Institution']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.section': {
            'Meta': {'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'journalmanager.sectiontitle': {
            'Meta': {'object_name': 'SectionTitle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Language']"}),
            'section': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Section']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor', '_ormbases': ['journalmanager.Institution']},
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'symmetrical': 'False'}),
            'institution_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Institution']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.supplement': {
            'Meta': {'object_name': 'Supplement', '_ormbases': ['journalmanager.Issue']},
            'issue_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Issue']", 'unique': 'True', 'primary_key': 'True'}),
            'suppl_label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'object_name': 'UseLicense'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.usercollections': {
            'Meta': {'object_name': 'UserCollections'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'journalmanager.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['journalmanager']
