# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CourseEmail'
        db.create_table('bulk_email_courseemail', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sender', self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['auth.User'], null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(max_length=128, db_index=True)),
            ('subject', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('html_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('text_message', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(max_length=255, db_index=True)),
            ('to_option', self.gf('django.db.models.fields.CharField')(default='myself', max_length=64)),
            ('template_name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
            ('from_addr', self.gf('django.db.models.fields.CharField')(max_length=255, null=True)),
        ))
        db.send_create_signal('bulk_email', ['CourseEmail'])

        # Adding model 'Optout'
        db.create_table('bulk_email_optout', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(max_length=255, db_index=True)),
        ))
        db.send_create_signal('bulk_email', ['Optout'])

        # Adding unique constraint on 'Optout', fields ['user', 'course_id']
        db.create_unique('bulk_email_optout', ['user_id', 'course_id'])

        # Adding model 'CourseEmailTemplate'
        db.create_table('bulk_email_courseemailtemplate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('html_template', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('plain_template', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('bulk_email', ['CourseEmailTemplate'])

        # Adding model 'CourseAuthorization'
        db.create_table('bulk_email_courseauthorization', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('course_id', self.gf('xmodule_django.models.CourseKeyField')(unique=True, max_length=255, db_index=True)),
            ('email_enabled', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('bulk_email', ['CourseAuthorization'])


    def backwards(self, orm):
        # Removing unique constraint on 'Optout', fields ['user', 'course_id']
        db.delete_unique('bulk_email_optout', ['user_id', 'course_id'])

        # Deleting model 'CourseEmail'
        db.delete_table('bulk_email_courseemail')

        # Deleting model 'Optout'
        db.delete_table('bulk_email_optout')

        # Deleting model 'CourseEmailTemplate'
        db.delete_table('bulk_email_courseemailtemplate')

        # Deleting model 'CourseAuthorization'
        db.delete_table('bulk_email_courseauthorization')


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
        'bulk_email.courseauthorization': {
            'Meta': {'object_name': 'CourseAuthorization'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'email_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'bulk_email.courseemail': {
            'Meta': {'object_name': 'CourseEmail'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_addr': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'html_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'sender': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '128', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            'template_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'text_message': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'to_option': ('django.db.models.fields.CharField', [], {'default': "'myself'", 'max_length': '64'})
        },
        'bulk_email.courseemailtemplate': {
            'Meta': {'object_name': 'CourseEmailTemplate'},
            'html_template': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'plain_template': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        'bulk_email.optout': {
            'Meta': {'unique_together': "(('user', 'course_id'),)", 'object_name': 'Optout'},
            'course_id': ('xmodule_django.models.CourseKeyField', [], {'max_length': '255', 'db_index': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['bulk_email']
