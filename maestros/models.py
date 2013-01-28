# -*- coding: utf-8 -*-
import datetime
import sys

__author__ = 'julian'
from django.db import models


class TiposCurvas(models.Model):
    descripcion = models.CharField(max_length=100, help_text ="Tipos de Curvas")
    minutos     = models.BigIntegerField(default=0, help_text="Minutos que componen el tipo de curva")
    fechaalta   = models.DateField()
    def save(self, *args, **kwargs):
        self.fechaalta=datetime.date.today()
        super(TiposCurvas, self).save(*args, **kwargs)
    def __unicode__(self):
        return unicode(self.descripcion)
    class Meta:
        ordering = ('descripcion',)
        verbose_name_plural = "Tipos de Curvas"


class TiposInstalacion(models.Model):
    descripcion = models.CharField(max_length=100, help_text ="Denominacion de la instalacion")
    fechaalta   = models.DateField()
    def save(self, *args, **kwargs):
        self.fechaalta=datetime.date.today()
        super(TiposInstalacion, self).save(*args, **kwargs)
    def __unicode__(self):
        return unicode(self.descripcion)
    class Meta:
        ordering = ('descripcion',)
        verbose_name_plural = "Tipos de Instatalacion"

class TiposTerceros(models.Model):
    descripcion = models.CharField(max_length=100, help_text="Denominacion del tercero, proeveedor, cliente, etc",verbose_name="Tipo Tercero")
    accion      = models.CharField(max_length=1, choices=( ('1','Proveedor'),('2','Cliente'),('3','Acreedor'),('4', 'Administradora'),('5','Admin. Publica' ), ('6','Planta de Generacion')  ), verbose_name="Indicador")
    fechaalta   = models.DateField(verbose_name="Fecha Alta:")
    def save(self, *args, **kwargs):
        self.fechaalta=datetime.date.today()
        super(TiposTerceros, self).save(*args, **kwargs)
    def __unicode__(self):
        return unicode(self.descripcion)
    class Meta:
        ordering = ('descripcion',)
        verbose_name_plural = "Tipos de Terceros"

class Paises(models.Model):
    codpais = models.CharField(max_length=3, help_text="Introduzca codigo del Pais")
    nombre  = models.CharField(max_length=100,help_text="Introduzca nombre del Pais",verbose_name="Nombre Pais")
    def __unicode__(self):
        return unicode(self.nombre)
    class Meta:
        verbose_name_plural = "Paises"

class Provincias(models.Model):
    codprovincia = models.CharField(max_length=3,verbose_name="Codigo Provincia")
    nombre       = models.CharField(max_length=100, verbose_name ="Provincia")
    tipo         = models.CharField(max_length = 2, choices =(('x','Capital'), ('0', 'Ciudad'),('1', 'Mas Ciudad')), verbose_name="Tipo")
    pais         = models.ForeignKey(Paises, verbose_name="Pais")
    def __unicode__(self):
        return unicode(self.codprovincia+' '+self.nombre)
    class Meta:
        verbose_name_plural = "Provincias"

class CodigosPostales(models.Model):
    codpostal = models.CharField(max_length=5, help_text= "Codigo postal de la ciudad", verbose_name="Codigo Postales")
    provincia =  models.ForeignKey(Provincias,verbose_name="Provincias")
    calle     = models.CharField(max_length=100,verbose_name="Calle")
    def __unicode__(self):
        return unicode(self.codpostal)
    class Meta:
        verbose_name_plural = "Codigos Postales"



