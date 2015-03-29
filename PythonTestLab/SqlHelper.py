import uuid
import sqlite3
from datetime import datetime
import time

class SqlHelper:

    def __init__(self, dataBaseName):
        '''
        Konstruktor, der Datenbankname muss beim 
        instanzieren uebergeben werden
        '''
        self.dataBaseName = dataBaseName

    def Anzeige(self):
        conn = sqlite3.connect(self.dataBaseName)
        cursor = conn.execute("SELECT * FROM Messwerte;")
        for werte in cursor:
            print(str(werte[0]).rstrip())
            print(str(werte[1]).rstrip())
            print(str(werte[2]).rstrip())
            print(str(werte[3]).rstrip())
            print(str(werte[4]).rstrip())
            print("-----")

    
    def TabellenErstellen(self):
        '''
        Erstellt neue Tabellen falls noch nicht vorhanden
        '''
        conn = sqlite3.connect(self.dataBaseName)
        print("Opened database successfully")
        conn.execute('CREATE TABLE IF NOT EXISTS MESSUNG (MessungPK guid PRIMARY KEY NOT NULL, Messwert real NOT NULL, EinheitFK guid, SensorFK guid, Zeitstempel datetime, LocationFK guid);')
        conn.execute('CREATE TABLE IF NOT EXISTS EINHEIT (EinheitPK guid PRIMARY KEY NOT NULL, EinheitBezeichnung varchar(16) NOT NULL);')
        conn.execute('CREATE TABLE IF NOT EXISTS SENSOR (SensorPK guid PRIMARY KEY NOT NULL, SensorBezeichnung varchar(16) NOT NULL);')
        conn.execute('CREATE TABLE IF NOT EXISTS LOCATION (LocationPK guid PRIMARY KEY NOT NULL, LocationName varchar(16));')
        print("Tabellen erstellt")
        conn.close()

    def NeueLocation(self,LocationName):
        '''
        fuegt der Location-Tabelle neue Orte hinzu
        '''
        conn = sqlite3.connect(self.dataBaseName)
        conn.execute("INSERT INTO LOCATION (LocationPK, LocationName) VALUES ('" + str(uuid.uuid1()) + "','" + str(LocationName) + "');")
        conn.commit()
        conn.close()
        print("Location eingetragen")

    def NeueEinheit(self,EinheitName):
        '''
        fuegt der Location-Tabelle neue Orte hinzu
        '''
        conn = sqlite3.connect(self.dataBaseName)
        conn.execute("INSERT INTO EINHEIT (EinheitPK, EinheitBezeichnung) VALUES ('" + str(uuid.uuid1()) + "','" + str(EinheitName) + "');")
        conn.commit()
        conn.close()
        print("Einheit eingetragen")

    def NeuerSensor(self,SensorName):
        '''
        fuegt der Location-Tabelle neue Orte hinzu
        '''
        conn = sqlite3.connect(self.dataBaseName)
        conn.execute("INSERT INTO SENSOR (SensorPK, SensorBezeichnung) VALUES ('" + str(uuid.uuid1()) + "','" + str(SensorName) + "');")
        conn.commit()
        conn.close()
        print("Sensor eingetragen")

    def WertEintragen(self, Wert, Einheit, Sensor, Location):
        esc = False
        if Einheit is '%':
            Einheit = str("\%")
            esc = True

        timestring = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        conn = sqlite3.connect(self.dataBaseName)

        cursor = conn.execute("SELECT COUNT(*) FROm LOCATION WHERE LocationName LIKE  '" + str(Location) + "';")
        #print(cursor)
        for row in cursor:
            treffer = int(row[0])

        if treffer == 0:
            self.NeueLocation(Location)
            print("Datensatz " + str(Location) + " hinzugefuegt.")


        cursor = conn.execute("SELECT LocationPK  FROM LOCATION WHERE LocationName LIKE '" + str(Location) + "';")
        #print(cursor)

        for row in cursor:
            locationPK = row[0]
            #print(row[0])

        cursor = conn.execute("SELECT COUNT(*) FROM SENSOR WHERE SensorBezeichnung LIKE  '" + str(Sensor) + "';")
        #print(cursor)
        for row in cursor:
            treffer = int(row[0])

        if treffer == 0:
            self.NeuerSensor(Sensor)
            print("Datensatz " + str(Sensor) + " hinzugefuegt.")


        cursor = conn.execute("SELECT SensorPK FROM SENSOR WHERE SensorBezeichnung LIKE '" + str(Sensor) + "';")
        for row in cursor:
            sensorPK = row[0]

        if esc == False:        
            cursor = conn.execute("SELECT COUNT(*) FROM EINHEIT WHERE EinheitBezeichnung LIKE  '" + str(Einheit) + "';")
        else:
            cmd = str("SELECT COUNT(*) FROM EINHEIT WHERE EinheitBezeichnung LIKE  '" + str(Einheit) + "' ESCAPE '\\';")
            #print(cmd)
            cursor = conn.execute(cmd)
        
        for row in cursor:
            treffer = int(row[0])

        if treffer == 0:
            if esc == False:
                self.NeueEinheit(Einheit)
            else:
                self.NeueEinheit('%')
            print("Datensatz " + str(Einheit) + " hinzugefuegt.")

        if esc == False:
            cursor = conn.execute("SELECT EinheitPK FROM EINHEIT WHERE EinheitBezeichnung LIKE '" + str(Einheit) + "';")
        else:
            cursor = conn.execute("SELECT EinheitPK FROM EINHEIT WHERE EinheitBezeichnung LIKE '" + str(Einheit) + "' ESCAPE '\\';")

        for row in cursor:
            einheitPK = row[0]
            
        cmd = "INSERT INTO MESSUNG (MessungPK, Messwert, EinheitFK,SensorFK, Zeitstempel, LocationFK) VALUES ('" + str(uuid.uuid1()) + "','" 
        cmd += str(Wert) + "','" + str(einheitPK) + "','" + str(sensorPK) + "', datetime('"
        cmd += str(timestring) +"'),'" + str(locationPK) + "');"

        conn.execute(cmd)
        conn.commit()
        conn.close()
        #print(str(cmd))
        print("Daten vom " + str(Sensor) + " mit Einheit " + str(Einheit) + " in/im/auf " + str(Location) + " erfolgreich eingetragen")

