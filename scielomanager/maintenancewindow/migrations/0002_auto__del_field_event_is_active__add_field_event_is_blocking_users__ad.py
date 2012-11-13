# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Event.is_active'
        db.delete_column('maintenancewindow_event', 'is_active')

        # Adding field 'Event.is_blocking_users'
        db.add_column('maintenancewindow_event', 'is_blocking_users', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Event.is_finished'
        db.add_column('maintenancewindow_event', 'is_finished', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Adding field 'Event.event_report'
        db.add_column('maintenancewindow_event', 'event_report', self.gf('django.db.models.fields.TextField')(default=False), keep_default=False)


    def backwards(self, orm):
        
        # Adding field 'Event.is_active'
        db.add_column('maintenancewindow_event', 'is_active', self.gf('django.db.models.fields.BooleanField')(default=False), keep_default=False)

        # Deleting field 'Event.is_blocking_users'
        db.delete_column('maintenancewindow_event', 'is_blocking_users')

        # Deleting field 'Event.is_finished'
        db.delete_column('maintenancewindow_event', 'is_finished')

        # Deleting field 'Event.event_report'
        db.delete_column('maintenancewindow_event', 'event_report')


    models = {
        'maintenancewindow.event': {
            'Meta': {'ordering': "['begin_at', 'title']", 'object_name': 'Event'},
            'begin_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {}),
            'event_report': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blocking_users': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['maintenancewindow']
