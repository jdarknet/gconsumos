# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ConsumosAnos'
        db.create_table('lecturas_consumosanos', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.TextField')(unique=True, blank=True)),
            ('ejer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('per', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('energia', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('idcomsumos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.PtdMedida'])),
        ))
        db.send_create_signal('lecturas', ['ConsumosAnos'])

        # Adding model 'ConsumosDias'
        db.create_table('lecturas_consumosdias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('ejer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('per', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('energia', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('semana', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('idcomsumos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.PtdMedida'])),
        ))
        db.send_create_signal('lecturas', ['ConsumosDias'])

        # Adding model 'ConsumosHoras'
        db.create_table('lecturas_consumoshoras', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.TextField')(unique=True, blank=True)),
            ('ejer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('per', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hora', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('energia', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('idcomsumos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.PtdMedida'])),
        ))
        db.send_create_signal('lecturas', ['ConsumosHoras'])

        # Adding model 'ConsumosMes'
        db.create_table('lecturas_consumosmes', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.TextField')(unique=True, blank=True)),
            ('ejer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('per', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('energia', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('idcomsumos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.PtdMedida'])),
        ))
        db.send_create_signal('lecturas', ['ConsumosMes'])

        # Adding model 'ConsumosTmp'
        db.create_table('lecturas_consumostmp', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ts', self.gf('django.db.models.fields.TextField')(unique=True, blank=True)),
            ('ejer', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('per', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('dia', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('hora', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('min', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('seg', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('energia', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('idcomsumos', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['web.PtdMedida'])),
        ))
        db.send_create_signal('lecturas', ['ConsumosTmp'])


    def backwards(self, orm):
        # Deleting model 'ConsumosAnos'
        db.delete_table('lecturas_consumosanos')

        # Deleting model 'ConsumosDias'
        db.delete_table('lecturas_consumosdias')

        # Deleting model 'ConsumosHoras'
        db.delete_table('lecturas_consumoshoras')

        # Deleting model 'ConsumosMes'
        db.delete_table('lecturas_consumosmes')

        # Deleting model 'ConsumosTmp'
        db.delete_table('lecturas_consumostmp')


    models = {
        'lecturas.consumosanos': {
            'Meta': {'object_name': 'ConsumosAnos'},
            'ejer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcomsumos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.PtdMedida']"}),
            'per': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        },
        'lecturas.consumosdias': {
            'Meta': {'object_name': 'ConsumosDias'},
            'dia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ejer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcomsumos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.PtdMedida']"}),
            'per': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'semana': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'lecturas.consumoshoras': {
            'Meta': {'object_name': 'ConsumosHoras'},
            'dia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ejer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hora': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcomsumos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.PtdMedida']"}),
            'per': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        },
        'lecturas.consumosmes': {
            'Meta': {'object_name': 'ConsumosMes'},
            'ejer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcomsumos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.PtdMedida']"}),
            'per': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        },
        'lecturas.consumostmp': {
            'Meta': {'object_name': 'ConsumosTmp'},
            'dia': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ejer': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'energia': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'hora': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'idcomsumos': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.PtdMedida']"}),
            'min': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'per': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'seg': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ts': ('django.db.models.fields.TextField', [], {'unique': 'True', 'blank': 'True'})
        },
        'web.ptdmedida': {
            'Meta': {'object_name': 'PtdMedida'},
            'canal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['lecturas']