# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Configuracion.serialmodulo'
        db.alter_column('web_configuracion', 'serialmodulo', self.gf('django.db.models.fields.CharField')(max_length=20, null=True))

        # Changing field 'Configuracion.e_ip'
        db.alter_column('web_configuracion', 'e_ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))

        # Changing field 'Configuracion.e_gw'
        db.alter_column('web_configuracion', 'e_gw', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))

        # Changing field 'Configuracion.fecha'
        db.alter_column('web_configuracion', 'fecha', self.gf('django.db.models.fields.DateField')(null=True))

        # Changing field 'Configuracion.e_mask'
        db.alter_column('web_configuracion', 'e_mask', self.gf('django.db.models.fields.IPAddressField')(max_length=15, null=True))

    def backwards(self, orm):

        # Changing field 'Configuracion.serialmodulo'
        db.alter_column('web_configuracion', 'serialmodulo', self.gf('django.db.models.fields.CharField')(default=123456, max_length=20))

        # Changing field 'Configuracion.e_ip'
        db.alter_column('web_configuracion', 'e_ip', self.gf('django.db.models.fields.IPAddressField')(default='192.168.10.100', max_length=15))

        # User chose to not deal with backwards NULL issues for 'Configuracion.e_gw'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.e_gw' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.fecha'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.fecha' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Configuracion.e_mask'
        raise RuntimeError("Cannot reverse this migration. 'Configuracion.e_mask' and its values cannot be restored.")

    models = {
        'maestros.codigospostales': {
            'Meta': {'object_name': 'CodigosPostales'},
            'calle': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'codpostal': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provincia': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Provincias']"})
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
        'maestros.tiposterceros': {
            'Meta': {'ordering': "('descripcion',)", 'object_name': 'TiposTerceros'},
            'accion': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'fechaalta': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'web.alarmas': {
            'Meta': {'object_name': 'Alarmas'},
            'consigna': ('django.db.models.fields.IntegerField', [], {}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'habilitar': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'tiempofin': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 1, 17, 0, 0)'}),
            'tiempoinicio': ('django.db.models.fields.TimeField', [], {'default': 'datetime.datetime(2013, 1, 17, 0, 0)'}),
            'tipo': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        },
        'web.configuracion': {
            'Meta': {'object_name': 'Configuracion'},
            'e_gw': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'e_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'e_mask': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'emailvolcado': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'essid': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'fecha': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'frecuencia': ('django.db.models.fields.CharField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipvolcado': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'passvolcado': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True', 'blank': 'True'}),
            'protvolcado': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'serialmodulo': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'uservolcado': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'w_gw': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'w_ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'w_mask': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'})
        },
        'web.contrato': {
            'Meta': {'object_name': 'Contrato'},
            'actividadeco': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'cups': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'empresaelectrica': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Terceros']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'numcontador': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'potencia': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'tfacceso': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.TarifasdeAcceso']"})
        },
        'web.generales': {
            'Meta': {'object_name': 'Generales'},
            'aireacondicionado': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calefaccion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'calentadoragua': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'congelador': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'diasfestivos': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mediaconsumo': ('django.db.models.fields.DecimalField', [], {'max_digits': '10', 'decimal_places': '2'}),
            'nombpropietario': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maestros.Terceros']"}),
            'tipousuario': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'vitroceramica': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'web.mensajes': {
            'Meta': {'object_name': 'Mensajes'},
            'alarma': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['web.Alarmas']"}),
            'cuerpomensaje': ('django.db.models.fields.TextField', [], {}),
            'email_destino1': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'web.ptdmedida': {
            'Meta': {'object_name': 'PtdMedida'},
            'canal': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'descripcion': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ubicacion': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['web']