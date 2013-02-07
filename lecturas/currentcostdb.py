# -*- coding: utf-8 -*-

#
# CurrentCost GUI
# 
#    Copyright (C) 2008  Dale Lane
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#  The author of this code can be contacted at Dale.Lane@gmail.com
#    Any contact about this application is warmly welcomed.
#
import logging
from pysqlite2 import dbapi2 as sqlite
import datetime, time

#
# We use a SQLite database to persist data - both historical CurrentCost data,
#   and user preferences and settings.
# 
# This class is used to provide the database.
# 
# 
#  Dale Lane (http://dalelane.co.uk/blog)
from django.db import transaction
from lecturas.models import ConsumosAnos, ConsumosMes, ConsumosDias, ConsumosHoras, EstaAcumMes, EstaAcumDiaSema, EstaAcumHora

trc =logging.getLogger('lecturas.currentcostdb')


class CurrentCostDB():

    # connection to the database
    connection = None

    # what is the path to the database used to store CurrentCost data?
    dbLocation = ""

    # connect to the database
    #
    # create tables if not already found
    # 
    def InitialiseDB(self, dbfilepath):
        self.dbLocation = dbfilepath

        self.connection = sqlite.connect(dbfilepath, detect_types=sqlite.PARSE_DECLTYPES|sqlite.PARSE_COLNAMES)
        cursor = self.connection.cursor()

        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="settings" ORDER BY name')
        if not cursor.fetchone():
            cursor.execute('CREATE TABLE settings(settingkey TEXT unique, settingvalue TEXT)')

        cursor.execute('SELECT name FROM sqlite_master WHERE type="table" AND NAME="lecturas_consumos_tmp" ORDER BY name')
