# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'DetallesTarifas.llano'
        db.alter_column('maestros_detallestarifas', 'llano', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6))

        # Changing field 'DetallesTarifas.punta'
        db.alter_column('maestros_detallestarifas', 'punta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6))

        # Changing field 'DetallesTarifas.valle'
        db.alter_column('maestros_detallestarifas', 'valle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=8, decimal_places=6))

    def backwards(self, orm):

        # Changing field 'DetallesTarifas.llano'
        db.alter_column('maestros_detallestarifas', 'llano', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2))

        # Changing field 'DetallesTarifas.punta'
        db.alter_column('maestros_detallestarifas', 'punta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2))

        # Changing field 'DetallesTarifas.valle'
        db.alter_column('maestros_detallestarifas', 'valle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2))

    models = {
        'maestros.cabperiodoshorarios': {
            'Meta': {'object_name': 'CabPeriodosHorarios'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechaalta': ('django.db.models.fields.DateField', [], {}),
            'fechabaja': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'maestros.codigospostales': {
            'Meta': {'object_name': 'CodigosPostales'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'codpostal': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Provincias']"})
        },
        'maestros.detallestarifas': {
            'Meta': {'object_name': 'DetallesTarifas'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'llano': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'punta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'}),
            'tfacceso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.TarifasdeAcceso']"}),
            'valle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '6', 'blank': 'True'})
        },
        'maestros.detperiodoshorarios': {
            'Meta': {'ordering': "['temporada', 'denoperiodo']", 'object_name': 'DetPeriodosHorarios'},
            'cabperhorario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.CabPeriodosHorarios']"}),
            'codigoper': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'denoperiodo': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intfinal': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'intinicial': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'temporada': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'maestros.paises': {
            'Meta': {'object_name': 'Paises'},
            'codpais': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maestros.provincias': {
            'Meta': {'object_name': 'Provincias'},
            'codprovincia': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nombre': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Paises']"}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '2'})
        },
        'maestros.tarifasdeacceso': {
            'Meta': {'object_name': 'TarifasdeAcceso'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechapublica': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'maestros.terceros': {
            'Meta': {'ordering': "('denominacion',)", 'object_name': 'Terceros'},
            'cif': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'codpostal': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.CodigosPostales']"}),
            'denominacion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'direccion1': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'direccion2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'paginaweb': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'pais': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Paises']"}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Provincias']"}),
            'telefono': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'tipotercero': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.TiposTerceros']"})
        },
        'maestros.tiposcurvas': {
            'Meta': {'ordering': "('descripcion',)", 'object_name': 'TiposCurvas'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechaalta': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'minutos': ('django.db.models.fields.BigIntegerField', [], {'default': '0'})
        },
        'maestros.tiposinstalacion': {
            'Meta': {'ordering': "('descripcion',)", 'object_name': 'TiposInstalacion'},
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechaalta': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'maestros.tiposterceros': {
            'Meta': {'ordering': "('descripcion',)", 'object_name': 'TiposTerceros'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechaalta': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['maestros']