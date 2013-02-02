# -*- coding: utf-8 -*-
import datetime
import os
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db import connection, IntegrityError
from django.core.servers.basehttp import FileWrapper
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext, Context
from gconsumos.settings import PROJECT_ROOT, LOGGING
from utils import ponCero, validaEnergia, avalidaEnergia, consultaTablas, tiempoenMil, sentenciaSensores
from web.forms import  ContratosForms, GeneralesForms, AlarmasForms, MensajesFormsSet, PtsMedidasForms, ConfiguracionForms, HistoricoForms
from web.models import Configuracion, Contrato, Generales, Alarmas, Mensajes, PtdMedida


data = {'form_detail-TOTAL_FORMS': u'1','form_detail-INITIAL_FORMS': u'0','form_detail-MAX_NUM_FORMS': u'',}


def test(request):
    return render_to_response("test.html",context_instance=RequestContext(request))



@login_required(login_url='/')
def inicio(request):

    #Modificaciones a nivels de tarifas horarias
    aenergia=[]
    acoste=[]
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    nsemana =hoy.strftime("%W")
    sentencia = sentenciaSensores()
    cur  = connection.cursor()
    cur_dia          = cur.execute('select  sum(energia) from lecturas_consumoshoras  where dia=%s and per=%s and ejer=%s %s' % (dia,mes,ano,sentencia) )
    ediaria   = validaEnergia(cur_dia)
    cur_semana       = cur.execute(" " "select sum(energia) from lecturas_consumosdias   where  semana =" " "+str(nsemana)+" " " and ejer=" " "+str(ano)+" %s" % sentencia )
    esemana   = validaEnergia(cur_semana)
    cur_mes_encurso  = cur.execute(' select sum(energia) from lecturas_consumosdias   where per=%s and ejer=%s %s' %(mes,ano,sentencia))
    emescurso = validaEnergia(cur_mes_encurso)
    cur_mes    = cur.execute('select     sum(energia) from lecturas_consumosmes    where per=%s and ejer=%s  %s' % (mes,ano,sentencia))
    emens     = validaEnergia(cur_mes)
    cur_ano_encurso  = cur.execute( 'select sum(energia) from lecturas_consumosmes  where ejer=%s %s' % (ano,sentencia))
    eanocurso = validaEnergia(cur_ano_encurso)
#    cur_ano   = cur.execute('select     sum(energia) from lecturas_consumos_anos   where ejer=%s  ' % ano )
#    eano      = validaEnergia(cur_ano)
    #Buscar conste segun contrato en base de datos
    coste =0.00015 #Buscar a nivel de configuracion

    cur_hora_max  = cur.execute('select  max(energia) ,hora from (select sum(energia) energia,hora from lecturas_consumoshoras  where dia=%s and per=%s and ejer=%s %s group by hora)' % (dia,mes,ano,sentencia) )
    ehoramax,horamax = avalidaEnergia(cur_hora_max)

    cur_semana_max  = cur.execute('select max(energia) , semana from (select semana, sum(energia) energia from lecturas_consumosdias  where  per =%s and ejer=%s %s group by semana) '  %( mes,ano,sentencia) )
    esemanamax,semanamax  = avalidaEnergia(cur_semana_max)

    cur_dia_max     = cur.execute(' select max(energia) ,dia from (select sum(energia) energia,dia from lecturas_consumosdias   where per=%s and ejer=%s  %s group by dia) ' %(mes,ano,sentencia))
    ediamax,diamax  = avalidaEnergia(cur_dia_max)

    cur_mes_max     = cur.execute('select    max(energia), per from (select sum(energia) energia,per from lecturas_consumosmes  where per=%s and ejer=%s %s group by per) ' % (mes,ano,sentencia))
    emensmax,mesmax = avalidaEnergia(cur_mes_max)

    aenergiamax=(dict(ehoramax=ehoramax,esemanamax=esemanamax,ediamax=ediamax,emesmax=emensmax))
    momentos   =(dict(horamax =horamax, semanamax=semanamax,diamax=diamax,mesmax=mesmax))

    aenergia=(dict(diaria=ediaria,semanal=esemana+ediaria,mensual=emens+emescurso+ediaria,anual=eanocurso+emescurso+ediaria))
    acoste=( dict(diaria=round(aenergia["diaria"]*coste,2),semanal=round(aenergia["semanal"]*coste,2), mensual=round(aenergia["mensual"]*coste,2),anual=round(aenergia["anual"]*coste,2) ))

    return render_to_response("web/secciones/panelcontrol/estadisticas.html",{'energia':aenergia, 'coste': acoste, 'maximos' : aenergiamax, 'momento' : momentos },context_instance=RequestContext(request))

