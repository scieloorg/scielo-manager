# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'JournalHist'
        db.create_table('journalmanager_journalhist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('d', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('status', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('journalmanager', ['JournalHist'])

        # Adding model 'JournalParallelTitles'
        db.create_table('journalmanager_journalparalleltitles', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Journal'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('journalmanager', ['JournalParallelTitles'])

        # Adding field 'Journal.copyrighter'
        db.add_column('journalmanager_journal', 'copyrighter', self.gf('django.db.models.fields.CharField')(max_length=254, null=True, blank=True), keep_default=False)

        # Adding field 'Journal.url_submission'
        db.add_column('journalmanager_journal', 'url_submission', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True), keep_default=False)

        # Adding field 'Journal.url_journal'
        db.add_column('journalmanager_journal', 'url_journal', self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True), keep_default=False)

        # Adding field 'Journal.notes'
        db.add_column('journalmanager_journal', 'notes', self.gf('django.db.models.fields.CharField')(max_length=256, null=True), keep_default=False)

        # Deleting field 'Collection.manager'
        db.delete_column('journalmanager_collection', 'manager_id')

        # Changing field 'IndexingCoverage.database_acronym'
        db.alter_column('journalmanager_indexingcoverage', 'database_acronym', self.gf('django.db.models.fields.CharField')(max_length=16, null=True))

        # Deleting field 'JournalTitleOtherForms.title_type'
        db.delete_column('journalmanager_journaltitleotherforms', 'title_type')

        # Deleting field 'JournalTitleOtherForms.form_sub'
        db.delete_column('journalmanager_journaltitleotherforms', 'form_sub')

        # Adding field 'UserProfile.is_manager'
        db.add_column('journalmanager_userprofile', 'is_manager', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting model 'JournalHist'
        db.delete_table('journalmanager_journalhist')

        # Deleting model 'JournalParallelTitles'
        db.delete_table('journalmanager_journalparalleltitles')

        # Deleting field 'Journal.copyrighter'
        db.delete_column('journalmanager_journal', 'copyrighter')

        # Deleting field 'Journal.url_submission'
        db.delete_column('journalmanager_journal', 'url_submission')

        # Deleting field 'Journal.url_journal'
        db.delete_column('journalmanager_journal', 'url_journal')

        # Deleting field 'Journal.notes'
        db.delete_column('journalmanager_journal', 'notes')

        # User chose to not deal with backwards NULL issues for 'Collection.manager'
        raise RuntimeError("Cannot reverse this migration. 'Collection.manager' and its values cannot be restored.")

        # Changing field 'IndexingCoverage.database_acronym'
        db.alter_column('journalmanager_indexingcoverage', 'database_acronym', self.gf('django.db.models.fields.CharField')(default='', max_length=16))

        # Adding field 'JournalTitleOtherForms.title_type'
        db.add_column('journalmanager_journaltitleotherforms', 'title_type', self.gf('django.db.models.fields.CharField')(max_length=16, null=True), keep_default=False)

        # User chose to not deal with backwards NULL issues for 'JournalTitleOtherForms.form_sub'
        raise RuntimeError("Cannot reverse this migration. 'JournalTitleOtherForms.form_sub' and its values cannot be restored.")

        # Deleting field 'UserProfile.is_manager'
        db.delete_column('journalmanager_userprofile', 'is_manager')


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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'journalmanager.indexingcoverage': {
            'Meta': {'object_name': 'IndexingCoverage'},
            'database_acronym': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'database_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'journalmanager.institution': {
            'Address': ('django.db.models.fields.TextField', [], {}),
            'Address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'Address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'publisher_collection'", 'to': "orm['journalmanager.Collection']"}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mail': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
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
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'alphabet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_collection'", 'to': "orm['journalmanager.Collection']"}),
            'copyrighter': ('django.db.models.fields.CharField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
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
            'indexing_coverage': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.IndexingCoverage']", 'symmetrical': 'False'}),
            'init_num': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'init_vol': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'}),
            'init_year': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'institution': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journal_institution'", 'to': "orm['journalmanager.Institution']"}),
            'literature_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'notes': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'scielo_issn': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'secs_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'study_area': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'subject_descriptors': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'treatment_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'url_journal': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'url_submission': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'validated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'journalmanager.journalabstrlanguage': {
            'Meta': {'object_name': 'JournalAbstrLanguage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'})
        },
        'journalmanager.journalhist': {
            'Meta': {'object_name': 'JournalHist'},
            'd': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'journalmanager.journalmission': {
            'Meta': {'object_name': 'JournalMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'journalmanager.journalparalleltitles': {
            'Meta': {'object_name': 'JournalParallelTitles'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"})
        },
        'journalmanager.journalshorttitleotherforms': {
            'Meta': {'object_name': 'JournalShortTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'title_type': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True'})
        },
        'journalmanager.journaltextlanguage': {
            'Meta': {'object_name': 'JournalTextLanguage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'journalmanager.journaltitleotherforms': {
            'Meta': {'object_name': 'JournalTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Journal']"})
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
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['journalmanager']
