# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Status'
        db.create_table('articletrack_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articletrack.Attempt'])),
            ('phase', self.gf('django.db.models.fields.CharField')(default='upload', max_length=32)),
            ('is_accomplished', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('changed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('articletrack', ['Status'])

        # Adding model 'Attempt'
        db.create_table('articletrack_attempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checkin_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=32)),
            ('articlepkg_id', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('collection', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['journalmanager.Collection'])),
            ('article_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('journal_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('issue_label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pkgmeta_filename', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pkgmeta_md5', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pkgmeta_filesize', self.gf('django.db.models.fields.IntegerField')()),
            ('pkgmeta_filecount', self.gf('django.db.models.fields.IntegerField')()),
            ('pkgmeta_submitter', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('closed_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
        ))
        db.send_create_signal('articletrack', ['Attempt'])


    def backwards(self, orm):
        
        # Deleting model 'Status'
        db.delete_table('articletrack_status')

        # Deleting model 'Attempt'
        db.delete_table('articletrack_attempt')


    models = {
        'articletrack.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'article_title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'articlepkg_id': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'checkin_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'closed_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'journal_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'pkgmeta_filecount': ('django.db.models.fields.IntegerField', [], {}),
            'pkgmeta_filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pkgmeta_filesize': ('django.db.models.fields.IntegerField', [], {}),
            'pkgmeta_md5': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pkgmeta_submitter': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'articletrack.status': {
            'Meta': {'object_name': 'Status'},
            'attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articletrack.Attempt']"}),
            'changed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_accomplished': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'phase': ('django.db.models.fields.CharField', [], {'default': "'upload'", 'max_length': '32'})
        },
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
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'name_slug': ('django.db.models.fields.SlugField', [], {'db_index': 'True', 'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.usercollections': {
            'Meta': {'unique_together': "(('user', 'collection'),)", 'object_name': 'UserCollections'},
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.Collection']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_manager': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['articletrack']
