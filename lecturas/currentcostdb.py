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
        print "Energia promedio en hora %s   Watts: %s" %(hora,energia)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumoshoras(ts, ejer, per, dia, hora, energia,idcomsumos_id) values(?, ?, ?, ?, ?, ?,?)',
                (primary,ejer,per,dia, hora,energia,sensor) )
            self.connection.commit()

    def StoreConsumoDias(self, timestamp, primary, ejer,per,dia,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumoshoras  where dia=%s and per=%s and ejer=%s and idcomsumos_id=%s" " " % (dia,per,ejer,sensor))
        energia = self.validaEnergia(cursor)
        if energia > 0:
            diasemana ="%s-%s-%s" % (dia,per,ejer)
            semana = datetime.datetime.strptime(diasemana,"%d-%m-%Y").strftime("%W")
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosdias(ts, ejer, per, dia, energia, semana, idcomsumos_id) values(?, ?, ?, ?, ?, ?, ? )',
                (primary,ejer,per,dia,energia,semana,sensor) )
            self.connection.commit()

    def StoreConsumoMes(self, timestamp, primary, ejer,per,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumosdias  where per=%s and ejer=%s and idcomsumos_id=%s" " " % (per,ejer,sensor))
        energia = self.validaEnergia(cursor)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosmes(ts, ejer, per,energia,idcomsumos_id) values(?, ?, ?, ?,?)',
                (primary,ejer,per,energia,sensor) )
            self.connection.commit()

    def StoreConsumoAno(self, timestamp, primary, ejer ,sensor):
        cursor =self.connection.execute(" " " select sum(energia) energia from lecturas_consumosmes  where  ejer=%s and idcomsumos_id=%s " " " % (ejer,sensor) )
        energia = self.validaEnergia(cursor)
        if energia > 0:
            self.connection.execute('INSERT OR REPLACE INTO lecturas_consumosanos(ts, ejer, energia,idconsumos_id) values(?, ?, ?,?)',
                (primary,ejer,energia,sensor) )
            self.connection.commit()

    # COUNT THE NUMBER OF OBJECTS IN THE DATABASE
    def CountConsumoData(self):
        cnt = 0
        for row in self.connection.execute("SELECT * FROM lecturas_consumos"):
            cnt += 1
        return cnt






