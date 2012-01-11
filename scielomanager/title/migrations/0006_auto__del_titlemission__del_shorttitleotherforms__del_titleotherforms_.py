# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting model 'TitleMission'
        db.delete_table('title_titlemission')

        # Deleting model 'ShortTitleOtherForms'
        db.delete_table('title_shorttitleotherforms')

        # Deleting model 'TitleOtherForms'
        db.delete_table('title_titleotherforms')

        # Deleting model 'Title'
        db.delete_table('title_title')

        # Deleting model 'Publisher'
        db.delete_table('title_publisher')

        # Adding model 'Journal'
        db.create_table('title_journal', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='journal_collection', to=orm['title.Collection'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='journal_institution', to=orm['title.Institution'])),
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
        db.send_create_signal('title', ['Journal'])

        # Adding model 'JournalTitleOtherForms'
        db.create_table('title_journaltitleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Journal'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('form_sub', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
        ))
        db.send_create_signal('title', ['JournalTitleOtherForms'])

        # Adding model 'JournalMission'
        db.create_table('title_journalmission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Journal'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('title', ['JournalMission'])

        # Adding model 'JournalShortTitleOtherForms'
        db.create_table('title_journalshorttitleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Journal'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True)),
        ))
        db.send_create_signal('title', ['JournalShortTitleOtherForms'])

        # Adding model 'Institution'
        db.create_table('title_institution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publisher_collection', to=orm['title.Collection'])),
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
        db.send_create_signal('title', ['Institution'])

        # Changing field 'Issue.journal'
        db.alter_column('title_issue', 'journal_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Journal'], null=True))


    def backwards(self, orm):
        
        # Adding model 'TitleMission'
        db.create_table('title_titlemission', (
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('title', ['TitleMission'])

        # Adding model 'ShortTitleOtherForms'
        db.create_table('title_shorttitleotherforms', (
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
        ))
        db.send_create_signal('title', ['ShortTitleOtherForms'])

        # Adding model 'TitleOtherForms'
        db.create_table('title_titleotherforms', (
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('form_sub', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('title', ['TitleOtherForms'])

        # Adding model 'Title'
        db.create_table('title_title', (
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('study_area', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('text_language', self.gf('django.db.models.fields.CharField')(max_length=259, blank=True)),
            ('classification', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('acronym', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('national_code', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title_publisher', to=orm['title.Publisher'])),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title_collection', to=orm['title.Collection'])),
            ('treatment_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('frequency', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('indexation_range', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('final_num', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('medline_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('eletronic_issn', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('init_num', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('init_vol', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('iso_title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('literature_type', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('abst_language', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('alphabet', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('final_vol', self.gf('django.db.models.fields.CharField')(max_length=4, blank=True)),
            ('medline_short_title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('final_year', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('editorial_standard', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('subject_descriptors', self.gf('django.db.models.fields.CharField')(max_length=256, blank=True)),
            ('scielo_issn', self.gf('django.db.models.fields.CharField')(max_length=8, blank=True)),
            ('pub_status', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('secs_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('init_year', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('print_issn', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('pub_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
        ))
        db.send_create_signal('title', ['Title'])

        # Adding model 'Publisher'
        db.create_table('title_publisher', (
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('Address_complement', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('Address_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('cel', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=16, null=True, blank=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publisher_collection', to=orm['title.Collection'])),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('sponsor', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('Address', self.gf('django.db.models.fields.TextField')()),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
        ))
        db.send_create_signal('title', ['Publisher'])

        # Deleting model 'Journal'
        db.delete_table('title_journal')

        # Deleting model 'JournalTitleOtherForms'
        db.delete_table('title_journaltitleotherforms')

        # Deleting model 'JournalMission'
        db.delete_table('title_journalmission')

        # Deleting model 'JournalShortTitleOtherForms'
        db.delete_table('title_journalshorttitleotherforms')

        # Deleting model 'Institution'
        db.delete_table('title_institution')

        # Changing field 'Issue.journal'
        db.alter_column('title_issue', 'journal_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'], null=True))


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
        'title.collection': {
            'Meta': {'ordering': "['name']", 'object_name': 'Collection'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'manager': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collection_user'", 'to': "orm['auth.User']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'title.institution': {
            'Address': ('django.db.models.fields.TextField', [], {}),
            'Address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'Address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'ordering': "['name', 'sponsor']", 'object_name': 'Institution'},
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publisher_collection'", 'to': "orm['title.Collection']"}),
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
        'title.issue': {
            'Meta': {'object_name': 'Issue'},
            'bibliographic_strip': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_available': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_marked_up': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_press_release': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Journal']", 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher_fullname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['title.Section']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'total_documents': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.UseLicense']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'title.journal': {
            'Meta': {'ordering': "['title']", 'object_name': 'Journal'},
            'abst_language': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'alphabet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_collection'", 'to': "orm['title.Collection']"}),
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
            'literature_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_institution'", 'to': "orm['title.Institution']"}),
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
        'title.journalmission': {
            'Meta': {'object_name': 'JournalMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Journal']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'title.journalshorttitleotherforms': {
            'Meta': {'object_name': 'JournalShortTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Journal']"}),
            'title_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'title.journaltitleotherforms': {
            'Meta': {'object_name': 'JournalTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'form_sub': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Journal']"}),
            'title_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'title.section': {
            'Meta': {'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'title.supplement': {
            'Meta': {'object_name': 'Supplement', '_ormbases': ['title.Issue']},
            'issue_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['title.Issue']", 'unique': 'True', 'primary_key': 'True'}),
            'suppl_label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'title.uselicense': {
            'Meta': {'object_name': 'UseLicense'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'max_length': '512'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_code': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'title.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_collection'", 'to': "orm['title.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['title']
