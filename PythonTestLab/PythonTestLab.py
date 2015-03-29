import uuid
import time
from datetime import datetime
import serial
import SqlHelper
import random

def Connect():
    while True:
        try:
            return serial.Serial('/dev/ttyUSB0', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB1', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB2', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB3', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB4', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB5', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB6', 57600, timeout = 2)
        except:
            print("pong")
        try:
            return serial.Serial('/dev/ttyUSB7', 57600, timeout = 2)
        except:
            print("pong")
            time.sleep(1)
        

SER = Connect()
counter = 6000
data = SqlHelper.SqlHelper('test.db')
data.TabellenErstellen()
data.Anzeige()

while True:
    try:
        messwerte = SER.readlines();
        #SER.flushInput()
        print(messwerte)
        if counter >= 250:
            for inhalt in messwerte:
                if "x" not in inhalt:
                    print(str(inhalt))
                else:

                    # wert einheit sensor ort
                    current = inhalt.split("x");
                    wert = current[0]
                    einheit = str(current[1]).rstrip()
                    sensor = str(current[2]).rstrip()      
                    location = str(current[3]).rstrip()
                    counter = 0
                    data.WertEintragen(wert, einheit, sensor, location)   
        else:
            counter += 1
    except:
        print("Some shit happpens")
        SER = Connect()



