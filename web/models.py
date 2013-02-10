# -*- coding: utf-8 -*-
import datetime
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.
from maestros.models import Terceros, TarifasdeAcceso

class Configuracion(models.Model):
    serialmodulo   = models.CharField(max_length=20 , verbose_name="Serial",null=True,blank=True)
    w_dhcp         = models.BooleanField(verbose_name="DHCP",help_text="Ip dinamica")
    w_ip           = models.IPAddressField(verbose_name="IP WIFI",null=True,blank=True)
    w_mask         = models.IPAddressField(verbose_name="MASCARA WIFI",null=True,blank=True)
    w_gw           = models.IPAddressField(verbose_name="Puerta de enlace WIFI",null=True,blank=True)
    essid          = models.CharField(max_length=50,verbose_name="ESSID", null=True, blank=True)
    ipvolcado      = models.IPAddressField(verbose_name="Ip",null=True,blank=True)
    uservolcado    = models.CharField(max_length=20,verbose_name="Usuario",   null=True,blank=True)
    passvolcado    = models.CharField(max_length=20,verbose_name="Passsowd",  null=True,blank=True)
    frecuencia     = models.CharField(max_length=2 ,verbose_name="Frecuencia",null=True,blank=True,choices=(('01','Hora'),('02','Diaria'),('03',"Semanal"),('04','Mensual')))
    protvolcado    = models.CharField(verbose_name="Protocolo",null=True, blank=True,max_length=10,choices=(('email','Email'),('ftp',"FTP"),('ssh','SSH')))
    emailvolcado   = models.EmailField(verbose_name="Email Volcado", null=True,blank=True)
    password       = models.CharField(max_length=8, verbose_name="Password",blank=True,null=True)
    fecha          = models.DateField(verbose_name="Fecha Alta",null=True,blank=True)


class PtdMedida(models.Model):
    descripcion  = models.CharField(max_length=50, verbose_name="Descripción")
    ubicacion    = models.CharField(max_length=50, verbose_name="Ubicacion")
    canal        = models.CharField(unique=True, max_length=2, verbose_name="Canales" , choices=( ('0','Canal 0'),('1','Canal 1'),('2','Canal 2'),('3','Canal 3'),('4','Canal 4'),('5','Canal 5'),('6','Canal 6'),('7','Canal 7'),('8','Canal 8'),('9','Canal 9')) )
    totaliza     = models.BooleanField(verbose_name='Totaliza', blank=True)

    def __unicode__(self):
        return "%s " % self.descripcion

    @models.permalink
    def get_absolute_url(self):
        return ('ptsmedidasEdita',(), {'pk' :str(self.id), })


class Contrato(models.Model):
    empresaelectrica = models.ForeignKey(Terceros,verbose_name="Electrica")
    actividadeco     = models.CharField(max_length=20,verbose_name="Actividad Economica")
    cups             = models.CharField(max_length=25,verbose_name="CUPS" )
    potencia         = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="Potencia")
    tfacceso         = models.ForeignKey(TarifasdeAcceso,verbose_name="Tarifas de Acceso") #Tarifas de acceso precios
    numcontador     =  models.CharField(max_length=25,verbose_name="Numero Contador")


class Generales(models.Model):
    nombpropietario     = models.ForeignKey(Terceros,verbose_name="Propietario")
    mediaconsumo        = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Media Consumo",help_text="Media en Watts")
    tipousuario         = models.CharField(max_length=1,choices=( ('1','Domestico'),('2','Comercial'),('3','Industrial') ),verbose_name="Usuario",help_text="Tipo de consumo" )
    diasfestivos        = models.BooleanField(verbose_name="Dias Festivos", help_text="La actividad no es la habitual en esos días" )
    calefaccion         = models.BooleanField(verbose_name="Calefacción",blank=True)
    aireacondicionado   = models.BooleanField(verbose_name="Aire Acondicionado",blank=True)
    calentadoragua      = models.BooleanField(verbose_name="Calentador de agua",blank=True)
    vitroceramica       = models.BooleanField(verbose_name="Vitroceramica/Inducción" ,blank=True)
    congelador          = models.BooleanField(verbose_name="Congelador" ,blank=True)


class Alarmas(models.Model):
    descripcion   = models.CharField(max_length=100,verbose_name="Nombre de Alarma")
    consigna      = models.IntegerField(verbose_name="Consigna en Watts",help_text="en Watts",default=0,null=True)
    tipo          = models.CharField(max_length=1,choices=( ('1','Historico'),('2','---------'),('3','Restrictiva Maxima'),('4','Restrictiva Minima') ),verbose_name="Tipo de Consigna" )
    sensibilidad  = models.CharField(max_length=1,choices=( ('1','Horaria'),('2','Dia Semana'),('3','Mensual') ),default="1",verbose_name="Sensibilidad" )
    tiempoinicio  = models.TimeField(verbose_name="Hora de inicio" , help_text="formato 0-24", default=datetime.date.today())
    tiempofin     = models.TimeField(verbose_name="Hora fin",help_text="formato 0-24",default=datetime.date.today())
    habilitar     = models.BooleanField(verbose_name="Habilitar",blank=True)
    idcomsumos    = models.ForeignKey(PtdMedida, verbose_name="Punto de Medida",null=True,blank=True)
#    class Meta:
#        unique_together=[('consigna','tipo'),]

    def __unicode__(self):
        return self.descripcion

    @models.permalink
    def get_absolute_url(self):
        return ('alarmasEdita',(), {'pk' :str(self.id), })


class Mensajes(models.Model):
    alarma         = models.ForeignKey(Alarmas,verbose_name='Alarmas')
    cuerpomensaje  = models.TextField(verbose_name="Mensaje")
    email_destino1 = models.EmailField(verbose_name="Email Destino")




#@dajaxice_register
#def updateCity(request, option):
#    dajax = Dajax()
#    options = City.objects.filter(country.id=option)
#    out = ""
#    for o in options[int(option)]:
#        out += "%s%s" % (out,o,)
#
#    dajax.assign('#id_city','innerHTML',out)
#    return dajax.json()
#country = forms.ModelChoiceField(widget = forms.Select(attrs = {'onchange' : "Dajaxice.acg.updateCity(Dajax.process,{'option':this.value});"}), queryset=Country.objects.all(), required=True,  empty_label = lcountry_empty, label=lcountry, help_text = lcountry_help, error_messages={'required': lcountry_required})
#city = forms.ModelChoiceField(queryset=City.objects.all(), required=False, empty_label = lcity_empty, label=lcity, help_text = lcity_help)