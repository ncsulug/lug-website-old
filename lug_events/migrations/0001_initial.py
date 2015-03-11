# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'EventKind'
        db.create_table('lug_events_eventkind', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('singular', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('plural', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=128)),
        ))
        db.send_create_signal('lug_events', ['EventKind'])

        # Adding model 'Event'
        db.create_table('lug_events_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('kind', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lug_events.EventKind'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')()),
            ('speaker', self.gf('django.db.models.fields.CharField')(max_length=48, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('pitch', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('custom_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('advisory', self.gf('django.db.models.fields.CharField')(max_length=32, blank=True)),
            ('on_website', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('on_billboard', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('lug_events', ['Event'])


    def backwards(self, orm):
        # Deleting model 'EventKind'
        db.delete_table('lug_events_eventkind')

        # Deleting model 'Event'
        db.delete_table('lug_events_event')


    models = {
        'lug_events.event': {
            'Meta': {'ordering': "['-start_time']", 'object_name': 'Event'},
            'advisory': ('django.db.models.fields.CharField', [], {'max_length': '32', 'blank': 'True'}),
            'custom_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'end_time': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lug_events.EventKind']"}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'on_billboard': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'on_website': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'pitch': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'speaker': ('django.db.models.fields.CharField', [], {'max_length': '48', 'blank': 'True'}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {})
        },
        'lug_events.eventkind': {
            'Meta': {'ordering': "['plural']", 'object_name': 'EventKind'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plural': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'singular': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['lug_events']