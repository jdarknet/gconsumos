from django.contrib.admin import ModelAdmin

__author__ = 'julian'
from maestros.models import *
from django.contrib import admin

#admin.site.register(TiposCurvas)
#admin.site.register(TiposInstalacion)
admin.site.register(TiposTerceros)
admin.site.register(Paises)
admin.site.register(Provincias)
admin.site.register(CodigosPostales)

admin.site.register(Terceros)


class DetPeriodoHorarioTabular(admin.TabularInline):

    fieldsets = [
        ('Detalle Horario', {'fields': ['denoperiodo','temporada','intinicial','intfinal']}),
        ]

    model=DetPeriodosHorarios

    def get_fieldsets(self, request, obj=None):
        if self.declared_fieldsets:
            return self.declared_fieldsets
        form = self.get_formset(request).form
        return [(None, {'fields': form.base_fields.keys()})]


class CabPeriodosHorariosAdmin(ModelAdmin):

    fieldsets = (
        ('Definicion de Periodos', {
            'fields': ('descripcion', ('fechaalta', 'fechabaja'),)
        }),
        )

    inlines=[DetPeriodoHorarioTabular]
    list_display= ('descripcion','fechaalta','fechabaja',)


admin.site.register(CabPeriodosHorarios,CabPeriodosHorariosAdmin)


class DetTarifasTabular(admin.TabularInline):

    model = DetallesTarifas

    fieldsets = [
        ('Detalle Tarifa', {'fields': ['detperiodo','precio']}),
        ]


class TarifasAccesoAdmin(ModelAdmin):
    fieldsets = (
        ('Definicion de Periodos', {
            'fields': ('descripcion', ('cabperiodo', 'fechapublica'),)
        }),
        )

    inlines=[DetTarifasTabular]
    list_display = ('descripcion','cabperiodo','fechapublica')

    class Media:
        #css = { "all": ("/static/css/comprasadmin.css",)}
        js  = ("/static/js/jquery-1.3.2.min.js","/static/js/tarifasacceso.js","/static/dajax/jquery.dajax.core.js","/static/dajaxice/dajaxice.core.js",)


admin.site.register(TarifasdeAcceso,TarifasAccesoAdmin)