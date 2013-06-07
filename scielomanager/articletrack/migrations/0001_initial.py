# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Attempt'
        db.create_table('articletrack_attempt', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('checking_id', self.gf('django.db.models.fields.IntegerField')()),
            ('articlepkg_id', self.gf('django.db.models.fields.IntegerField')()),
            ('collection_uri', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('article_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('journal_title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('issue_label', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('pkgmeta_filename', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pkgmeta_md5', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('pkgmeta_filesize', self.gf('django.db.models.fields.IntegerField')()),
            ('pkgmeta_filecount', self.gf('django.db.models.fields.IntegerField')()),
            ('pkgmeta_submitter', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('articletrack', ['Attempt'])

        # Adding model 'Status'
        db.create_table('articletrack_status', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('attempt', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['articletrack.Attempt'])),
            ('accomplished', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('articletrack', ['Status'])


    def backwards(self, orm):
        
        # Deleting model 'Attempt'
        db.delete_table('articletrack_attempt')

        # Deleting model 'Status'
        db.delete_table('articletrack_status')


    models = {
        'articletrack.attempt': {
            'Meta': {'object_name': 'Attempt'},
            'article_title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'articlepkg_id': ('django.db.models.fields.IntegerField', [], {}),
            'checking_id': ('django.db.models.fields.IntegerField', [], {}),
            'collection_uri': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_label': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'journal_title': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pkgmeta_filecount': ('django.db.models.fields.IntegerField', [], {}),
            'pkgmeta_filename': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pkgmeta_filesize': ('django.db.models.fields.IntegerField', [], {}),
            'pkgmeta_md5': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'pkgmeta_submitter': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'articletrack.status': {
            'Meta': {'object_name': 'Status'},
            'accomplished': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'attempt': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articletrack.Attempt']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['articletrack']
