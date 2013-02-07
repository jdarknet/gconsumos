# -*- coding: utf-8 -*-
from web.models import PtdMedida

__author__ = 'julian'
from django.db import models



class ConsumosAnos(models.Model):
    ts         = models.TextField(unique=True, blank=True) # This field type is a guess.
    ejer       = models.IntegerField(null=True, blank=True)
    per        = models.IntegerField(null=True, blank=True)
    energia    = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class ConsumosDias(models.Model):
    ts      = models.TextField(blank=True) # This field type is a guess.
    ejer    = models.IntegerField(null=True, blank=True)
    per     = models.IntegerField(null=True, blank=True)
    dia     = models.IntegerField(null=True, blank=True)
    energia = models.FloatField(null=True, blank=True)
    semana  = models.IntegerField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")


class ConsumosHoras(models.Model):
    ts = models.TextField(unique=True, blank=True) # This field type is a guess.
    ejer = models.IntegerField(null=True, blank=True)
    per = models.IntegerField(null=True, blank=True)
    dia = models.IntegerField(null=True, blank=True)
    hora = models.IntegerField(null=True, blank=True)
    energia = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class ConsumosMes(models.Model):
    ts = models.TextField(unique=True, blank=True) # This field type is a guess.
    ejer = models.IntegerField(null=True, blank=True)
    per = models.IntegerField(null=True, blank=True)
    energia = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class ConsumosTmp(models.Model):
    ts = models.TextField(unique=True, blank=True) # This field type is a guess.
    ejer = models.IntegerField(null=True, blank=True)
    per = models.IntegerField(null=True, blank=True)
    dia = models.IntegerField(null=True, blank=True)
    hora = models.IntegerField(null=True, blank=True)
    min = models.IntegerField(null=True, blank=True)
    seg = models.IntegerField(null=True, blank=True)
    energia = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class EstaAcumMes(models.Model):
    per     = models.IntegerField(null=True, blank=True)
    hora    = models.IntegerField(null=True, blank=True)
    energia = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class EstaAcumDiaSema(models.Model):
    diasemana = models.IntegerField(null=True, blank=True)
    hora      = models.IntegerField(null=True, blank=True)
    energia   = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")

class EstaAcumHora(models.Model):
    hora       = models.IntegerField(null=True, blank=True)
    energia    = models.FloatField(null=True, blank=True)
    idcomsumos = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida")