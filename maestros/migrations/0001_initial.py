# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TiposCurvas'
        db.create_table('maestros_tiposcurvas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('minutos', self.gf('django.db.models.fields.BigIntegerField')(default=0)),
            ('fechaalta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('maestros', ['TiposCurvas'])

        # Adding model 'TiposInstalacion'
        db.create_table('maestros_tiposinstalacion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fechaalta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('maestros', ['TiposInstalacion'])

        # Adding model 'TiposTerceros'
        db.create_table('maestros_tiposterceros', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('accion', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('fechaalta', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('maestros', ['TiposTerceros'])

        # Adding model 'Paises'
        db.create_table('maestros_paises', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codpais', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('maestros', ['Paises'])

        # Adding model 'Provincias'
        db.create_table('maestros_provincias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codprovincia', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('nombre', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('tipo', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.Paises'])),
        ))
        db.send_create_signal('maestros', ['Provincias'])

        # Adding model 'CodigosPostales'
        db.create_table('maestros_codigospostales', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('codpostal', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.Provincias'])),
            ('calle', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('maestros', ['CodigosPostales'])

        # Adding model 'TarifasdeAcceso'
        db.create_table('maestros_tarifasdeacceso', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fechapublica', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('maestros', ['TarifasdeAcceso'])

        # Adding model 'DetallesTarifas'
        db.create_table('maestros_detallestarifas', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tfacceso', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.TarifasdeAcceso'])),
            ('punta', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('llano', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
            ('valle', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2, blank=True)),
        ))
        db.send_create_signal('maestros', ['DetallesTarifas'])

        # Adding model 'CabPeriodosHorarios'
        db.create_table('maestros_cabperiodoshorarios', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('descripcion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fechaalta', self.gf('django.db.models.fields.DateField')()),
            ('fechabaja', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal('maestros', ['CabPeriodosHorarios'])

        # Adding model 'DetPeriodosHorarios'
        db.create_table('maestros_detperiodoshorarios', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('cabperhorario', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.CabPeriodosHorarios'])),
            ('temporada', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('codigoper', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('denoperiodo', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('intinicial', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('intfinal', self.gf('django.db.models.fields.CharField')(max_length=2)),
        ))
        db.send_create_signal('maestros', ['DetPeriodosHorarios'])

        # Adding model 'Terceros'
        db.create_table('maestros_terceros', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tipotercero', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.TiposTerceros'])),
            ('denominacion', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('cif', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('direccion1', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('direccion2', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('telefono', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=50, null=True, blank=True)),
            ('paginaweb', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('pais', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.Paises'])),
            ('provincia', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.Provincias'])),
            ('codpostal', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maestros.CodigosPostales'])),
        ))
        db.send_create_signal('maestros', ['Terceros'])


    def backwards(self, orm):
        # Deleting model 'TiposCurvas'
        db.delete_table('maestros_tiposcurvas')

        # Deleting model 'TiposInstalacion'
        db.delete_table('maestros_tiposinstalacion')

        # Deleting model 'TiposTerceros'
        db.delete_table('maestros_tiposterceros')

        # Deleting model 'Paises'
        db.delete_table('maestros_paises')

        # Deleting model 'Provincias'
        db.delete_table('maestros_provincias')

        # Deleting model 'CodigosPostales'
        db.delete_table('maestros_codigospostales')

        # Deleting model 'TarifasdeAcceso'
        db.delete_table('maestros_tarifasdeacceso')

        # Deleting model 'DetallesTarifas'
        db.delete_table('maestros_detallestarifas')

        # Deleting model 'CabPeriodosHorarios'
        db.delete_table('maestros_cabperiodoshorarios')

        # Deleting model 'DetPeriodosHorarios'
        db.delete_table('maestros_detperiodoshorarios')

        # Deleting model 'Terceros'
        db.delete_table('maestros_terceros')


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
            'llano': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'punta': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'tfacceso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.TarifasdeAcceso']"}),
            'valle': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'})
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