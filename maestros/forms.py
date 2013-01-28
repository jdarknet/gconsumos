# -*- coding: utf-8 -*-
from django.db import models
from django.forms import forms
from maestros.models import CabPeriodosHorarios, DetPeriodosHorarios

__author__ = 'julian'


class CabPeriodosForms(forms.ModelForm):
    class Meta:
        model=CabPeriodosHorarios
    id             = forms.IntegerField()
    fechaalta      = forms.DateField(label='F.Alta')
    fechabaja      = forms.DateField(label='F.Baja')

class  DetPeriodosForms(forms.ModelForm):
    class Meta:
        model =  DetPeriodosHorarios


def get_formfacturacion_formset(form, formset=models.BaseInlineFormSet, **kwargs):
    return models.inlineformset_factory(CabPeriodosHorarios, DetPeriodosHorarios, form, formset, can_delete=True)



