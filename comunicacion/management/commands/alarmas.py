# -*- coding: utf-8 -*-
# __author__ = 'julian'
from os import path
from lecturas.GetDataFromCurrentCostMeter import leeDatos
from gconsumos import settings
import datetime
from pysqlite2 import dbapi2 as sqlite
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from maestros.models import Terceros
from web.ajax import testLectura
from web.models import Configuracion
from lecturas.currentcostdb import *

class Command(BaseCommand):
    hoy  = datetime.datetime.now()
    dia  = datetime.datetime.now().day
    mes  = datetime.datetime.now().month
    ano  = datetime.datetime.now().year
    hora = datetime.datetime.now().hour
    minu = datetime.datetime.now().minute
    conexion=""

    #tiempo en minutos
    def normalizatiempo(self,hora,minutos):
        return ((int(str(hora))*60)+int(str(minutos)))

    def __init__(self):
        try:
            self.conexion = sqlite.connect(settings.DATABASE , detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        except sqlite.OperationalError, e:
            print e.message

    def envio(self, body,destino,subject,attach=None):
        from comunicacion import mailer
        yo = 'info@infinityloop.es'
        message = mailer.Message()
        message.From = yo
        message.To = destino
        message.Subject = subject
        message.Body = body
        message.attach(attach)
        mailer = mailer.Mailer('localhost')
        mailer.send(message)


    def buscarUno(self,sql):
        try:
            cursor =self.conexion.cursor()
            cursor.execute(sql)
        except sqlite.DataError,e:
            print e.message
        return cursor.fetchone()

    def  buscarTodos(self,sql):
        try:
            cursor =self.conexion.cursor()
            cursor.execute(sql)
        except sqlite.DataError,e:
            print e.message
        return cursor.fetchall()


    def seleccionTipoAlarma(self, tipo):
        sql= "select id,descripcion,consigna,tiempoinicio,tiempofin,idcomsumos_id,sensibilidad from web_alarmas where tipo=%s and habilitar='1' " % tipo
        return self.buscarTodos(sql)

    def selecionarEnvio(self, id):
        sql = "select email_destino1,cuerpomensaje from web_mensajes where alarma_id=%s " % id
        return self.buscarTodos(sql)


    def verificarUltimaHora(self,sentencia):
        sql = "select max(energia) from lecturas_consumoshoras where dia=%s and per=%s and ejer=%s and hora-1<=%s and hora+1>=%s %s" % (self.dia,self.mes,self.ano,self.hora,self.hora,sentencia)
        return self.buscarUno(sql)

    def verificarUltimoMinuto(self,sentencia):
        if self.minu-5 <0:
            hora1 = self.hora-1
            self.minu = 55
        sql = "select max(energia) from lecturas_consumostmp where dia=%s and per=%s and ejer=%s and hora=%s and min+5>=%s  and min-5<=%s  %s" % (self.dia,self.mes,self.ano,self.hora,self.minu,self.minu,sentencia)
        return self.buscarUno(sql)


    def nulos(self,valor):
        if  valor is None:
            return 0
        else:
            return valor[0]

    def componerMensaje(self, txt,subject,datosmensaje):
        for datosm in datosmensaje:
            txt_envio = datosmensaje[0][1]+"\n"+txt
            self.envio(txt_envio,datosm[0],subject,None)

    def volcadoHoras(self,parchivo):
        query = ConsumosHoras.objects.raw("select * from lecturas_consumoshoras where  datetime(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))||' '||substr('0'||hora,length(hora))||':'||'00' ) between datetime('now','-120 minutes') and datetime('now')")
        if len(list(query))==0:
            return False
        archivo   = open(parchivo,"w")
        archivo.write("dia;mes;ano;hora;watts,sensor\n")
        for linf in query:
            archivo.write("%s;%s;%s;%s;%s;%s\n" % (linf.dia,linf.per,linf.ejer,linf.hora,round(linf.energia,0),linf.idcomsumos)  )
        archivo.close()
        return True

    def volcadoDiario(self,parchivo):
        query = ConsumosHoras.objects.raw("select * from lecturas_consumoshoras where  datetime(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))||' '||substr('0'||hora,length(hora))||':'||'00' ) between datetime('now','-1 days') and datetime('now')")
        if len(list(query))==0:
            return False
        archivo   = open(parchivo,"w")
        archivo.write("dia;mes;ano;hora;watts;sensor\n")
        for linf in query:
            archivo.write("%s;%s;%s;%s;%s;%s\n" % (linf.dia,linf.per,linf.ejer,linf.hora,round(linf.energia,0),linf.idcomsumos)  )
        archivo.close()
        return True

    def volcadoSemanal(self,parchivo):
        query = ConsumosHoras.objects.raw("select * from lecturas_consumoshoras where  datetime(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))||' '||substr('0'||hora,length(hora))||':'||'00' ) between datetime('now','-7 days') and datetime('now')")
        if len(list(query))==0:
            return False
        archivo   = open(parchivo,"w")
        archivo.write("dia;mes;ano;hora;watts;sensor\n")
        for linf in query:
            archivo.write("%s;%s;%s;%s;%s;%s\n" % (linf.dia,linf.per,linf.ejer,linf.hora,round(linf.energia,0),linf.idcomsumos)  )
        archivo.close()
        return True
    def volcadoMensual(self,parchivo):
        query = ConsumosHoras.objects.raw("select * from lecturas_consumoshoras where  datetime(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))||' '||substr('0'||hora,length(hora))||':'||'00' ) between datetime('now','-30 day') and datetime('now')")
        if len(list(query))==0:
            return False
        archivo   = open(parchivo,"w")
        archivo.write("dia;mes;ano;hora;watts;sensor\n")
        for linf in query:
            archivo.write("%s;%s;%s;%s;%s;%s\n" % (linf.dia,linf.per,linf.ejer,linf.hora,round(linf.energia,0),linf.idcomsumos)  )
        archivo.close()
        return True

    def volcado(self):
        volcado = Configuracion.objects.all()[0]
        if len(volcado.protvolcado)==0:
            return
        else:
            if volcado.protvolcado=="email":
                if volcado.frecuencia=="01":
                    archivo="/tmp/horas.csv"
                    if self.volcadoHoras(archivo):
                        txt ="Volcado de Webloggeer Horaria"
                    else:
                        return
                if volcado.frecuencia=="02":
                    archivo="/tmp/diario.csv"
                    if self.volcadoDiario(archivo):
                        txt ="Volcado de Webloggeer Diario"
                    else:
                        return
                if volcado.frecuencia=="03":
                    archivo="/tmp/semanal.csv"
                    if self.volcadoSemanal(archivo):
                        txt ="Volcado de Webloggeer Semanal"
                    else:
                        return
                if volcado.frecuencia=="04":
                    archivo="/tmp/mensual.csv"
                    if self.volcadoMensual(archivo):
                        txt ="Volcado de Webloggeer Mensual"
                    else:
                        return
                self.envio( txt,volcado.emailvolcado,"Envio de datos consumo Weblogger %s " % volcado.serialmodulo,archivo)




    def verificar(self):

        txt_envio=""
        txt=""
        verifico=[]
        tiposdealarma = [('1','Historico'),('2','Predictivo'),('3','Restrictiva Maximo'),('4','Restrictiva Minimo')]
        verifiH=self.seleccionTipoAlarma(tiposdealarma[0][0])
        verifiP=self.seleccionTipoAlarma(tiposdealarma[1][0])
        verifiR=self.seleccionTipoAlarma(tiposdealarma[2][0])
        verifiM=self.seleccionTipoAlarma(tiposdealarma[3][0])

        if verifiH !=[]:
            sensor      = verifiH[0][5]
            sensibilidad = verifiH[0][6]
            if sensor is None:
                sentencia = "and 1=1"
                descrp    =""
            else:
                sentencia = "and idcomsumos_id = %s" % sensor
                descrp    = "Sensor N.%s" % sensor

            energiaactual      = self.nulos(self.verificarUltimoMinuto(sentencia))
            if sensibilidad == "1":
                try:
                    energia = EstaAcumHora.objects.get(hora = self.hora , idcomsumos_id = sensor).energia
                except EstaAcumHora.DoesNotExist:
                    energia=0
            if sensibilidad =="2":
                diasem  = datetime.date.today().isoweekday()
                if  diasem==7:
                    diasem =0

                try:
                    energia = EstaAcumDiaSema.objects.get(hora=self.hora, idcomsumos_id =sensor,diasemana=diasem ).energia
                except EstaAcumDiaSema.DoesNotExist:
                    energia=0
            if sensibilidad =="3":
                try:
                    energia = EstaAcumMes.objects.get(hora=self.hora, idcomsumos_id=sensor, per =self.mes).energia
                except EstaAcumMes.DoesNotExist:
                    energia=0


            if energiaactual > energia:
                datosmensaje = self.selecionarEnvio(verifiH[0][0])
                txt = "exceso de consumo de %s watts supera la consigna  historica %s watts %s " % (energiaactual,energia,descrp)
                subject = "Aviso generado hora: %s  del %s-%s-%s %s " %(self.hora,self.dia,self.mes,self.ano,descrp)
                self.componerMensaje(txt,subject,datosmensaje)


        if verifiP !=[]:
            #Hacer analisis Predictivo
            pass
        if verifiR !=[]:
            #Conseguimos consumo la utltima hora y si se ha excedido enviamos email.
            hinicio      = verifiR[0][3].hour
            minicio      = verifiR[0][3].minute
            hfin         = verifiR[0][4].hour
            minfin       = verifiR[0][4].minute
            sensor       = verifiR[0][5]
            #Genera sentencia sql para consulta por canales
            if sensor is None:
                sentencia = "and 1=1"
                descrp    =""
            else:
                sentencia = "and idcomsumos_id = %s" % sensor
                descrp    = "Sensor N.%s" % sensor

            if  self.normalizatiempo(hinicio,minicio) < self.normalizatiempo(self.hora,self.minu) and self.normalizatiempo(hfin,minfin) > self.normalizatiempo(self.hora,self.minu):
                energia      = self.nulos(self.verificarUltimoMinuto(sentencia))
                if energia >= verifiR[0][2]:
                    datosmensaje = self.selecionarEnvio(verifiR[0][0])
                    txt = "exceso de consumo de %s watts supera la consigna %s watts %s " % (energia,verifiR[0][2],descrp)
                    subject = "Aviso generado hora: %s  del %s-%s-%s %s " %(self.hora,self.dia,self.mes,self.ano,descrp)
                    self.componerMensaje(txt,subject,datosmensaje)

        if verifiM !=[]:
            #Conseguimos consumo la utltima hora y si se ha excedido enviamos email.
            hinicio      = verifiM[0][3].hour
            minicio      = verifiM[0][3].minute
            hfin         = verifiM[0][4].hour
            minfin       = verifiM[0][4].minute
            sensor       = verifiM[0][5]
            #Genera sentencia sql para consulta por canales
            if sensor is None:
                sentencia = "and 1=1"
                descrp    =""
            else:
                sentencia = "and idcomsumos_id = %s" % sensor
                descrp    = "Sensor N.%s" % sensor

            if  self.normalizatiempo(hinicio,minicio) < self.normalizatiempo(self.hora,self.minu) and self.normalizatiempo(hfin,minfin) > self.normalizatiempo(self.hora,self.minu):
                energia      = self.nulos(self.verificarUltimoMinuto(sentencia))

                if energia <= verifiM[0][2]:
                    datosmensaje = self.selecionarEnvio(verifiM[0][0])
                    txt = "minimo consumo de %s watts inferior a la consigna %s watts %s " % (energia,verifiM[0][2],descrp)
                    subject = "Aviso generado hora: %s  del %s-%s-%s %s " %(self.hora,self.dia,self.mes,self.ano,descrp)
                    self.componerMensaje(txt,subject,datosmensaje)


    option_list = BaseCommand.option_list + (
        make_option('--estado',
            action='store_true',
            dest='comunica',
            default=False,
            help='Comprueba estado de la comunicacion con EnviR'),
        make_option('--alarmas',
            action='store_true',
            dest='alarmas',
            default=False,
            help='Supervision alarmas'),
        make_option('--reconciliar',
            action='store_true',
            dest='reconciliar',
            default=False,
            help='Reconstruir resumenes datos'),
        make_option('--reconstruir',
            action='store_true',
            dest='reconstruir',
            default=False,
            help='Limpia y reconstruye resumenes datos'),
        make_option('--estadistica',
            action='store_true',
            dest='estadistica',
            default=False,
            help='Limpia y reconstruye resumenes datos'),
        make_option('--volcado',
            action='store_true',
            dest='volcado',
            default=False,
            help='Comprueba que el volcado esta habilitado'),

        )


    def handle(self, *args, **options):

        if options['comunica']:
            swt=0
            if testLectura() != 1:
                try:
                    email  = Terceros.objects.filter(tipotercero_id=1)[0].email
                except Terceros.DoesNotExist:
                    swt=1
                try:
                    serial = Configuracion.objects.all()[0].serialmodulo
                except Configuracion.DoesNotExist:
                    swt=1
                if swt==0:
                    self.envio("Perdida de comunicacion con el ENVIR No. %s" % serial,email,'Sin comunicación EnviR, intente reconectar el Envir',None)
                    lee = leeDatos()

        if options['alarmas']:
            self.verificar()

        if options['reconciliar']:
            cdb = CurrentCostDB()
            cdb.InitialiseDB(settings.DATABASE)
            cdb.ReconciliarData(False)

        if options['reconstruir']:
            cdb = CurrentCostDB()
            cdb.InitialiseDB(settings.DATABASE)
            cdb.ReconciliarData(True)

        if options['estadistica']:
            cdb = CurrentCostDB()
            cdb.InitialiseDB(settings.DATABASE)
            cdb.ReconciliarEstaData()

        if options['volcado']:
            self.volcado()