@login_required(login_url='/')
def configuracion(request):

        if 'envia_configura' in request.POST:

            id= request.POST['configura-id']

            if id == "":
                #Solo queremos un registro para la configuracion
                form_configura = ConfiguracionForms(request.POST,prefix="configura",pessid=str(request.POST['configura-essid']))
            else:
                objeto =Configuracion.objects.get(pk=id)
                form_configura = ConfiguracionForms(request.POST,prefix="configura",instance=objeto,pessid=str(request.POST['configura-essid']))

            if form_configura.is_valid():
                configura = form_configura.save()
                id = configura.id
                configura = Configuracion.objects.get(pk =id)
                form_configura = ConfiguracionForms(instance=configura,prefix="configura",pessid=configura.essid)

            else:
                print form_configura.errors.as_text()

        else:
            configura = Configuracion.objects.all()
            if configura.exists() == False:
                form_configura = ConfiguracionForms(prefix="configura",pessid="")
            else:
                form_configura = ConfiguracionForms(instance=configura[0],prefix="configura",pessid=configura[0].essid)


        return render_to_response("web/secciones/general/configuracion.html", {'configura' : form_configura},context_instance=RequestContext(request) )

@login_required(login_url='/')
def generales(request):

    if 'envia_general' in request.POST:
        id= request.POST['general-id']
        if id == "":
            form_general = GeneralesForms(request.POST,prefix="general")
        else:
            general = Generales.objects.get(pk=id)
            form_general = GeneralesForms(request.POST,prefix="general",instance=objeto)
        if form_general.is_valid():
            ogeneral =form_general.save()
            form_general = GeneralesForms(instance=ogeneral, prefix="general")
        else:
            print form_general.errors.as_text()
    else:
        general = Generales.objects.all()
        if general.exists() == False:
            form_general = GeneralesForms(prefix="general")
        else:
            form_general = GeneralesForms(instance=general[0],prefix="general")

    if 'envia_contrato' in request.POST:
        id= request.POST['contrato-id']
        if id == "":
            form_contratos = ContratosForms(request.POST,prefix="contrato")
        else:
            contrato = Contrato.objects.get(pk=id)
            form_contratos = ContratosForms(request.POST,prefix="contrato",instance=contrato)

        if form_contratos.is_valid():
            ocontrato=form_contratos.save()
            form_contratos = ContratosForms(prefix="contrato",instance=ocontrato)
        else:
            print "Error en contratos..."
            print form_contratos.errors.as_text()
            #Retornar mensaje de error
    else:
        contratos = Contrato.objects.all()
        if contratos.exists() ==False:
            form_contratos = ContratosForms(prefix="contrato")
        else:
            form_contratos =ContratosForms(instance=contratos[0],prefix="contrato")

    return render_to_response("web/secciones/general/generales.html", {'general' : form_general,'contrato' : form_contratos },context_instance=RequestContext(request) )

@login_required(login_url='/')
def alarmas(request):
    alarmas = Alarmas.objects.all()
    if "envia_nuevo" in request.POST:
        return redirect('/panelcontrol/alarmas/add')
    else:
        if alarmas.exists() == False:
            form_cab            = AlarmasForms(prefix="cabalarma")
            form_detail         = MensajesFormsSet(prefix="mensajes")
        else:
            alarma = Alarmas.objects.get(pk=alarmas[0].id)
            form_cab            = AlarmasForms(instance=alarma,prefix="cabalarma")
            form_detail         = MensajesFormsSet(instance=alarma,prefix="mensajes")


    formset_alarma = Alarmas.objects.all()
    return render_to_response("web/secciones/panelcontrol/alarmas.html", {'listalarm' : formset_alarma,'form_cab' :form_cab , 'form_detail': form_detail},context_instance=RequestContext(request) )

