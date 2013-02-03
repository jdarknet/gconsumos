# -*- coding: utf-8 -*-
# __author__ = 'julian'
from lecturas.GetDataFromCurrentCostMeter import leeDatos
from gconsumos import settings
import datetime
import smtplib
from email.mime.text import  MIMEText
from pysqlite2 import dbapi2 as sqlite
from django.core.management.base import BaseCommand, CommandError
from optparse import make_option
from maestros.models import Terceros
from web.ajax import testLectura
from web.models import Configuracion


class Command(BaseCommand):

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

    def envio(self, descripcion,destino,subject):
        yo = 'info@infinityloop.es'
        #        fp = open( textfile,'rb')
        msg = MIMEText(descripcion)
        #        fp.close()
        msg['Subject']= subject
        msg['From']   = yo
        msg['To']     = destino
        s= smtplib.SMTP('localhost')
        s.sendmail(yo,destino,msg.as_string())
        s.quit()

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
        sql= "select id,descripcion,consigna,tiempoinicio,tiempofin,idcomsumos_id from web_alarmas where tipo=%s and habilitar='1' " % tipo
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
            #Hacer analisis del Historico
            pass
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
                datosmensaje = self.selecionarEnvio(verifiR[0][0])
                if energia >= verifiR[0][2]:
                    txt = "exceso de consumo de %s watts supera la consigna %s watts %s " % (energia,verifiR[0][2],descrp)
                    txt_envio = datosmensaje[0][1]+"\n"+txt
                    subject = "Aviso generado hora: %s  del %s-%s-%s %s " %(self.hora,self.dia,self.mes,self.ano,descrp)
                    self.envio(txt_envio,datosmensaje[0][0],subject)
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
                datosmensaje = self.selecionarEnvio(verifiM[0][0])
                if energia <= verifiM[0][2]:
                    txt = "minimo consumo de %s watts inferior a la consigna %s watts %s " % (energia,verifiM[0][2],descrp)
                    txt_envio = datosmensaje[0][1]+"\n"+txt
                    subject = "Aviso generado hora: %s  del %s-%s-%s %s " %(self.hora,self.dia,self.mes,self.ano,descrp)
                    self.envio(txt_envio,datosmensaje[0][0],subject)


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
                    self.envio("Perdida de comunicacion con el ENVIR No. %s" % serial,email,'Sin comunicación EnviR, intente reconectar el Envir')
                    lee = leeDatos()

        if options['alarmas']:
            self.verificar()