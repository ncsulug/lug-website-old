# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Fortune'
        db.create_table('lug_fortune_fortune', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=240)),
            ('priority', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('lug_fortune', ['Fortune'])


    def backwards(self, orm):
        # Deleting model 'Fortune'
        db.delete_table('lug_fortune_fortune')


    models = {
        'lug_fortune.fortune': {
            'Meta': {'object_name': 'Fortune'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'priority': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '240'})
        }
    }

    complete_apps = ['lug_fortune']