@login_required(login_url='/')
def alarmasNuevo(request):
    form_detail =""
    if 'envia_actualiza' in request.POST:
        form_cab            = AlarmasForms(request.POST,prefix="cabalarma")
        if form_cab.is_valid():
            cabecera            = form_cab.save(commit=False)
            form_detail         = MensajesFormsSet(request.POST,instance=cabecera,prefix="mensajes")
            if form_detail.is_valid():
                cabecera.save()
                form_detail.save()
                id = cabecera.id
                return redirect(reverse('alarmasEdita',kwargs = {'pk':id}))
            else:
                print form_detail
                print form_detail.errors
                request.user.message_set.create(message = form_detail.errors)
        else:
            print form_cab.errors.as_text()

    else:
        form_cab            = AlarmasForms(prefix="cabalarma")
        form_detail         = MensajesFormsSet(prefix="mensajes")
    formset_alarma =  Alarmas.objects.all()
    return render_to_response("web/secciones/panelcontrol/alarmas.html", {'listalarm' : formset_alarma,'form_cab' :form_cab , 'form_detail': form_detail },context_instance=RequestContext(request) )


@login_required(login_url='/')
def alarmasDelete(request,pk):
    try:
        alarmas = Alarmas.objects.get(pk=int(pk))
        try:
            mensajes = Mensajes.objects.filter(alarma_id =int(pk)).delete()
            alarmas.delete()

        except IntegrityError:
            request.user.message_set.create(message = "No se elimina, Error de Integridad")
        except:
            request.user.message_set.create(message = "Error al eliminar la alarma")
            form_cab            = AlarmasForms(instance=alarmas,prefix="cabalarma")
            form_detail         = MensajesFormsSet(instance=alarmas,prefix="mensajes")
            formset_alarma      = Alarmas.objects.all()
            return redirect(reverse('alarmasEdita',kwargs = {'pk':id}))

    except Alarmas.DoesNotExist:
        raise Http404
    return redirect(reverse('alarmas'))

@login_required(login_url='/')
def alarmasEdita(request,pk):
    try:
        alarmas = Alarmas.objects.get( pk=pk)
    except Alarmas.DoesNotExist:
        raise Http404

    if 'envia_actualiza' in request.POST:
        form_cab            = AlarmasForms(request.POST,prefix="cabalarma",instance=alarmas)
        if form_cab.is_valid():
            cabecera            = form_cab.save(commit=False)
            form_detail         = MensajesFormsSet(request.POST,instance=cabecera,prefix="mensajes")
            if form_detail.is_valid():
                cabecera.save()
                form_detail.save()
                messages.error(request,"Se actualizo la alarma")
            else:
                messages.error(request, "%s " % form_detail.errors)
                print "%s " % form_detail.errors

        else:
            messages.error(request, "%s " % form_cab.errors.as_text)
            print "%s " % form_cab.errors.as_text

    elif 'envia_elimina' in request.POST:
        return redirect(reverse('alarmasDelete',kwargs = {'pk':pk}))
    elif 'envia_nuevo' in request.POST:
        return redirect(reverse('alarmasNuevo'))

    form_cab            = AlarmasForms(instance=alarmas,prefix="cabalarma")
    form_detail         = MensajesFormsSet(instance=alarmas,prefix="mensajes")
    formset_alarma      = Alarmas.objects.all()

    return render_to_response("web/secciones/panelcontrol/alarmas.html", {'listalarm' : formset_alarma,'form_cab' :form_cab , 'form_detail': form_detail},context_instance=RequestContext(request) )


@login_required(login_url='/')
def lecturas(request,tipo):
    template=""
    listadatos=[]
    listgrafico=[]
    tipo=str(tipo)
    hoy    = datetime.datetime.now()
    if tipo=="24":
        template = "web/secciones/lecturas/ultima24horas.html"
        datos=consultaTablas('24',hoy,sensores=None)
        if datos!=[]:
            listgrafico =[([  [  tiempoenMil(row[0],row[1],row[2],row[3],row[4])  , ponCero(row[5]) ]] ) for row in datos ]
            for dat in datos:
                #listadatos.append([str(dat[3])+":"+str(dat[4]),ponCero(dat[5])])
                listadatos.append( [str(dat[6]).split(' ')[1],ponCero(dat[5])])
    if tipo=="7":
        template = "web/secciones/lecturas/ultimos7dias.html"
        datos=consultaTablas('semana', hoy,sensores=None)
        if datos!=[]:
            listgrafico =[([[ tiempoenMil(row[0],row[1],row[2],0,0), ponCero(row[3]) ]] ) for row in datos ]
            for dat in datos:
                listadatos.append(dict(dia=dat[0],energia=ponCero(dat[3])))
    if tipo=="30":
        template = "web/secciones/lecturas/ultimomes.html"
        datos=consultaTablas('mes',hoy,sensores=None)
        if datos!=[]:
            listgrafico =[([[ tiempoenMil(row[0],row[1],row[2],0,0), ponCero(row[3]) ]] ) for row in datos ]
            for dat in datos:
                listadatos.append([dat[0],ponCero(dat[3])] )


    return render_to_response(template, {'listadatos' : listadatos,'listgraf':listgrafico, },context_instance=RequestContext(request) )

