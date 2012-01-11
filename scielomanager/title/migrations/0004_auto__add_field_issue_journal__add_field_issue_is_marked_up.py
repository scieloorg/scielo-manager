# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Issue.journal'
        db.add_column('title_issue', 'journal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'], null=True), keep_default=False)

        # Adding field 'Issue.is_marked_up'
        db.add_column('title_issue', 'is_marked_up', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Deleting field 'Issue.journal'
        db.delete_column('title_issue', 'journal_id')

        # Deleting field 'Issue.is_marked_up'
        db.delete_column('title_issue', 'is_marked_up')


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
            'journal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']", 'null': 'True'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'publication_date': ('django.db.models.fields.DateField', [], {}),
            'publisher_fullname': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'section': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['title.Section']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.UseLicense']"}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'title.publisher': {
            'Address': ('django.db.models.fields.TextField', [], {}),
            'Address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'Address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'Meta': {'ordering': "['name', 'sponsor']", 'object_name': 'Publisher'},
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
        'title.section': {
            'Meta': {'object_name': 'Section'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'creation_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'update_date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'title.shorttitleotherforms': {
            'Meta': {'object_name': 'ShortTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'title.supplement': {
            'Meta': {'object_name': 'Supplement', '_ormbases': ['title.Issue']},
            'issue_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['title.Issue']", 'unique': 'True', 'primary_key': 'True'}),
            'suppl_label': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'})
        },
        'title.title': {
            'Meta': {'ordering': "['title']", 'object_name': 'Title'},
            'abst_language': ('django.db.models.fields.CharField', [], {'max_length': '256', 'blank': 'True'}),
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'alphabet': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'classification': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title_collection'", 'to': "orm['title.Collection']"}),
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
            'iso_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'literature_type': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'medline_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'medline_short_title': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'title_publisher'", 'to': "orm['title.Publisher']"}),
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
        'title.titlemission': {
            'Meta': {'object_name': 'TitleMission'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']"})
        },
        'title.titleotherforms': {
            'Meta': {'object_name': 'TitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'form_sub': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
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
