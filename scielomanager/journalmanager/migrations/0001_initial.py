# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Collection'
        db.create_table('journalmanager_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collection_user', to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['Collection'])

        # Adding model 'UserProfile'
        db.create_table('journalmanager_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_collection', to=orm['journalmanager.Collection'])),
        ))
        db.send_create_signal('journalmanager', ['UserProfile'])

        # Adding model 'Institution'
        db.create_table('journalmanager_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publisher_collection', to=orm['journalmanager.Collection'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('Address', self.gf('django.db.models.fields.TextField')()),
            ('Address_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('Address_complement', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('cel', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sponsor', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['Institution'])

        # Adding model 'Journal'
        db.create_table('journalmanager_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='journal_collection', to=orm['journalmanager.Collection'])),
            ('institution', self.gf('django.db.models.fields.related.ForeignKey')(related_name='journal_institution', to=orm['journalmanager.Institution'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('scielo_issn', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('print_issn', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('eletronic_issn', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('subject_descriptors', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('study_area', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('indexation_range', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('init_year', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('init_vol', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('init_num', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('final_year', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('final_vol', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('final_num', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('pub_status', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('alphabet', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('national_code', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('text_language', self.gf('django.db.models.fields.CharField')(max_length=259, blank=True)),
            ('abst_language', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('literature_type', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('treatment_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('pub_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('secs_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('journalmanager', ['Journal'])

        # Adding model 'JournalMission'
        db.create_table('journalmanager_journalmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('journalmanager', ['JournalMission'])

        # Adding model 'JournalTitleOtherForms'
        db.create_table('journalmanager_journaltitleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('form_sub', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
        ))
        db.send_create_signal('journalmanager', ['JournalTitleOtherForms'])

        # Adding model 'JournalShortTitleOtherForms'
        db.create_table('journalmanager_journalshorttitleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
        ))
        db.send_create_signal('journalmanager', ['JournalShortTitleOtherForms'])

        # Adding model 'UseLicense'
        db.create_table('journalmanager_uselicense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('license_code', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('reference_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('disclaimer', self.gf('django.db.models.fields.TextField')(max_length=512)),
        ))
        db.send_create_signal('journalmanager', ['UseLicense'])

        # Adding model 'Section'
        db.create_table('journalmanager_section', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Section'])

        # Adding model 'Issue'
        db.create_table('journalmanager_issue', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'], null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
            ('volume', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('is_press_release', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('creation_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('publication_date', self.gf('django.db.models.fields.DateField')()),
            ('is_available', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_marked_up', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('bibliographic_strip', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('use_license', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.UseLicense'])),
            ('publisher_fullname', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('total_documents', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Issue'])

        # Adding M2M table for field section on 'Issue'
        db.create_table('journalmanager_issue_section', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('issue', models.ForeignKey(orm['journalmanager.issue'], null=False)),
            ('section', models.ForeignKey(orm['journalmanager.section'], null=False))
        ))
        db.create_unique('journalmanager_issue_section', ['issue_id', 'section_id'])

        # Adding model 'Supplement'
        db.create_table('journalmanager_supplement', (
            ('issue_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['journalmanager.Issue'], unique=True, primary_key=True)),
            ('suppl_label', self.gf('django.db.models.fields.CharField')(max_length=256, null=True, blank=True)),
        ))
        db.send_create_signal('journalmanager', ['Supplement'])


    def backwards(self, orm):
        
        # Deleting model 'Collection'
        db.delete_table('journalmanager_collection')

        # Deleting model 'UserProfile'
        db.delete_table('journalmanager_userprofile')

        # Deleting model 'Institution'
        db.delete_table('journalmanager_institution')

        # Deleting model 'Journal'
        db.delete_table('journalmanager_journal')

        # Deleting model 'JournalMission'
        db.delete_table('journalmanager_journalmission')

        # Deleting model 'JournalTitleOtherForms'
        db.delete_table('journalmanager_journaltitleotherforms')

        # Deleting model 'JournalShortTitleOtherForms'
        db.delete_table('journalmanager_journalshorttitleotherforms')

        # Deleting model 'UseLicense'
        db.delete_table('journalmanager_uselicense')

        # Deleting model 'Section'
        db.delete_table('journalmanager_section')

        # Deleting model 'Issue'
        db.delete_table('journalmanager_issue')

        # Removing M2M table for field section on 'Issue'
        db.delete_table('journalmanager_issue_section')

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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_user'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'journalmanager.institution': {
            'Address': ('django.db.models.fields.TextField', [], {}),
            'Address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'Address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'ordering': "['name', 'sponsor']", 'object_name': 'Institution'},
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publisher_collection'", 'to': "orm['journalmanager.Collection']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'sponsor': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.issue': {
            'Meta': {'object_name': 'Issue'},
            'bibliographic_strip': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_marked_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_press_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']", 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher_fullname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Section']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_documents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.journal': {
            'Meta': {'ordering': "['title']", 'object_name': 'Journal'},
            'abst_language': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'alphabet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_collection'", 'to': "orm['journalmanager.Collection']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enjoy_creator'", 'to': "orm['auth.User']"}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'eletronic_issn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'final_num': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'final_vol': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'final_year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'indexation_range': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'init_num': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'init_vol': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'init_year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_institution'", 'to': "orm['journalmanager.Institution']"}),
            'literature_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'scielo_issn': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'secs_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'study_area': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'subject_descriptors': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'text_language': ('django.db.models.fields.CharField', [], {'max_length': '259', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'treatment_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'journalmanager.journalmission': {
            'Meta': {'object_name': 'JournalMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'journalmanager.journalshorttitleotherforms': {
            'Meta': {'object_name': 'JournalShortTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'title_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'journalmanager.journaltitleotherforms': {
            'Meta': {'object_name': 'JournalTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'form_sub': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'title_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'journalmanager.section': {
            'Meta': {'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'journalmanager.supplement': {
            'Meta': {'object_name': 'Supplement', '_ormbases': ['journalmanager.Issue']},
            'issue_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Issue']", 'unique': 'True', 'primary_key': 'True'}),
            'suppl_label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.uselicense': {
            'Meta': {'object_name': 'UseLicense'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'journalmanager.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_collection'", 'to': "orm['journalmanager.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['journalmanager']