@login_required(login_url='/')
def ptsmedidas(request):
    ptsmedidas = PtdMedida.objects.all()
    if "envia_nuevo" in request.POST:
        return redirect('/general/ptsmedidas/add')
    else:
        if ptsmedidas.exists() == False:
            form_cab            = PtsMedidasForms(prefix="cabptmedidas")

        else:
            ptmedida = PtdMedida.objects.get(pk=ptsmedidas[0].id)
            form_cab            = PtsMedidasForms(instance=ptmedida,prefix="cabptmedidas")



    formset_ptsmedidas = ptsmedidas
    return render_to_response("web/secciones/general/ptsmedidas.html", { 'listaptsmedidas' : formset_ptsmedidas,'form_cab' :form_cab },context_instance=RequestContext(request) )



@login_required(login_url='/')
def ptsmedidasNuevo(request):

    if 'envia_actualiza' in request.POST:
        form_cab            = PtsMedidasForms(request.POST,prefix="cabptmedidas")
        if form_cab.is_valid():
            cabecera            = form_cab.save()
            id = cabecera.id
            return redirect(reverse('ptsmedidasEdita',kwargs = {'pk':id}))
        else:
            request.user.message_set.create(message = form_cab.errors.as_text())

    else:
        form_cab = PtsMedidasForms(prefix="cabptmedidas")

    formset_ptsmedidas =  PtdMedida.objects.all()
    return render_to_response("web/secciones/general/ptsmedidas.html", {'listaptsmedidas' : formset_ptsmedidas,'form_cab' :form_cab },context_instance=RequestContext(request) )


@login_required(login_url='/')
def ptsmedidasDelete(request,pk):
    try:
        ptsmedidas = PtdMedida.objects.get(pk=int(pk))
        try:

            ptsmedidas.delete()

        except IntegrityError:
            request.user.message_set.create(message = "No se elimina, Error de Integridad")
        except:
            request.user.message_set.create(message = "Error al eliminar la alarma")
            form_cab                = PtsMedidasForms(instance=ptsmedidas,prefix="cabptmedidas")
            formset_ptsmedidas      = PtdMedida.objects.all()
            return redirect(reverse('ptsmedidasEdita',kwargs = {'pk':id}))

    except PtdMedida.DoesNotExist:
        raise Http404
    return redirect(reverse('ptsmedidas'))

@login_required(login_url='/')
def ptsmedidasEdita(request,pk):
    try:
        ptsmedidas = PtdMedida.objects.get(pk=int(pk))
    except PtdMedida.DoesNotExist:
        raise Http404

    if 'envia_actualiza' in request.POST:
        form_cab            = PtsMedidasForms(request.POST,prefix="cabptmedidas",instance=ptsmedidas)
        if form_cab.is_valid():
            cabecera            = form_cab.save()
        else:
            messages.error(request, "%s " % form_cab.errors.as_text)
            print "%s " % form_cab.errors.as_text

    elif 'envia_elimina' in request.POST:
        return redirect(reverse('ptsmedidasDelete',kwargs = {'pk':pk}))
    elif 'envia_nuevo' in request.POST:
        return redirect(reverse('ptsmedidasNuevo'))

    form_cab                = PtsMedidasForms(instance=ptsmedidas,prefix="cabptmedidas")
    formset_ptsmedidas      = PtdMedida.objects.all()

    return render_to_response("web/secciones/general/ptsmedidas.html", {'listaptsmedidas' : formset_ptsmedidas,'form_cab' :form_cab },context_instance=RequestContext(request) )


@login_required(login_url='/')
def verLogs(request):
    textologs =""
    response=""
    if 'leer_logs' in request.POST:
         filename =LOGGING['handlers']['log_file']['filename']
