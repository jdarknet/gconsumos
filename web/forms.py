# -*- coding: utf-8 -*-
import datetime
from os.path import splitext

from maestros.models import Terceros, TiposTerceros
from web.librerias import SelectTimeWidget

__author__ = 'julian'
from django import forms
from django.forms import models, TextInput, CheckboxInput
from django.forms.models import  inlineformset_factory, ModelChoiceField
from web.models import Configuracion, Contrato, Generales, Alarmas, Mensajes, PtdMedida



#class ConfiguraTiempo(forms.Forms):
#    fecha          = forms.DateField(required=False,label="Fecha",help_text="Formato d-m-yyyy")
#    tiempo         = forms.TimeField(widget=SelectTimeWidget(attrs={ 'class':'span3'} ),  label="Tiempo")

class ConfiguracionForms(models.ModelForm):
    class Meta:
        model   = Configuracion


    def __init__(self, *args, **kwargs):
        valor=kwargs.pop('pessid')
        super(models.ModelForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.format = '%d-%m-%Y'
        self.fields['fecha'].input_formats = ['%d-%m-%Y']
        self.fields['w_dhcp'].widget.attrs['class'] = "checky"
        if len(valor)!=0:
            self.fields['essid'].choices= ([(valor,valor),])

    id             = forms.IntegerField(required=False)
    fecha          = forms.DateField(required=False,label="Fecha",help_text="Formato d-m-yyyy")
    serialmodulo   = forms.CharField(required=False,max_length=20,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'No.Series'}))
    ipvolcado      = forms.IPAddressField(required=False, label="IP destino",widget=TextInput(attrs={'type':'text','placeholder':'IP volcado'}))
    uservolcado    = forms.CharField(required=False,label="Usuario",max_length=20,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Usuario'}))
    passvolcado    = forms.CharField(required=False,max_length=8, widget=TextInput(attrs={'type':'password','class':'error','placeholder':'Password'}))
    emailvolcado   = forms.EmailField(required=False,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Email'}))
    w_ip           = forms.IPAddressField(required=False,label="IP",widget=TextInput(attrs={'type':'text','placeholder':'IP'}))
    w_mask         = forms.IPAddressField(required=False,label="Mascara",widget=TextInput(attrs={'type':'text','placeholder':'MASK'}))
    w_gw           = forms.IPAddressField(required=False,label="Puerta de enlace",widget=TextInput(attrs={'type':'text','placeholder':'Puerta de Enlace'}))
    password       = forms.CharField(required=False,max_length=20, widget=TextInput(attrs={'type':'password','class':'error','placeholder':'Password'}))
    essid          = forms.ChoiceField(required=False, choices=(("",""),))
    w_dhcp         = forms.BooleanField(required=False)

class ContratosForms(models.ModelForm):
    class Meta:
        model = Contrato

    id               =  forms.IntegerField(required=False,  widget=TextInput(attrs= {'class':'hidden'}))
    empresaelectrica =  forms.ModelChoiceField(queryset= Terceros.objects.filter(tipotercero=TiposTerceros.objects.filter(accion=1)[0].id),required=True, help_text=None, label= 'Compañia de Suministro' )
    actividadeco     =  forms.CharField(required=False,max_length=20,label="Actividad Economica",  widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Actividad Economica'}))
    cups             =  forms.CharField(required=False,max_length=25,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'CUPS'}))
    potencia         =  forms.CharField(required=True,max_length=20,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Potencia Contratada'}))



class GeneralesForms(models.ModelForm):

    class Meta:
        model = Generales

    def __init__(self,*args,**kwargs):
        super(GeneralesForms,self).__init__(*args,**kwargs)
        for campos in ['diasfestivos','calefaccion','aireacondicionado','calentadoragua','vitroceramica','congelador']:
            self.fields[campos].widget.attrs['class']='normal-check'

    id               =  forms.IntegerField(required=False,  widget=TextInput(attrs= {'class':'hidden'}))
    nombpropietario  =  forms.ModelChoiceField(queryset= Terceros.objects.filter(tipotercero=TiposTerceros.objects.filter(accion=4)[0].id),required=True, help_text=None, label= 'Nombre Propietario' )
    mediaconsumo     =  forms.DecimalField(initial=0,max_digits=10, decimal_places=2, widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Media Consumo'}),label="Media de Consumo",help_text="Media en Watts")
    diasfestivos     =  forms.CheckboxInput()


class PtsMedidasForms(models.ModelForm):
    class Meta:
        model= PtdMedida
    id           = forms.IntegerField(required=False,  widget=TextInput(attrs= {'class':'hidden'}))
    descripcion  = forms.CharField(max_length=100,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Denominación'}))
    ubicacion  = forms.CharField(max_length=100,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Ubicacion'}))



class AlarmasForms(models.ModelForm):
    class Meta:
        model= Alarmas
    id           = forms.IntegerField(required=False,  widget=TextInput(attrs= {'class':'hidden'}))
    descripcion  = forms.CharField(max_length=100,widget=TextInput(attrs={'type':'text','class':'error','placeholder':'Denominación'}))
    consigna     = forms.IntegerField(required=False,label="Consigna",help_text="En Watts",initial=0)
    tiempoinicio = forms.TimeField(widget=SelectTimeWidget(attrs={ 'class':'span3'} ),  label="Inicio vigencia")
    tiempofin    = forms.TimeField(widget=SelectTimeWidget(attrs={ 'class':'span3'} ), label= "Fin vigencia"  )
    idcomsumos    =forms.ModelChoiceField(queryset=PtdMedida.objects.all(), label="Sensor",required=True)
#    tipo        = forms.(label="Tipo de Consigna",help_text="Selecciones el tipo de alarma a generar")


MensajesFormsSet    = inlineformset_factory(Alarmas,Mensajes,extra=1,can_delete=True)



class HistoricoForms(forms.Form):

    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.format = '%d-%m-%Y'
        self.fields['fecha'].input_formats = ['%d-%m-%Y']

    sensores = forms.ModelChoiceField( required=True,queryset=PtdMedida.objects.all(), label="Selecciona Sensores")
    fecha    = forms.DateField(required=True,label="Fecha")


class ConfiguraTiempo(forms.Form):
    def __init__(self, *args, **kwargs):
        super(forms.Form, self).__init__(*args, **kwargs)
        self.fields['fecha'].widget.format = '%d-%m-%Y'
        self.fields['fecha'].input_formats = ['%d-%m-%Y']
        self.fields['fecha'].initial = datetime.datetime.today()
        self.fields['tiempo'].widget.format = '%H:%M:%S'
        self.fields['tiempo'].input_formats = ['%H:%M%S']
        self.fields['tiempo'].initial = datetime.datetime.now()

    fecha          = forms.DateField(required=False,label="Fecha",help_text="Formato d-m-yyyy")
    tiempo         = forms.TimeField(widget=SelectTimeWidget(attrs={ 'class':'span3'} ),  label="Tiempo")

class ArchivoValidationError(forms.ValidationError):
    def __init__(self):
        super(ArchivoValidationError, self).__init__((u'Solo archivos de actualización ') )


class ArchivoField(forms.FileField):
    valid_content_types = ('application/x-compressed-tar',)
    valid_file_extensions = ('tgz')
    def __init__(self, *args, **kwargs):
        super(ArchivoField, self).__init__(*args, **kwargs)
        self.label = unicode('Archivo')
        self.helptext = unicode('Selecccione el archivo de actualización')

    def clean(self,data,initial=None):
        f = super(ArchivoField, self).clean(data, initial)
        ext = splitext(f.name)[1][1:].lower()
        if ext in ArchivoField.valid_file_extensions:
            return f
        raise ArchivoValidationError()


class ActualizaSistema(forms.Form):
    archivo  = ArchivoField()

