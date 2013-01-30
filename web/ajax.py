# -*- coding: utf-8 -*-
import datetime
from time import sleep
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from django.db import connection
from django.utils import simplejson
from gconsumos import settings
from lecturas.GetDataFromCurrentCostMeter import leeDatos
import os
from maestros.models import DetPeriodosHorarios
from utils import ponCero, noSemana, tiempoenMil, sentenciaSensores, calculoTotalEnergia

__author__ = 'julian'


@dajaxice_register
def conectarwifi(request,ip,mask,gw,essid,dhcp,passwd):
    dajax = Dajax()
    con =0
    cfgfile=open("/etc/wpa_supplicant/wpa_supplicant.conf","w")
    cfgfile.write("ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev\n")
    cfgfile.write("update_config=1\n")
    cfgfile.write("network={\n")
    cfgfile.write('ssid="%s"\n' % essid.rstrip() )
    cfgfile.write('psk="%s"\n' % passwd)
    cfgfile.write("}")
    cfgfile.close()
    #lineas = os.popen(settings.PROJECT_ROOT+'/web/wificonnect.sh',"r")

    dajax.script("$('#essid').spin(false);")
    return dajax.json()



@dajaxice_register
def updatewifis(request):
    dajax = Dajax()
    con =0
    while con <= 20:
        lineas = os.popen(settings.PROJECT_ROOT+'/web/iwlist.sh',"r")
        if not lineas.readline():
            con= con+1
            sleep(3)
        else:
            break;
    essid=[]
    while 1:
        linea = lineas.readline()
        if not linea: break
        essid.append(linea.split("---"))
    out=[]
    for ess in essid:
        out.append("<option value='%s'>%s</option>" % (ess[0],ess[0]))

    dajax.assign('#id_configura-essid', 'innerHTML', ''.join(out))
    dajax.script("$('#essid').spin(false);")
    return dajax.json()

def testLectura():
    valor=0
    sql  = """select 1 valor from lecturas_consumostmp where datetime(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))||' '||substr('0'||hora,length(hora))||':'||substr('0'||min,length(min))) between datetime('now','-10 minutes') and datetime('now') """
    cur  = connection.cursor()
    cur.execute(sql)
    entries = cur.fetchall()
    if entries == []:
        valor=0;
    elif entries[0][0] !=1:
        valor=0
    else:
        valor=1

    return valor

@dajaxice_register
def llenaPeriodos(request,numero,id,valor):
    dajax = Dajax()
    valores = DetPeriodosHorarios.objects.filter(cabperhorario_id=int(id))
    out=[]
    out.append("<option value selected='selected'>---------</option>")
    for val in valores:
        if val.id== int(valor):
            out.append("<option value='%s' selected='selected'> Periodo: %s - %s %s %s </option>" % (val.id,val.denoperiodo,val.temporada,val.intinicial,val.intfinal) )
        else:
            out.append("<option value='%s'> Periodo: %s - %s %s %s </option>" % (val.id,val.denoperiodo,val.temporada,val.intinicial,val.intfinal) )

    dajax.assign('.field-detperiodo > #id_detallestarifas_set-%s-detperiodo' % numero, 'innerHTML', ''.join(out))
    return dajax.json()




@dajaxice_register
def calcula_costes(request, tipo):
    dajax = Dajax()
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    lista = calculoTotalEnergia(tipo,dia,mes,ano)
    out=[]
    for val in lista:
        out.append("<tr> <td> %s </td> <td> %s </td> <td> %s </td></tr>" % (val[0],val[1],val[2]) )

    id = '#dia' if tipo=="D" else ('#mes' if tipo=="M" else "#ano")
    dajax.assign(id, 'innerHTML', ''.join(out))
    return dajax.json()

@dajaxice_register
def grafico_dia(request):
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    sql=('select dia,per,ejer,hora, sum(energia) from lecturas_consumoshoras  where dia=%s and per=%s and ejer=%s  %s group by dia,per,ejer,hora order by hora' % (dia,mes,ano,sentenciaSensores() ) )
    cur  = connection.cursor()
    cur.execute(sql)
    entries = [([[tiempoenMil(row[0],row[1],row[2],row[3],0), ponCero(row[4])]]) for row in cur.fetchall()]
    return simplejson.dumps(entries)


@dajaxice_register
def grafico_semana(request):
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    nsemana = noSemana(dia,mes,ano)
    sql       = (""" select  dia,per,ejer,sum(energia) from lecturas_consumosdias   where  per = """+str(mes)+"""  and ejer="""+str(ano)+ """  %s group by semana """ % sentenciaSensores() )
    print sql
    #sql=("""select  strftime('%%w',date(cast(ejer as varchar(2)) || "-"|| cast(per as varchar(2)) ||"-"|| cast(dia as varchar(2)) ) ) ,sum(energia) promedio  from (select dia,per,ejer,hora,avg(energia) energia from lecturas_consumos  where strftime('%%W',date(cast(ejer as varchar(2)) || "-"|| cast(per as varchar(2)) ||"-"|| cast(dia as varchar(2)) ) ) ="%s" and ejer=%s  group by hora,dia,per,ejer)  group by strftime('%%w',date(cast(ejer as varchar(2)) || "-"|| cast(per as varchar(2)) ||"-"|| cast(dia as varchar(2)) ) ) order by 1 """ % (nsemana,ano))
    cur  = connection.cursor()
    cur.execute(sql)
    entries = [([[ tiempoenMil(row[0],row[1],row[2],0,0), ponCero(row[3])] ]) for row in cur.fetchall()]
    return simplejson.dumps(entries)


@dajaxice_register
def grafico_mes(request):
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    nsemana =hoy.strftime("%W")
    sql =('select dia,per,ejer,sum(energia) promedio from lecturas_consumosdias where per=%s and ejer=%s %s group by dia,per,ejer order by dia ' % (mes,ano,sentenciaSensores()))
    cur  = connection.cursor()
    cur.execute(sql)
    entries = [([[tiempoenMil(row[0],row[1],row[2],0,0)  , ponCero(row[3])]]) for row in cur.fetchall()]
    return simplejson.dumps(entries)


@dajaxice_register
def grafico_ano(request):
    hoy = datetime.datetime.now()
    dia = hoy.day
    mes = hoy.month
    ano = hoy.year
    nsemana =hoy.strftime("%W")
    sql = ('select  per, sum(energia) promedio  from (select dia,per,ejer,hora,avg(energia) energia from lecturas_consumosmes where ejer=%s %s group by hora,dia,per,ejer) group by per order by 1' % (ano,sentenciaSensores()))
    cur  = connection.cursor()
    cur.execute(sql)
    entries = [([[row[0], ponCero(row[1])]]) for row in cur.fetchall()]
    return simplejson.dumps(entries)


@dajaxice_register
def comprobarLectura(request):
    valor= testLectura()
    return simplejson.dumps(valor)


@dajaxice_register
def conectarLectura(request):
    valor=testLectura()
    if valor==0:
        leer = leeDatos()
        valor = 1
    return simplejson.dumps(valor)