#        file = open(LOGGING['handlers']['log_file']['filename'])
#        lineas = File(file).readlines()
#        file.close()
#        for lin in lineas:
#            textologs=lin.replace("\n", "&#10")+textologs
         wrapper = FileWrapper(file(filename))
         response = HttpResponse(wrapper, content_type='text/plain')
         response['Content-Length'] = os.path.getsize(filename)
    return render_to_response("web/secciones/panelcontrol/logs.html", {'textologs' : response },context_instance=RequestContext(request) )


@login_required(login_url='/')
def verHistoricos(request,tipo):
    listadatos=[]
    listgrafico=[]
    datos=[]
    template="web/secciones/historico/resumenhistorico.html"
    if 'consulta' in request.POST:
        formconsulta = HistoricoForms(request.POST)
        if formconsulta.is_valid():
            vsensor = formconsulta.cleaned_data['sensores']
            vfecha  = formconsulta.cleaned_data['fecha']
            vfecha  =  datetime.datetime(*(vfecha.timetuple()[:6]))
            if tipo==u'1': #Diario
                etiquetas = { 'titulotab': 'Datos Diarios', 'titcol1': 'Horas', 'titulograf' : 'Grafico Diario'}
                datos= consultaTablas('24',vfecha,int(vsensor.id))
                if datos!=[]:
                    listgrafico =[([  [  tiempoenMil(row[0],row[1],row[2],row[3],row[4])  , ponCero(row[5]) ]] ) for row in datos ]
                    for dat in datos:
                        listadatos.append( [str(dat[6]).split(' ')[1],ponCero(dat[5])])
            elif tipo==u'2': #Semana
                etiquetas = { 'titulotab': 'Datos Semanales', 'titcol1': 'Dia Semana', 'titulograf' : 'Grafico Semanal'}
                datos= consultaTablas('semana',vfecha,int(vsensor.id))
                if datos!=[]:
                    listgrafico =[([  [  tiempoenMil(row[0],row[1],row[2],0,0)  , ponCero(row[3]) ]] ) for row in datos ]
                    print listgrafico
                    for dat in datos:
                        listadatos.append([dat[0],ponCero(dat[3])])
            elif tipo==u'3': #Mes
                etiquetas = { 'titulotab': 'Datos Mensuales', 'titcol1': 'Dias', 'titulograf' : 'Grafico Mensuales'}
                datos= consultaTablas('mes',vfecha,int(vsensor.id))
                print datos
                if datos!=[]:
                    listgrafico =[([  [  tiempoenMil(row[0],row[1],row[2],0,0)  , ponCero(row[3]) ]] ) for row in datos ]
                    for dat in datos:
                        listadatos.append([str(dat[0]),ponCero(dat[3])] )
            elif tipo==u'4': #Ano
                etiquetas = { 'titulotab': 'Datos Anuales', 'titcol1': 'Mes', 'titulograf' : 'Grafico Anual'}
                datos= consultaTablas('ano',vfecha,int(vsensor.id))
                if datos!=[]:
                    listgrafico =[([  [  tiempoenMil(1,row[0],row[1],0,0)  , ponCero(row[2]) ]] ) for row in datos ]
                    for dat in datos:
                        listadatos.append( [str(dat[0]),ponCero(dat[2])])
        else:
            print  messages.error(request, "%s " % formconsulta.errors.as_text)
            print "Error"
    else:
        if tipo==u'1':
            etiquetas = { 'titulotab': 'Datos Diarios', 'titcol1': 'Horas', 'titulograf' : 'Grafico Diario'}
        elif tipo==u'2':
            etiquetas = { 'titulotab': 'Datos Semanales', 'titcol1': 'Dia Semana', 'titulograf' : 'Grafico Semanal'}
        elif tipo==u'3':
            etiquetas = { 'titulotab': 'Datos Mensuales', 'titcol1': 'Dias', 'titulograf' : 'Grafico Mensuales'}
        elif tipo==u'4':
            etiquetas = { 'titulotab': 'Datos Anuales', 'titcol1': 'Mes', 'titulograf' : 'Grafico Anual'}
        formconsulta = HistoricoForms()



    return render_to_response(template, {'formconsulta' :formconsulta,'listadatos' : listadatos,'listgraf':listgrafico, 'etiquetas' : etiquetas } ,context_instance=RequestContext(request) )