#        if not cursor.fetchone():
#            cursor.execute('CREATE TABLE lecturas_consumos_tmp(ts timestamp   unique,  idconsumo INT, ejer INT, per INT, dia INT, hora INT, min INT,seg INT, energia REAL )')
#            cursor.execute('CREATE TABLE lecturas_consumos_horas(ts timestamp unique,  idconsumo INT, ejer INT, per INT, dia INT, hora INT, energia REAL )')
#            cursor.execute('CREATE TABLE lecturas_consumos_dias(ts timestamp  unique,  idconsumo INT, ejer INT, per INT, dia INT,  energia REAL, semana INT )')
#            cursor.execute('CREATE TABLE lecturas_consumos_mes(ts timestamp   unique,  idconsumo INT, ejer INT, per INT, energia REAL )')
#            cursor.execute('CREATE TABLE lecturas_consumos_anos(ts timestamp   unique, idconsumo INT, ejer INT, per INT, energia REAL )')
#            cursor.execute('CREATE INDEX "ejercicio" on lecturas_consumos_anos (ejer ASC)')
#            cursor.execute('CREATE INDEX "ep" on lecturas_consumos_mes (ejer ASC, per ASC)')
#            cursor.execute('CREATE INDEX "epd" on lecturas_consumos_dias (ejer ASC, per ASC, dia ASC )')
#            cursor.execute('CREATE INDEX "epdh" on lecturas_consumos_horas (ejer ASC, per ASC, dia ASC, hora ASC)')





        self.connection.commit()

    #
    # disconnect from the database
    # 
    # the connection is unusable after calling this
    # 
    def CloseDB(self):
        if self.connection != None:
            self.connection.close()



    # store a key-value pair in the database
    def StoreSetting(self, key, value):
        self.connection.execute('INSERT OR REPLACE INTO settings(settingkey, settingvalue) values(?, ?)',
                                (key, value))
        self.connection.commit()

    # retrieve the value from a key-value pair in the database
    def RetrieveSetting(self, key):
        cursor = self.connection.cursor()
        cursor.execute('SELECT settingkey, settingvalue FROM settings WHERE settingkey="' + key + '"')
        row = cursor.fetchone()
        if row:
            return row[1]
        else:
            return None

    #
    ############################################################
    # helper functions for storing data in the database
    # 
    ############################################################
    #

    def validaEnergia(self,cursor):
        energia = cursor.fetchone()
        if energia == None:
            energia=0
        else:
            energia=energia[0]

        return energia


    def StoreConsumoData(self, timestamp, primary, ejer,per,dia,energia,sensor):
        if energia > 0:
            hora,min,seg=timestamp.split(":")
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumostmp(ts, ejer, per, dia, hora,min,seg,energia,idcomsumos_id) values(?, ?, ?, ?, ?, ?, ?, ?, ?)', (primary,ejer,per,dia, hora, min,seg,energia,sensor) )
            self.connection.commit()


    def StoreConsumoHoras(self, hora, primary, ejer,per,dia,sensor):
        cursor =self.connection.execute(" " " select avg(energia) energia from lecturas_consumostmp  where dia=%s and per=%s and ejer=%s and hora=%s  and idcomsumos_id=%s group by hora,dia,per,ejer" " " % (dia,per,ejer,hora,sensor))
        energia = self.validaEnergia(cursor)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumoshoras(ts, ejer, per, dia, hora, energia,idcomsumos_id) values(?, ?, ?, ?, ?, ?,?)',
                (primary,ejer,per,dia, hora,energia,sensor) )
            self.connection.commit()

    def StoreConsumoDias(self,  primary, ejer,per,dia,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumoshoras  where dia=%s and per=%s and ejer=%s and idcomsumos_id=%s" " " % (dia,per,ejer,sensor))
        energia = self.validaEnergia(cursor)
        trc.info("Energia a grabar en dia %s" % energia)
        if energia > 0:
            diasemana ="%s-%s-%s" % (dia,per,ejer)
            semana = datetime.datetime.strptime(diasemana,"%d-%m-%Y").strftime("%W")
            trc.info("Graba dia %s-%s-%s " % (dia,per,ejer))
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosdias(ts, ejer, per, dia, energia, semana, idcomsumos_id) values(?, ?, ?, ?, ?, ?, ? )',
                (primary,ejer,per,dia,energia,semana,sensor) )
            self.connection.commit()

    def StoreConsumoMes(self,  primary, ejer,per,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumosdias  where per=%s and ejer=%s and idcomsumos_id=%s" " " % (per,ejer,sensor))
        energia = self.validaEnergia(cursor)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosmes(ts, ejer, per,energia,idcomsumos_id) values(?, ?, ?, ?,?)',
                (primary,ejer,per,energia,sensor) )
            self.connection.commit()

    def StoreConsumoAno(self,  primary, ejer ,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumosmes  where  ejer=%s and idcomsumos_id=%s " " " % (ejer,sensor) )
        energia = self.validaEnergia(cursor)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosanos(ts, ejer, energia,idcomsumos_id) values(?, ?, ?,?)',
                (primary,ejer,energia,sensor) )
            self.connection.commit()

    # COUNT THE NUMBER OF OBJECTS IN THE DATABASE
    def CountConsumoData(self):
        cnt = 0
        for row in self.connection.execute("SELECT * FROM lecturas_consumos"):
            cnt += 1
        return cnt

    def validaAhora(self,pejer,pper=0,pdia=0,phora=0):
        #Hora, Dia ,Mes y Ano Actual no se toman encuenta para la reconciliación
        #Limitacion no lanzar proceso a las 00:00 horas
        hoy  = datetime.datetime.now()
        dia  = str(hoy.day)
        mes  = str(hoy.month)
        ano  = str(hoy.year)
        hora = str(hoy.hour)
        if phora=="0" and pdia!="0" and pper!="0" :
            if dia==pdia and mes==pper and ano==pejer:
                return False
        if pdia=="0" and pper!="0" and phora=="0":
            if  mes==pper and ano==pejer:
                return False
        if pper=="0" and pdia=="0" and phora=="0":
            if pejer==ano:
                return False
        if phora==hora and pdia==dia and pper==mes and pejer==ano:
                return False
        return True

    #Reconstruye todos los resumenes
    def ReconciliarData(self, limpiar):



        if limpiar:
            ConsumosAnos.objects.all().delete()
            ConsumosMes.objects.all().delete()
            ConsumosDias.objects.all().delete()
            ConsumosHoras.objects.all().delete()


        sql_tmp_res   ="select  ejer,per,dia,hora,idcomsumos_id,max(ts) tiempo from lecturas_consumostmp group by ejer,per,dia,hora,idcomsumos_id order by ejer,per,dia,hora"
        sql_horas     ="select 1 from lecturas_consumoshoras where ejer=? and per=? and dia=? and hora=? and idcomsumos_id=?"
        sql_horas_res ="select  ejer,per,dia,idcomsumos_id,max(ts) tiempo from lecturas_consumoshoras group by ejer,per,dia,idcomsumos_id order by ejer,per,dia"
        sql_dias      ="select 1 from lecturas_consumosdias  where ejer=? and per=? and dia=? and idcomsumos_id=? "
        sql_dias_res  ="select  ejer,per,idcomsumos_id,max(ts) tiempo from lecturas_consumosdias group by ejer,per,idcomsumos_id order by ejer,per"
        sql_mes       ="select 1 from lecturas_consumosmes where ejer=? and per=? and idcomsumos_id=? "
        sql_mes_res   ="select ejer,idcomsumos_id,max(ts) tiempo from lecturas_consumosmes  group by ejer,idcomsumos_id order by ejer"
        sql_ano       ="select 1 from lecturas_consumosanos where ejer=? and idcomsumos_id=?"

        #Reconcilia Horas
        cursor_tmp = self.connection.execute(sql_tmp_res)
        for reg in cursor_tmp:
            if self.validaAhora(str(reg[0]),str(reg[1]),str(reg[2]),str(reg[3])):
                cursor_horas = self.connection.execute(sql_horas,(reg[0],reg[1],reg[2],reg[3],reg[4]) )
                existe = self.validaEnergia(cursor_horas)
                cursor_horas
                if existe ==0:
                    primaria = str(reg[5])
                    self.StoreConsumoHoras(reg[3],primaria,reg[0],reg[1],reg[2],reg[4])


        #Reconcilia Dias
        cursor_horas_res = self.connection.execute(sql_horas_res)
        for reg in cursor_horas_res:
            if self.validaAhora(str(reg[0]),str(reg[1]),str(reg[2]),"0"):
                cursor_dias = self.connection.execute(sql_dias, (reg[0],reg[1],reg[2],reg[3]))
                existe = self.validaEnergia(cursor_dias)
                if existe==0:
                    primaria = str(reg[4])
                    self.StoreConsumoDias(primaria,reg[0],reg[1],reg[2],reg[3])

        #Reconcilia Mes
        cursor_dias_res = self.connection.execute(sql_dias_res)
        for reg in cursor_dias_res:
            if self.validaAhora(str(reg[0]),str(reg[1]),"0","0"):
                cursor_mes = self.connection.execute(sql_mes,(reg[0],reg[1],reg[2]))
                existe = self.validaEnergia(cursor_mes)
                if existe ==0:
                    primaria = str(reg[3])
                    self.StoreConsumoMes(primaria,reg[0],reg[1],reg[2])

        #Reconcilia Año
        cursor_mes_res = self.connection.execute(sql_mes_res)
        for reg in cursor_mes_res:
            if self.validaAhora(str(reg[0]),"0","0","0"):
                cursor_ano = self.connection.execute(sql_ano,(reg[0],reg[1]))
                existe = self.validaEnergia(cursor_ano)
                if existe==0:
                    primaria = str(reg[2])
                    self.StoreConsumoAno(primaria,reg[0],reg[1])

    @transaction.commit_manually
    def ReconciliarEstaData(self):


        EstaAcumMes.objects.all().delete()
        EstaAcumDiaSema.objects.all().delete()
        EstaAcumHora.objects.all().delete()

        sql_horas   ="select hora,idcomsumos_id,avg(energia) energia from lecturas_consumoshoras  group by hora,idcomsumos_id"
        sql_mes     ="select per,hora,idcomsumos_id,avg(energia) energia from lecturas_consumoshoras  group by per,hora,idcomsumos_id"
        sql_diasem  ="select strftime('%w',(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))) ) diasemana,hora,idcomsumos_id,avg(energia) energia from lecturas_consumoshoras  group by hora,idcomsumos_id,strftime('%w',(ejer||'-'||substr('0'||per,length(per))||'-'||substr('0'||dia,length(dia))) ) order by 1"


        cursor_horas = self.connection.execute(sql_horas)
        for reg in cursor_horas:
            objhoras = EstaAcumHora(hora=reg[0],idcomsumos_id=reg[1],energia=round(reg[2],0))
            objhoras.save()
        transaction.commit()

        cursor_mes = self.connection.execute(sql_mes)
        for reg in cursor_mes:
            objmes = EstaAcumMes(per=reg[0],hora=reg[1],idcomsumos_id=reg[2],energia=round(reg[3],0))
            objmes.save()
        transaction.commit()

        cursor_diasem = self.connection.execute(sql_diasem)
        for reg in cursor_diasem:
            objdia = EstaAcumDiaSema(diasemana=reg[0],hora=reg[1],idcomsumos_id=reg[2],energia=round(reg[3],0))
            objdia.save()
        transaction.commit()
