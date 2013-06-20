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
            ('collection_uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
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
            'collection_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
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
        }
    }

    complete_apps = ['articletrack']
