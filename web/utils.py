# -*- coding: utf-8 -*-
import calendar
import datetime
from decimal import Decimal
from django.db import connection
from maestros.models import DetallesTarifas, DetPeriodosHorarios
from web.models import PtdMedida, Generales, Contrato

__author__ = 'julian'


def sentenciaSensores():
    #Numero de Sensores a Totalizar
    litsenso=""
    sensores = map(lambda x:int(x[0]),PtdMedida.objects.filter(totaliza=True).values_list('id'))
    if len(sensores)>=1:
        for senso in sensores:
            litsenso = litsenso+"%s," % senso
        sentencia = "and idcomsumos_id in (%s)" % litsenso.strip(",")
    else:
        sentencia= "and 1=1"
    return sentencia

def ponCero(valor):
    if valor ==None:
        return 0
    else:
        return round(valor,2)


def validaEnergia(cursor):
    energia = cursor.fetchone()[0]
    if energia == None:
        energia=0.0
    else:
        energia=round(energia,2)

    return energia

def avalidaEnergia(cursor):
    energia = cursor.fetchone()
    if energia[0] == None:
        eenergia=0.0
    else:
        eenergia=round(energia[0],2)

    return [eenergia,energia[1]]


def noSemana(dia,per,ejer):
    diasemana ="%s-%s-%s" % (dia,per,ejer)
    semana = datetime.datetime.strptime(diasemana,"%d-%m-%Y").strftime("%W")
    return semana

def tiempoenMil(dia,mes,ano,hora,min):
    tiempo = datetime.datetime.strptime("%s-%s-%s %s:%s" %(dia,mes,ano,hora,min), "%d-%m-%Y %H:%M")
    return str(calendar.timegm(tiempo.timetuple())*1000)


def consultaTablas(tipo):
    hoy    = datetime.datetime.now()
    dia  = hoy.day
    mes  = hoy.month
    ano  = hoy.year
    min  = hoy.minute
    horas = hoy.hour
    nsemana = noSemana(dia,mes,ano)
    sentencia = sentenciaSensores()
    if nsemana !="1":
        nsemana = int(nsemana)-1
    if mes==1:
        nmes    = 12
        nano    = ano-1
    else:
        nmes=mes
        nano=ano

    if tipo=='24':
        sql  = ('select dia,per,ejer,hora,min, avg(energia) energia from lecturas_consumostmp where dia=%s and per=%s and ejer=%s %s  group by dia,per,ejer,hora,min ' % (dia,mes,ano,sentencia) )
    if tipo=='semana':
        sql  = ('select dia,per,ejer, sum(energia) energia from lecturas_consumosdias where semana=%s and ejer=%s %s  group by dia,per,ejer' % (nsemana,ano,sentencia) )
    if tipo=='mes':
        sql  = ('select dia,per,ejer, sum(energia) energia from lecturas_consumosdias where per=%s and ejer=%s %s group by dia,per,ejer ' % (nmes,nano,sentencia) )
    cur  = connection.cursor()
    cur.execute(sql)
    entries = cur.fetchall()
    return entries


def veranoInvierno(dia,mes,ano):
    #Calcula si estamos en horario de Verano o Invierno
    averano     = [ i for i in calendar.Calendar().itermonthdays2(ano, 3) if i[1] == calendar.SUNDAY and i[0] !=0  ][-1][0]
    ainvierno   = [ i for i in calendar.Calendar().itermonthdays2(ano, 10) if i[1] == calendar.SUNDAY and i[0] !=0  ][-1][0]
    fecha       = datetime.datetime.strptime('%s-%s-%s' % (dia,mes,ano),'%d-%m-%Y')
    fecaverano  = datetime.datetime.strptime('%s-%s-%s' % (averano,3,ano),'%d-%m-%Y')
    fecinvierno = datetime.datetime.strptime('%s-%s-%s' % (ainvierno,10,ano),'%d-%m-%Y')

    if ( fecha >=fecaverano and fecha<=fecinvierno):
        return 'V'
    else:
        return 'I'


def calculoTotalEnergia(tipo,dia,mes,ano):
    sentencia = sentenciaSensores()
    if tipo=="D":
        sql  = ('select hora,sum(energia) from lecturas_consumoshoras where  dia=%s  and per=%s and ejer=%s %s  group by hora order by hora' % (dia,mes,ano,sentencia) )
    if tipo =="M":
        sql  = ('select hora,sum(energia) from lecturas_consumoshoras where  per=%s and ejer=%s %s  group by hora order by hora' % (mes,ano,sentencia) )
    if tipo =="A":
        sql  = ('select hora,sum(energia) from lecturas_consumoshoras where  ejer=%s %s  group by hora order by hora' % (ano,sentencia) )
    cur = connection.cursor()
    cur.execute(sql)
    datos= cur.fetchall()

    tarifas  = DetallesTarifas.objects.filter(tfacceso=Contrato.objects.all()[0].tfacceso)
    gastos   =[]
    for tari in tarifas:
        v_i = veranoInvierno(dia,mes,ano)
        if tari.detperiodo.temporada == v_i:
            hini       = int(tari.detperiodo.intinicial)
            hfin       = int(tari.detperiodo.intfinal)
            deno       = tari.detperiodo.denoperiodo
            precio     = Decimal(tari.precio)
            ele        = filter( lambda (x,y): x>=hini and x<hfin, datos)
            if ele !=[]:
                totenergia = Decimal(reduce(lambda x,y :x+y,map(lambda (x,y): y,ele ) ))
                totimporte = totenergia*precio/1000
                gastos.append([deno,round(totenergia,2),round(totimporte,2)])

    return gastos


def list_get_egfp(L,i,v=None):
    try: return[i]
    except IndexError: return v