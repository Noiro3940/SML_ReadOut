#python3 
'''
Dieses Programm dient dazu Zählerstande über eine Infrarot-Schnittstelle von einem Smart Message Language — Stromzähler auslesen.
Über die Schnittstelle wird der Datenstrom alle 57 sek. eingelesen und anschließend werden die Daten analysiert und bestimmte Bereiche aus dem Datenstrom 
ausgelesen.

Die ausgelesenen Daten werden, werden anschließend mit Timestamps aufbereitet und in eine CSV-Datei zur weiteren einfachen analyse abgespeichert. 
'''

import time, datetime
import os
import Lib.Sensor as SML



def ReadSensor():
	global USBSensor
	USBSensor = SML.Sensor('/dev/ttyUSB1',9600)
	Daten = USBSensor.ReadDatenFromSensor()
	return Daten

def SML_Parser(SMLDaten,Filename):
	
	ObisList = [[b'\x07',b'\x01',b'\x00',b'\x01',b'\x08',b'\x01',b'\xFF'],#'OBIS Kennzahl für Zählerstand Wirkenergie Bezug Tarif1',
                [b'\x07',b'\x01',b'\x00',b'\x01',b'\x08',b'\x02',b'\xFF'],#Obis Kennzahl für NachtTarif Zähler
			   [b'\x07',b'\x01',b'\x00',b'\x60',b'\x01',b'\x00',b'\xFF'],#'Obis Kennzahl für Gerätenummer = ServerID',
			   [b'\x07',b'\x01',b'\x00',b'\x60',b'\x32',b'\x01',b'\x01'],#'Obis Kennung für den Hersteller',
			   [b'\x07',b'\x01',b'\x00',b'\x02',b'\x08',b'\x00',b'\xFF']#'OBIS-Kennzahl für Zählerstand Wirkenergie Bezug Tarif2'
	]

	ObisDic = {1:'Zählerstand Wirkenergie Bezug Tarif1',
                2:'Zählerstand Wirkenergie Bezug Tarif2',
				3:'Gerätenummer = ServerID',
				4:'Hersteller-Bezeichnung',
				5:'Zählerstand Wirkenergie Bezug Tarif2'
	}

	ObisEntry = 0
	Zählerstände = []

	for Entry in ObisList:
		ObisEntry += 1 
		if ObisEntry == 1:
			Zählerstand1 = Get_OBIS_Informationen(Entry,SmlDaten).split()
			Zählerwert1 = int(''.join(Zählerstand1)[2:],16)/10000
			Zählerstand = str(Zählerwert1).split('.')
			Zählerstände.append(Zählerstand[0]+','+Zählerstand[1])
		if  ObisEntry == 2:
			Zählerstand1 = Get_OBIS_Informationen(Entry,SmlDaten).split()
			Zählerwert1 = int(''.join(Zählerstand1)[2:],16)/10000
			Zählerstand = str(Zählerwert1).split('.')
			Zählerstände.append(Zählerstand[0]+','+Zählerstand[1])
	#print(Zählerstände[0],Zählerstände[1])
	SaveData(Filename,Zählerstände[0],Zählerstände[1])
			
def Get_OBIS_Informationen(ObisList,SMLDaten):
	'''
	Diese Funktion gibt die ermittelten Hauptdaten für die Übergebene OBIS Kennung zurück.
	'''
	ViewAreaData = False
	AreaData = ''
	ColCounter = 0
	RowCounter = 0
	ListValue = 0
	FindEntry = []

	for SMLEntry in SMLDaten:
		
		if (SMLEntry in ObisList) and (ViewAreaData == False):
				FindEntry.append(SMLEntry)
		else:
			FindEntry = []
		
		if (ViewAreaData == True) and (SMLEntry != b'\x77'):
			if (ColCounter == 0):
				if RowCounter == 5:#in allen bereichen befindet sich der benötigt wert in der 5 Reihe (eigentlich 6 ;o)   )
					return AreaData
				ColCounter, ListValue = USBSensor.SplitHexByte(SMLEntry,True)
				AreaData = ''
				RowCounter = RowCounter-ListValue+1 #wenn ein Listeneintrag gefunden wurde wird die Anzahl der Listen einträger abgezogen.

			AreaData += SMLEntry.hex().upper()+' '
			ColCounter -= 1
			
		if (len(FindEntry) == 7) and (FindEntry == ObisList):#wenn obisList Eintrag gefunden wurde soll daten angezeigt werden.
			ViewAreaData = True
			
		if RowCounter == 6: #Abbruchkriterium für Anzeige der Daten informationen
			ViewAreaData = False

def GetTimeDateStringForLog():
	'''
	Liefert einen Datum_Zeit String zurück (Datum_Zeit)
	'''
	x = datetime.datetime.now()

	Monat = TwoCharsForTimeAndDate(x.month)
	Tag = TwoCharsForTimeAndDate(x.day)
	Stunde = TwoCharsForTimeAndDate(x.hour)
	Min = TwoCharsForTimeAndDate(x.minute)
	Sek = TwoCharsForTimeAndDate(x.second)

	Datum = Tag+'.'+Monat+'.'+str(x.year)
	Zeit = Stunde+':'+Min+':'+Sek
	return Datum,Zeit

def TwoCharsForTimeAndDate(DateTimeWert):
	'''
	Diese Funktion soll einen 2 Stelligen Wert für Zeit und Datum zurück.
	'''
	Wert = str(DateTimeWert)

	if len(Wert) == 1:
		return '0'+Wert
	else:
		return Wert

def SaveData(Filename,Zählerstand1,Zählerstand2):
	'''
	Mit dieser Funktion werden die Daten in eine csv Datei gespeichert
	'''
	
	Datum, Zeit = GetTimeDateStringForLog()
	
	if TimeChange:#wenn ein neuer Tag anfängt soll auch eine neue Logfile erzeugt werden.
		Filename = 'HeizungStromverbrauch_'+Datum+'.csv'
	else:
		Filename = Filename

	Logfile = open(Filename,'a')
	Logfile.write(Datum+'|'+Zeit+'|'+Zählerstand1+'|'+Zählerstand2+'\n')
	Logfile.close()	

def TimeChange():
	global StartZeit

	x = datetime.datetime.now()
	if StartZeit != x.day:
		StartZeit = x.day
		return True
	else:
		return False

LogDay = 'HeizungStromverbrauch_'
StartZeit = ''

while True:
	try:
		SmlDaten = ReadSensor()
		SML_Parser(SmlDaten,LogDay)
		time.sleep(57)
	except:
		continue