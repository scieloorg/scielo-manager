# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding index on 'Event', fields ['end_at']
        db.create_index('maintenancewindow_event', ['end_at'])

        # Adding index on 'Event', fields ['is_blocking_users']
        db.create_index('maintenancewindow_event', ['is_blocking_users'])


    def backwards(self, orm):
        
        # Removing index on 'Event', fields ['is_blocking_users']
        db.delete_index('maintenancewindow_event', ['is_blocking_users'])

        # Removing index on 'Event', fields ['end_at']
        db.delete_index('maintenancewindow_event', ['end_at'])


    models = {
        'maintenancewindow.event': {
            'Meta': {'ordering': "['begin_at', 'title']", 'object_name': 'Event'},
            'begin_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'event_report': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blocking_users': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['maintenancewindow']
