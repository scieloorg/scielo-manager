# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table('maintenancewindow_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('begin_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_at', self.gf('django.db.models.fields.DateTimeField')(db_index=True)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('is_blocking_users', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('is_finished', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('event_report', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('maintenancewindow', ['Event'])


    def backwards(self, orm):
        # Deleting model 'Event'
        db.delete_table('maintenancewindow_event')


    models = {
        'maintenancewindow.event': {
            'Meta': {'ordering': "['begin_at', 'title']", 'object_name': 'Event'},
            'begin_at': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'end_at': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'event_report': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_blocking_users': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_finished': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['maintenancewindow']