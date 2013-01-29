import serial
import datetime
import time
import os
from lecturas.currentcostparser import CurrentCostDataParser
from lecturas.currentcostdb import CurrentCostDB
from gconsumos import settings
from tracer import CurrentCostTracer
from serialconn import CurrentCostConnection
from web.utils import list_get_egfp
import logging

trc =logging.getLogger('lecturas.GetDataFromCurrentCostMeter')


class leeDatos:

    myserialconn = CurrentCostConnection()
    myparser     = CurrentCostDataParser()
    ccdb         = CurrentCostDB()

    def __init__(self):
        if self.myserialconn.isConnected():
            self.myserialconn.disconnect()
        self.ccdb.InitialiseDB(settings.PROJECT_ROOT+"/datos/datos.ccd")
        self.getDataFromCurrentCostMeter("/dev/ttyUSB0")

    def conecta(self,portdet):
        try:
            # connect to the CurrentCost meter
            #
            # we *hope* that the serialconn class will automatically handle what
            # connection settings (other than COM port number) are required for the
            # model of CurrentCost meter we are using
            #
            # the serialconn class does not handle serial exceptions - we need to
            # catch and handle these ourselves
            # (the only exception to this is that it will close the connection
            #  in the event of an error, so we do not need to do this explicitly)
            self.myserialconn.connect(portdet)
        except serial.SerialException, msg:
            trc.error("Fallo al conectar al CurrentCost meter")
            return False
        except:
            trc.error("Fallo al conectar al CurrentCost meter")
            return False

    def numberEmptyArray(self,array):
        long= len(array)
        numero = 0
        for i in range(0,long):
            if len(array[i])!=0:numero += 1
        return numero

    def grabarConsumos(self,aDatos):
        tiempo = ""
        ano = 0
        mes = 0
        ano = 0
        dia = 0
        energia  = 0
        promedio = 0
        nd     = 1
        switch = 0
        for datos in aDatos:
            tiempo = datos['tiempo']
            if switch == 0:
                inihora, min, seg = tiempo.split(":")
                iniano = datos['ano']
                inimes = datos['mes']
                inidia = datos['dia']
                switch = 1
            ano = datos['ano']
            mes = datos['mes']
            dia = datos['dia']
            energia = float(str(datos['potencia']))
            senso   = datos['sensor']
            hora, min, seg = tiempo.split(":")
            id = ano + mes + dia + tiempo
            if hora != inihora:
                trc.info("Entra en Hora .................................................")
                self.ccdb.StoreConsumoData(tiempo, id, ano, mes, dia, str((promedio / nd)),senso)
                self.ccdb.StoreConsumoHoras(inihora, id, iniano, inimes, inidia,senso)
                inihora = hora
                if inidia != dia:
                    time.sleep(5)
                    trc.info("Entra en dias .............................................")
                    self.ccdb.StoreConsumoDias(tiempo, id, iniano, inimes, inidia,senso)
                    inidia = dia
                    if inimes != mes:
                        time.sleep(5)
                        self.ccdb.StoreConsumoMes(tiempo, id, iniano, inimes,senso)
                        inimes = mes
                        ##Llam a Insertar Mes
                        if iniano != ano:
                            time.sleep(5)
                            self.ccdb.StoreConsumoAno(tiempo, id, iniano,senso)
                            iniano = ano
                            ##Llama a Inserta Ano
                            pass
                promedio = energia
                nd = 1
            promedio = energia + promedio
            nd = nd + 1
        trc.info("Grabando Sensor %s Energia %s" % ( str((promedio / nd)),senso))
        self.ccdb.StoreConsumoData(tiempo, id, ano, mes, dia, str((promedio / nd)),senso)
        return []


    def getDataFromCurrentCostMeter(self,portdet):
        #Arreglo para 10 sensores reset cada 5 minutos
        aDatos=[[],[],[],[],[],[],[],[],[],[]]
        trc.info('Connecting to local CurrentCost meter - using device "' + portdet)
        reuseconnection = self.myserialconn.isConnected()
        if reuseconnection == False:
            self.conecta(portdet)

        currentcoststruct = None
        updatesremaining = 1
        sincap = 0
        loopMessage = "Waiting for data from CurrentCost meter"
        trc.info(loopMessage)
        inicio = 0
        while updatesremaining > 0:
            #Linea para recibir datos
            line = ""

            while len(line) == 0:
                try:
                    line = self.myserialconn.readUpdate()
                except serial.SerialException, err:
                    trc.error('Failed to receive data from CurrentCost meter')
                    return False
                except Exception, msg:
                    trc.error('Failed to receive data from CurrentCost meter')
                    return False



            # try to parse the XML

            currentcoststruct = self.myparser.parseCurrentCostXML(line)


            #print "Linea cruda %s " % currentcoststruct
            #Si linea cruda es demasiada lectura que reinicie la conexion
            if currentcoststruct is None:
                sincap = sincap + 1
                trc.info("Esperando conexion No. %s" % sincap)
                if sincap > 8:
                    self.myserialconn.disconnect()
                    time.sleep(2)
                    reuseconnection = self.myserialconn.isConnected()
                    if reuseconnection == False:
                        trc.info("Intentando conectar...")
                        self.conecta(portdet)
                    sincap = 0
            if currentcoststruct is not None:

                sincap = 0
                #Solucionar problema de cambio de hora cuando sea media noche, en caso
                tiempo = currentcoststruct['msg']['time']
                hora, minuto, seg = tiempo.split(':')
                dia = str(datetime.datetime.now().day)
                mes = str(datetime.datetime.now().month)
                ano = str(datetime.datetime.now().year)
                if inicio == 0:
                    #Sincroniza fecha del Sistema con Envir
                    fecha = ('date -s "%s/%s/%s %s:%s:%s" ') % ( ano, mes, dia, hora, minuto, seg)
                    os.system(fecha)
                    inicio = time.time()

                if 'hist' not in currentcoststruct['msg']:
                    try:
                        trc.info("Consumos Watts %s  Sensor : %s " % (currentcoststruct['msg']['ch1']['watts'], int(str(currentcoststruct['msg']['sensor']))) )
                        potencia    = currentcoststruct['msg']['ch1']['watts']
                        sensor      = int(str(currentcoststruct['msg']['sensor']))
                        temperatura = currentcoststruct['msg']['tmpr']
                        aDatos[sensor].append({'tiempo': tiempo, 'id': ano + mes + dia + tiempo, 'ano': ano, 'mes': mes, 'dia': dia,
                                       'potencia': potencia, 'temperatura': temperatura,'sensor':sensor})

                    except KeyError:
                        trc.error("Error de lectura de alguna clave")

                    fin = time.time()
                    muestreo=300
                    if fin - inicio > muestreo:
                        trc.info("Graba al minuto %s" % (fin - inicio))
                        nsensor=9
                        for num in range(0,nsensor):
                            if len(list_get_egfp(aDatos,num))!=0:
                                aDatos[num] = self.grabarConsumos(aDatos[num])
                        trc.info("Finaliza Grabacion %s" % (fin - inicio))

                        inicio = 0

        return True

