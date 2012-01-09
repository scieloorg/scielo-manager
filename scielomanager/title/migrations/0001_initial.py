# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Collection'
        db.create_table('title_collection', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('manager', self.gf('django.db.models.fields.related.ForeignKey')(related_name='collection_user', to=orm['auth.User'])),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('title', ['Collection'])

        # Adding model 'UserProfile'
        db.create_table('title_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], unique=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='user_collection', to=orm['title.Collection'])),
        ))
        db.send_create_signal('title', ['UserProfile'])

        # Adding model 'Publisher'
        db.create_table('title_publisher', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='publisher_collection', to=orm['title.Collection'])),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('Address', self.gf('django.db.models.fields.TextField')()),
            ('Address_number', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('Address_complement', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('zip', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('fax', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('cel', self.gf('django.db.models.fields.CharField')(max_length=16, blank=True)),
            ('mail', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('sponsor', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('title', ['Publisher'])

        # Adding model 'Title'
        db.create_table('title_title', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='enjoy_creator', to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title_collection', to=orm['title.Collection'])),
            ('publisher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='title_publisher', to=orm['title.Publisher'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256, db_index=True)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('iso_title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
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
            ('standard', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('ctrl_vocabulary', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('literature_type', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('treatment_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('pub_level', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('secs_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('medline_code', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True)),
            ('medline_short_title', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('validated', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('title', ['Title'])

        # Adding model 'TitleMission'
        db.create_table('title_titlemission', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('title', ['TitleMission'])

        # Adding model 'TitleOtherForms'
        db.create_table('title_titleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('form_sub', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('title', ['TitleOtherForms'])

        # Adding model 'ShortTitleOtherForms'
        db.create_table('title_shorttitleotherforms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['title.Title'])),
            ('form', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('title', ['ShortTitleOtherForms'])


    def backwards(self, orm):
        
        # Deleting model 'Collection'
        db.delete_table('title_collection')

        # Deleting model 'UserProfile'
        db.delete_table('title_userprofile')

        # Deleting model 'Publisher'
        db.delete_table('title_publisher')

        # Deleting model 'Title'
        db.delete_table('title_title')

        # Deleting model 'TitleMission'
        db.delete_table('title_titlemission')

        # Deleting model 'TitleOtherForms'
        db.delete_table('title_titleotherforms')

        # Deleting model 'ShortTitleOtherForms'
        db.delete_table('title_shorttitleotherforms')


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
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'title.shorttitleotherforms': {
            'Meta': {'object_name': 'ShortTitleOtherForms'},
            'form': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['title.Title']"}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '16'})
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
            'standard': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
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
        'title.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'user_collection'", 'to': "orm['title.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['title']
