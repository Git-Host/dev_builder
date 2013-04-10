# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration


class Migration(SchemaMigration):

    def forwards(self, orm):
        try:
            print "trying to forward migrate - this fails sometimes due to columns already present"
            db.add_column('django_site', 'folder_name',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True))
            db.add_column('django_site', 'subdomains',
                          self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True))
        except Exception as ex:
            print "Yeah. We failed again %s" % ex
            print "but we'll move on ...."

    def backwards(self, orm):
        db.delete_column('django_site', 'folder_name')
        db.delete_column('django_site', 'subdomains')

    models = {

    }

    complete_apps = ['dynamicsites']
