# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ticket'
        db.create_table('articletrack_ticket', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('started_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('finished_at', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tickets', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('article', self.gf('django.db.models.fields.related.ForeignKey')(related_name='articles', to=orm['articletrack.Article'])),
        ))
        db.send_create_signal('articletrack', ['Ticket'])

        # Adding model 'Comment'
        db.create_table('articletrack_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments_author', to=orm['auth.User'])),
            ('ticket', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['articletrack.Ticket'])),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('articletrack', ['Comment'])

        # Adding model 'Article'
        db.create_table('articletrack_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('article_title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('articlepkg_ref', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('journal_title', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('issue_label', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pissn', self.gf('django.db.models.fields.CharField')(default='', max_length=9)),
            ('eissn', self.gf('django.db.models.fields.CharField')(default='', max_length=9)),
        ))
        db.send_create_signal('articletrack', ['Article'])

        # Adding M2M table for field journals on 'Article'
        m2m_table_name = db.shorten_name('articletrack_article_journals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('article', models.ForeignKey(orm['articletrack.article'], null=False)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['article_id', 'journal_id'])

        # Deleting field 'Checkin.issue_label'
        db.delete_column('articletrack_checkin', 'issue_label')

        # Deleting field 'Checkin.journal_title'
        db.delete_column('articletrack_checkin', 'journal_title')

        # Deleting field 'Checkin.pissn'
        db.delete_column('articletrack_checkin', 'pissn')

        # Deleting field 'Checkin.eissn'
        db.delete_column('articletrack_checkin', 'eissn')

        # Deleting field 'Checkin.article_title'
        db.delete_column('articletrack_checkin', 'article_title')

        # Deleting field 'Checkin.articlepkg_ref'
        db.delete_column('articletrack_checkin', 'articlepkg_ref')

        # Adding field 'Checkin.article'
        db.add_column('articletrack_checkin', 'article',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='checkins', null=True, to=orm['articletrack.Article']),
                      keep_default=False)

        # Removing M2M table for field journals on 'Checkin'
        db.delete_table(db.shorten_name('articletrack_checkin_journals'))


    def backwards(self, orm):
        # Deleting model 'Ticket'
        db.delete_table('articletrack_ticket')

        # Deleting model 'Comment'
        db.delete_table('articletrack_comment')

        # Deleting model 'Article'
        db.delete_table('articletrack_article')

        # Removing M2M table for field journals on 'Article'
        db.delete_table(db.shorten_name('articletrack_article_journals'))


        # User chose to not deal with backwards NULL issues for 'Checkin.issue_label'
        raise RuntimeError("Cannot reverse this migration. 'Checkin.issue_label' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Checkin.issue_label'
        db.add_column('articletrack_checkin', 'issue_label',
                      self.gf('django.db.models.fields.CharField')(max_length=64),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Checkin.journal_title'
        raise RuntimeError("Cannot reverse this migration. 'Checkin.journal_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Checkin.journal_title'
        db.add_column('articletrack_checkin', 'journal_title',
                      self.gf('django.db.models.fields.CharField')(max_length=256),
                      keep_default=False)

        # Adding field 'Checkin.pissn'
        db.add_column('articletrack_checkin', 'pissn',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=9),
                      keep_default=False)

        # Adding field 'Checkin.eissn'
        db.add_column('articletrack_checkin', 'eissn',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=9),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Checkin.article_title'
        raise RuntimeError("Cannot reverse this migration. 'Checkin.article_title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Checkin.article_title'
        db.add_column('articletrack_checkin', 'article_title',
                      self.gf('django.db.models.fields.CharField')(max_length=512),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Checkin.articlepkg_ref'
        raise RuntimeError("Cannot reverse this migration. 'Checkin.articlepkg_ref' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Checkin.articlepkg_ref'
        db.add_column('articletrack_checkin', 'articlepkg_ref',
                      self.gf('django.db.models.fields.CharField')(max_length=32),
                      keep_default=False)

        # Deleting field 'Checkin.article'
        db.delete_column('articletrack_checkin', 'article_id')

        # Adding M2M table for field journals on 'Checkin'
        m2m_table_name = db.shorten_name('articletrack_checkin_journals')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('checkin', models.ForeignKey(orm['articletrack.checkin'], null=False)),
            ('journal', models.ForeignKey(orm['journalmanager.journal'], null=False))
        ))
        db.create_unique(m2m_table_name, ['checkin_id', 'journal_id'])


    models = {
        'articletrack.article': {
            'Meta': {'object_name': 'Article'},
            'article_title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'articlepkg_ref': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'eissn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '9'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'issue_label': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'journal_title': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'journals': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'articles'", 'null': 'True', 'to': "orm['journalmanager.Journal']"}),
            'pissn': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '9'})
        },
        'articletrack.checkin': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Checkin'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'checkins'", 'null': 'True', 'to': "orm['articletrack.Article']"}),
            'attempt_ref': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'package_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'uploaded_at': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'articletrack.comment': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Comment'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments_author'", 'to': "orm['auth.User']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'ticket': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['articletrack.Ticket']"})
        },
        'articletrack.notice': {
            'Meta': {'ordering': "['-created_at']", 'object_name': 'Notice'},
            'checkin': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['articletrack.Checkin']"}),
            'checkpoint': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'stage': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'articletrack.ticket': {
            'Meta': {'object_name': 'Ticket'},
            'article': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'articles'", 'to': "orm['articletrack.Article']"}),
            'author': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tickets'", 'to': "orm['auth.User']"}),
            'finished_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'started_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256'})
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
            'name_slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.institution': {
            'Meta': {'ordering': "['name']", 'object_name': 'Institution'},
            'acronym': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '16', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'address_complement': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cel': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'complement': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'fax': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'})
        },
        'journalmanager.journal': {
            'Meta': {'ordering': "['title']", 'object_name': 'Journal'},
            'abstract_keyword_languages': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'abstract_keyword_languages'", 'symmetrical': 'False', 'to': "orm['journalmanager.Language']"}),
            'acronym': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'collection': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'journals'", 'to': "orm['journalmanager.Collection']"}),
            'copyrighter': ('django.db.models.fields.CharField', [], {'max_length': '254'}),
            'cover': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'enjoy_creator'", 'to': "orm['auth.User']"}),
            'ctrl_vocabulary': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'current_ahead_documents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'editor_address': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'editor_address_city': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'editor_address_country': ('scielo_extensions.modelfields.CountryField', [], {'max_length': '2'}),
            'editor_address_state': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'editor_address_zip': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'editor_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'editor_name': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'editor_phone1': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'editor_phone2': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True', 'blank': 'True'}),
            'editorial_standard': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'editors': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'user_editors'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'eletronic_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_index': 'True'}),
            'final_num': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'final_vol': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'final_year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'frequency': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_coverage': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'init_num': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'init_vol': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'init_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'is_indexed_aehci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_indexed_scie': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_indexed_ssci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_trashed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Language']", 'symmetrical': 'False'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medline_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'medline_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'blank': 'True'}),
            'national_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'max_length': '254', 'null': 'True', 'blank': 'True'}),
            'other_previous_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'previous_ahead_documents': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'previous_title': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'prev_title'", 'null': 'True', 'to': "orm['journalmanager.Journal']"}),
            'print_issn': ('django.db.models.fields.CharField', [], {'max_length': '9', 'db_index': 'True'}),
            'pub_level': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'pub_status': ('django.db.models.fields.CharField', [], {'default': "'inprogress'", 'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'pub_status_changed_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pub_status_changed_by'", 'to': "orm['auth.User']"}),
            'pub_status_reason': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'publication_city': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'publisher_country': ('scielo_extensions.modelfields.CountryField', [], {'max_length': '2'}),
            'publisher_name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'publisher_state': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'scielo_issn': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'secs_code': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'null': 'True', 'db_index': 'True'}),
            'sponsor': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'journal_sponsor'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['journalmanager.Sponsor']"}),
            'study_areas': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'journals_migration_tmp'", 'null': 'True', 'to': "orm['journalmanager.StudyArea']"}),
            'subject_categories': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "'journals'", 'null': 'True', 'to': "orm['journalmanager.SubjectCategory']"}),
            'subject_descriptors': ('django.db.models.fields.CharField', [], {'max_length': '1024'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'title_iso': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'}),
            'twitter_user': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url_journal': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'url_online_submission': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'use_license': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['journalmanager.UseLicense']"})
        },
        'journalmanager.language': {
            'Meta': {'ordering': "['name']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'iso_code': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'journalmanager.sponsor': {
            'Meta': {'ordering': "['name']", 'object_name': 'Sponsor', '_ormbases': ['journalmanager.Institution']},
            'collections': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['journalmanager.Collection']", 'symmetrical': 'False'}),
            'institution_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['journalmanager.Institution']", 'unique': 'True', 'primary_key': 'True'})
        },
        'journalmanager.studyarea': {
            'Meta': {'object_name': 'StudyArea'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'study_area': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        'journalmanager.subjectcategory': {
            'Meta': {'object_name': 'SubjectCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '256', 'db_index': 'True'})
        },
        'journalmanager.uselicense': {
            'Meta': {'ordering': "['license_code']", 'object_name': 'UseLicense'},
            'disclaimer': ('django.db.models.fields.TextField', [], {'max_length': '512', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'license_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
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