class CabPeriodosHorarios(models.Model):
    descripcion = models.CharField(max_length=100,verbose_name="Descripcion",help_text="Describa la resolucion a la que se refiere el periodo")
    fechaalta   = models.DateField()
    fechabaja   = models.DateField(blank=True, null=True)

    def __unicode__(self):
        return u'%s ' %(self.descripcion)

    def save(self, *args, **kwargs):
        self.fechaalta=datetime.date.today()
        super(CabPeriodosHorarios, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Discriminacion Horaria"

class DetPeriodosHorarios(models.Model):
    cabperhorario = models.ForeignKey(CabPeriodosHorarios)
    temporada     = models.CharField( max_length=1, choices=(('V','Verano'),('I','Invierno')), verbose_name="Temporada")
    denoperiodo   = models.CharField(max_length=100,verbose_name="Denominacion",help_text="Descripcion del periodo horario")
    intinicial    = models.CharField(max_length=2,choices=tuple((str(n), str(n)) for n in range(0,25)),verbose_name="Hora Inicial", help_text="Coloque la hora inicial ,no incluida en el intervalo" )
    intfinal      = models.CharField(max_length=2,choices=tuple((str(n), str(n)) for n in range(0,25)),verbose_name="Hora Final", help_text="Coloque la hora final, incluida en el intervalo")
    class Meta:
        verbose_name_plural = "Periodos Horas"
        ordering=['temporada','denoperiodo']

    def __unicode__(self):
        return u'%s %s'%(self.denoperiodo,self.temporada)


class TarifasdeAcceso(models.Model):
    descripcion  = models.CharField(max_length=100, verbose_name='Tarifas de Accesso')
    cabperiodo   = models.ForeignKey(CabPeriodosHorarios, verbose_name= "Tipo Discrminación Horaria",blank=True,null=True)
    fechapublica = models.DateField(verbose_name="Fecha de Publicacion")
    def __unicode__(self):
        return u'%s' %(self.descripcion)

    class Meta:
        verbose_name_plural = "Tarifas de Acceso"

class DetallesTarifas(models.Model):
    tfacceso    =models.ForeignKey(TarifasdeAcceso,verbose_name="Tarifas de Acceso")
    precio      =models.DecimalField(blank=True, max_digits=8, decimal_places=6, null=True, help_text="Precio €/Kw hora")
    detperiodo  =models.ForeignKey(DetPeriodosHorarios, verbose_name="Periodo")

    def __unicode__(self):
        return 'Tarifa: %s    Periodo: %s  Precio: %s' % (self.tfacceso,self.detperiodo,self.precio)

    class Meta:
        verbose_name_plural = "Tarifas Contratos"



class Terceros(models.Model):
    tipotercero   = models.ForeignKey(TiposTerceros, verbose_name = "Tipo Tercero")
    denominacion  = models.CharField(max_length=100, help_text="Razon social del tercero", verbose_name="Razon Social")
    cif           = models.CharField(max_length=20, verbose_name="CIF/DNI")
    direccion1    = models.CharField(max_length=50,  help_text="Direccion", verbose_name="Direccion")
    direccion2    = models.CharField(max_length=50, verbose_name=" ",blank=True,null=True)
    telefono      = models.CharField(max_length= 20, verbose_name="Telefono", blank=True,null=True)
    email         = models.EmailField(max_length=50, verbose_name="Correo electronico",blank=True,null=True)
    paginaweb     = models.CharField(max_length=100, verbose_name="Pagina Web",blank=True,null=True)
    pais          = models.ForeignKey(Paises,verbose_name="Paises")
    provincia     = models.ForeignKey(Provincias,verbose_name="Provincia")
    codpostal     = models.ForeignKey(CodigosPostales,verbose_name="Codigo Postal")

    def save(self, *args, **kwargs):
        self.fechaalta=datetime.date.today()
        super(Terceros, self).save(*args, **kwargs)
    #        user, created = User.objects.get_or_create(username=self.user)
    #        group, created = Group.objects.get_or_create(name="generico")
    #        if created: group.save()
    #        user.groups.add(group)
    #        user.save()
    def delete(self, *args, **kwargs):
        """Never delete, just mark as deleted"""
        try:
            self.deleted = True
            self.save()
        except:
            print >> sys.stderr, "ERROR! No puede ser borrado"
    def __unicode__(self):
        return unicode(self.denominacion)

    class Meta:
        ordering = ('denominacion',)
        verbose_name = "Tercero"
        verbose_name_plural = "Terceros"
