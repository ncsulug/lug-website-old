# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'MemberProfile.title'
        db.alter_column('lug_people_memberprofile', 'title', self.gf('django.db.models.fields.CharField')(default='', max_length=64))

        # Changing field 'MemberProfile.real_name'
        db.alter_column('lug_people_memberprofile', 'real_name', self.gf('django.db.models.fields.CharField')(default='', max_length=64))

        # Changing field 'BitType.link_template'
        db.alter_column('lug_people_bittype', 'link_template', self.gf('django.db.models.fields.CharField')(default='', max_length=240))

    def backwards(self, orm):

        # Changing field 'MemberProfile.title'
        db.alter_column('lug_people_memberprofile', 'title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Changing field 'MemberProfile.real_name'
        db.alter_column('lug_people_memberprofile', 'real_name', self.gf('django.db.models.fields.CharField')(max_length=64, null=True))

        # Changing field 'BitType.link_template'
        db.alter_column('lug_people_bittype', 'link_template', self.gf('django.db.models.fields.CharField')(max_length=240, null=True))

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
        'lug_people.bit': {
            'Meta': {'ordering': "('bit_type__ordering', 'bit_type__caption')", 'object_name': 'Bit'},
            'bit_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lug_people.BitType']"}),
            'data': ('django.db.models.fields.CharField', [], {'max_length': '240'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lug_people.MemberProfile']"})
        },
        'lug_people.bittype': {
            'Meta': {'ordering': "('ordering', 'caption')", 'object_name': 'BitType'},
            'caption': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'format': ('django.db.models.fields.CharField', [], {'default': "u'freetext'", 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructions': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'link_template': ('django.db.models.fields.CharField', [], {'max_length': '240', 'blank': 'True'}),
            'ordering': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '16'})
        },
        'lug_people.memberprofile': {
            'Meta': {'object_name': 'MemberProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'preferred_name': ('django.db.models.fields.CharField', [], {'default': "u'nick'", 'max_length': '4'}),
            'real_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'role': ('django.db.models.fields.CharField', [], {'default': "u'visitor'", 'max_length': '8'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['lug_people']