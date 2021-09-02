#python 3
'''
dieses ist eine Bibliothek mit der man die Daten vom Sensor für den Stromzähler auslesen kann.
'''
import serial
import os, time
from datetime import datetime

class Sensor:

	def __init__(self, ComPort, bautrate=9600):
		self.SensorDaten = serial.Serial(ComPort,baudrate=bautrate,timeout=1)
		if self.SensorDaten.isOpen()== False: #wenn Schnittstelle nicht offen ist soll sie aufgemacht werden.
			self.SensorDaten.open()
		time.sleep(2)

	def CloseSensor(self):
		self.SensorDaten.close()

	def CheckInitString(self):
		'''
		Mit dieser Funktion wird der InitString der SML Informationen erkannt. Wird dieser erkannt wird ein "True" zurückgegben.

		'''
		InitString = [b'\x1b',b'\x1b',b'\x1b',b'\x1b',b'\x01',b'\x01',b'\x01',b'\x01']
		StartInit = []
		while True:
			while self.SensorDaten.in_waiting > 0:
				Daten = self.SensorDaten.read()
				if Daten in InitString:
					StartInit.append(Daten)
				else:
					StartInit =[]
				if len(StartInit) == 8:
					#print('Init String erkannt.....')
					return True
					

	def ReadDatenFromSensor(self):
		'''
		Mit dieser Funktion werden die Daten des Zählers Byteweise eingelesen und zu einer großen ByteListe zusammen gefasst.
		wird der EndString erkannt, wird die ByteListe zurückgegeben. 
		'''
		EndString = [b'\x1b',b'\x1b',b'\x1b',b'\x1b',b'\x1a']
		EndInit = []
		Datenliste = [b'\x1b',b'\x1b',b'\x1b',b'\x1b',b'\x01',b'\x01',b'\x01',b'\x01'] #Gefundener InitString wird erweitert mit den ausgelesenen Daten
		if self.CheckInitString() == True:
			while self.SensorDaten.in_waiting > 0:
				Daten = self.SensorDaten.read()
				Datenliste.append(Daten)
				if Daten in EndString:
					EndInit.append(Daten)
				else:
					EndInit = []
				if len(EndInit) == 5:
					#print('End String erkannt.....')
					for i in range(0,3): # Die Forschleife soll die letzten 3 Bytes nach dem erkennen des Endstrings mit auslesen da hier die Checksumme der SML-Nachricht enthalten ist
						Datenliste.append(self.SensorDaten.read())
					return Datenliste
	
	def writeToFile(self,Daten,Filename):
		'''
		Mit dieser Funktion soll die empfangene SML-Nachricht in einen Datei gespeichert werden können.
		'''
		Liste = []
		dt = str(datetime.now())# Getting the current date and time
		
		for Entry in Daten: #wandelt die Hexbytes in eine Stringliste um
			Liste.append(Entry.hex().upper())

		File = open(dt+'_'+Filename,'a')
		
		for Daten in Liste:
			File.write(Daten)
		File.close()


	def SplitHexByte(self,HexByte,Check = True):
		'''
		Mit dieser Funktion soll es möglich sein, ein HexByte in seine zwei chars aufzusplitten.
		returns "Char[0],Char[1]" from HexByte
		'''
		ListValue = 0
		HexString = HexByte.hex().upper() #wandelt Hexbyte in String um
		FirstHexChar = int(HexString[0],16)
		LastHexChar = int(HexString[1],16)
		
		if (FirstHexChar != 7) and (Check == True):
			ListValue = 0
			return LastHexChar, ListValue
		else:
			return 1, LastHexChar
		