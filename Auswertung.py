#Python3
'''
Mit diesem Programm soll es möglich sein die ermittelten Zählerwerte auszuwerten.
'''

import os,sys
import Lib.FileLib as fl
import Lib.Menu as Menu
import matplotlib.pyplot as plt

#Logfile = 'TagesStromverbrauch_23.08.2021.csv'
Version = 'V0.3.0'
Path = './Daten/'

def PlotMesswerte(ListOfDate,Messwerte1,Messwerte2,XLabel,Bezeichnung,Einheit='Wh'):
	
	if len(ListOfDate)==len(Messwerte1): 
		if len(ListOfDate) > 0: plt.bar(ListOfDate,Messwerte1,label='Haupttarif')
	if len(ListOfDate)==len(Messwerte2): 
		if len(ListOfDate) > 0: plt.bar(ListOfDate,Messwerte2,label='Nebentarif', color='orange')
	
	plt.xlabel(XLabel)
    #plt.grid(linestyle='dotted', linewidth=1)
	plt.legend(loc='upper right')
	plt.ylabel(Einheit)
	plt.title('Auswertung: '+Bezeichnung)
	plt.show()

def ReadLogFile(Filename):
    '''
    Mit dieser Funktion werden die Werte eingelesen und aufbereitet.
    '''
    NewInhalt = []

    with open(Filename) as f:
        inhalt = f.readlines()
    
    for Zeile in inhalt:
        Zeile = Zeile.replace('\n','') #entfernt den zusätzlichen zeilen umbruch
        NewInhalt.append(Zeile)
    
    return NewInhalt

def ErweitereMonatsNummer(Monat):
    '''
    diese Funktion erweitert eine Einstellinge Monatsnummer in eine zweistellige String 
    '''
    StringZahl = str(Monat)
    if len(StringZahl)< 2: StringZahl='0'+StringZahl
    return StringZahl

def SplitZeile(Zeile=str):
    '''
    Mit dieser Funktion wird die Zeile in die einzelnen Werte aufgetrennt und als Liste zurückgegben.
    '''
    Werte = []
    Werte = Zeile.split('|')
    return Werte

def GetHourValue(Werte=[]):
    '''
    Diese Funktion Splittet die Werte für die Uhrzeit in 3 Werte auf Stunde, Minuten, Sekunden und 
    gibt den Wert für die Stunde zurück.
    '''
    TimeSplit =[]
    Zeit = Werte[1] #Zeit steht in der zweiten Spalte
    TimeSplit = Zeit.split(':')
    return TimeSplit[0]

def TagesverbrauchGesamt(Daten,Auswertung):
	'''
	Diese Funktion ermittelt den Gesamttagesverbrauch und gibt Ihn als float-Wert zurück. 
	'''
	
	Zählerwerte1 = []
	Zählerwerte2 = []

	if Auswertung == "Strom":

		for Zeile in Daten:
			Werte = SplitZeile(Zeile)
			Zählerwerte1.append(float(Werte[2].replace(',','.')))
		
		getlen = len(Zählerwerte1)-1
		Verbrauch = (Zählerwerte1[getlen]-Zählerwerte1[0])

		return Verbrauch

	elif Auswertung == "Heizung":

		for Zeile in Daten:
			Werte = SplitZeile(Zeile)
			Zählerwerte1.append(float(Werte[2].replace(',','.')))
			Zählerwerte2.append(float(Werte[3].replace(',','.')))
		
		getlen1 = len(Zählerwerte1)-1
		getlen2 = len(Zählerwerte2)-1
		Verbrauch1 = (Zählerwerte1[getlen1]-Zählerwerte1[0])
		Verbrauch2 = (Zählerwerte2[getlen2]-Zählerwerte2[0])
		Verbrauch = Verbrauch1+Verbrauch2

		return Verbrauch

def Monatsverbrauch_Tagesverbrauchsanzeige(Fileliste,Verzeichnis,Auswertung,Monat, Jahr,Anzeige=False):
	'''
	Mit dieser Funktion kann der Verbrauch eines Monats dargestellt werden. Zusätzlich wird auch der Durchschnittliche Tagesverbrauch berechnet und zurückgeben.
	return GesamtMonatsVerbrauch, MonatlicherTagesdurchschnittsverbrauch

	'''
	Monatsliste = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
	GesamtMonatsVerbrauch = 0
	MonatlicherTagesdurchschnittsverbrauch = 0
	Tagensverbrauchsdaten = []
	ListOfDays=[]

	Monat = ErweitereMonatsNummer(Monat)

	if Anzeige: print('Monatsverbrauch für',Auswertung+':',Monatsliste[int(Monat)-1],Jahr)
	if Anzeige: print()

	for Datei in Fileliste:
		SplitFilename = Datei.split('.')
		if SplitFilename[1] == Monat and SplitFilename[2]==Jahr:
			DateiInhalt = ReadLogFile(Verzeichnis+Datei)
			GesamtTagesverbrauch = TagesverbrauchGesamt(DateiInhalt,Auswertung)
			if Anzeige: print('Verbrauch am',Datei[-14:-4]+': ',"%.2f" % GesamtTagesverbrauch,'KWh')
			Tagensverbrauchsdaten.append(GesamtTagesverbrauch)
			ListOfDays.append(Datei[-14:-12])

	GesamtMonatsVerbrauch = sum(Tagensverbrauchsdaten)
	if GesamtMonatsVerbrauch > 0: MonatlicherTagesdurchschnittsverbrauch = GesamtMonatsVerbrauch/len(Tagensverbrauchsdaten) 
    
	if Anzeige: print()
	if Anzeige: print('Monatsverbrauch:',"%.2f" % GesamtMonatsVerbrauch,'KWh')
	if Anzeige: print('Monatlicher Tagesdurschnittsverbrauch:',"%.2f" % MonatlicherTagesdurchschnittsverbrauch,'KWh')

	return GesamtMonatsVerbrauch, MonatlicherTagesdurchschnittsverbrauch,Tagensverbrauchsdaten,ListOfDays

def Stundenverbrauch(Daten,Auswertung,Ausgabe=False):
	'''
	Mit dieser Funktion wird der Tagesverbrauch Stundenweise aufgelistet und es wird eine Liste mit den ermittelten Daten zurückgegeben.
	'''
	ListVerbrauch1 = []
	ListVerbrauch2 = []
	ListStunden = []
	for i in range(0,24): #für die Verbrauchsermittlung jeder Stunde
		Zählerwerte1 = []
		Zählerwerte2 = []
		ListStunden.append(i+1)
		for Zeile in Daten:
			
			Werte = SplitZeile(Zeile)

			if int(GetHourValue(Werte)) == i:
				Zählerwerte1.append(float(Werte[2].replace(',','.'))) #Sammelt die Zählerwerte für den Stundenbereich in einer Liste
				if Auswertung == "Heizung":
					Zählerwerte2.append(float(Werte[3].replace(',','.'))) #Sammelt die Zählerwerte für den Stundenbereich in einer Liste

		getlen1 = len(Zählerwerte1)-1
		getlen2 = len(Zählerwerte2)-1

		if getlen1 >= 0:
			
			Verbrauch1 = (Zählerwerte1[getlen1]-Zählerwerte1[0])*1000 #Berechnet den Verbrauch für die Stunde
			ListVerbrauch1.append(Verbrauch1) #Liste mit Verbrauchswerten für jede Stunde

			if Auswertung == "Heizung": 
				Verbrauch2 = (Zählerwerte2[getlen2]-Zählerwerte2[0])*1000 #Berechnet den Verbrauch für die Stunde
				ListVerbrauch2.append(Verbrauch2)

			if Ausgabe and Auswertung != "Heizung": print ('Verbrauch von',ErweitereMonatsNummer(i),'-',ErweitereMonatsNummer(i+1),'Uhr:',"%.2f" % Verbrauch1,'Wh') 
			else: print ('Verbrauch von',ErweitereMonatsNummer(i),'-',ErweitereMonatsNummer(i+1),'Uhr:',"%.2f" % Verbrauch1,'Wh / ',"%.2f" % Verbrauch2,'Wh')
		else:
			ListVerbrauch1.append(None)
	return ListVerbrauch1,ListVerbrauch2,ListStunden

def Jahresverbrauch(Fileliste,Verzeichnis,Auswertung, Jahr,Anzeige=False):
	'''
	Mit dieser Funktion kann der Verbrauch eines Jahres dargestellt werden. Zusätzlich wird auch der Durchschnittliche Monatsverbrauch berechnet und zurückgeben.
	return GesamtJahresVerbrauch, JährlicherMonatsdurchschnittverbrauch
	'''
	Monatsliste = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
	Monatsverbrauch = []
	ListOfMonth = []
	GesamtJahresVerbrauch = 0
	JährlicherMonatsdurchschnittverbrauch=0

	if Anzeige: print('Jahresverbrauch für',Jahr)
	if Anzeige: print()

	for Monat in range(1,13):
		Verbrauch,DVerbrauch,ListTagesVerbrauch,ListOfDays = Monatsverbrauch_Tagesverbrauchsanzeige(Fileliste,Verzeichnis,Auswertung,Monat,Jahr,False)
		#Monatsverbrauch.append(Verbrauch)
		if Anzeige and Verbrauch > 0: 
			print(Monatsliste[Monat-1]+':',"%.2f" % Verbrauch,'KWh')
			Monatsverbrauch.append(Verbrauch)
			ListOfMonth.append(Monatsliste[Monat-1])
    
	GesamtJahresVerbrauch = sum(Monatsverbrauch)
	if GesamtJahresVerbrauch > 0: JährlicherMonatsdurchschnittverbrauch = GesamtJahresVerbrauch/len(Monatsverbrauch)
	if Anzeige: print()
	if Anzeige: print('Jahresverbrauch:',"%.02f" % GesamtJahresVerbrauch,'KWh')
	if Anzeige: print('Jährlicher Monatsdurchschnittsverbrauch:',"%.2f" % JährlicherMonatsdurchschnittverbrauch,'KWh')

	return GesamtJahresVerbrauch,JährlicherMonatsdurchschnittverbrauch,Monatsverbrauch,ListOfMonth

def DurchschnittlicherJahresverbrauch(Daten,Auswertung):
    VerbrauchAmTag = TagesverbrauchGesamt(Daten,Auswertung)*365
    return VerbrauchAmTag

def main():
	LogFile = ''
	Switch = 'AN'
	SubPath = 'Strom/'
	Auswertung= 'Strom'
	Verzeichnis = Path+SubPath
	anzeigen = True
	while True:
		HauptMenuListe = ['Logfile auswählen','Daten anzeigen','Darstellung Tagesverbrauch An/AUS','Heizung / Strom','Durchschnittlicher-Jahresverbrauch','Monatsverbrauch anzeigen', 'Jahresverbrauch']
		HauptMenu = Menu.Menu('Auswertung Stromzähler-Logfile '+Version+', Logfile: '+LogFile+' Tagesverbrauch: '+Switch+' Auswertung: '+Auswertung) 
		Auswahl = HauptMenu.Display(HauptMenuListe,'Beenden')

		if Auswahl == 1:
			FileListe = fl.ListAllFilesInDiretory(Verzeichnis,'.csv')
			if len(FileListe) > 0:

				FileMenu = Menu.Menu('Welche Logfile soll verwendet werden?')
				FileAuswahl = FileMenu.Display(FileListe,'Zurück')

				if FileAuswahl != len(FileListe)+1:
					LogFile = FileListe[FileAuswahl-1]
				else:    
					print('Zurück')
			else:
				input('keine Logfile gefunden!')
				LogFile = ''

		elif Auswahl ==2:#Stellte den Tagesverbrauch da
			DateiInhalt = ReadLogFile(Verzeichnis+LogFile)
			Messwerte1,Messwerte2,Stunden = Stundenverbrauch(DateiInhalt,Auswertung,anzeigen)
			print('Gesamt Tagesverbrauch:',"%.2f" % TagesverbrauchGesamt(DateiInhalt,Auswertung),'KWh')
			PlotMesswerte(Stunden,Messwerte1,Messwerte2,'Stunde',LogFile)
			input()

		elif Auswahl ==3:#Schaltet die Darstellung des Stundenverbrauchs Aus/Ein
			if anzeigen:
				Switch = 'Aus'
				anzeigen = False            
			else:
				Switch = 'An'
				anzeigen = True

		elif Auswahl == 4:#Umschaltung Auswertung Heizung / Strom
			if Verzeichnis == Path+'Strom/':
				Verzeichnis = Path+'Heizung/'
				Auswertung = 'Heizung'
			else:
				Verzeichnis = Path+'Strom/'
				Auswertung = 'Strom'

		elif Auswahl == 5:#Durchschnittlicher Jähresverbrauch
			DateiInhalt = ReadLogFile(Verzeichnis+LogFile)
			JVerbrauch = DurchschnittlicherJahresverbrauch(DateiInhalt,Auswertung)
			Kosten = JVerbrauch*0.29
			print('Durchschnittlicher Jahresverbrauch ist:',"%.2f" % JVerbrauch,'KWh' )
			print('Kosten:',"%.2f" % Kosten,'€') 
			input()

		elif Auswahl == 6:#Monatsverbrauch
			FileListe = fl.ListAllFilesInDiretory(Verzeichnis,'.csv')
			Monat = input('Monat Eingeben: ')
			Jahr = input('Jahr Eingeben: ')
			os.system('clear')
			GesamtMonatsVerbrauch,MonatlicherTagesdurchschnittsverbrauch,Tagensverbrauchsdaten,ListOfDays = Monatsverbrauch_Tagesverbrauchsanzeige(FileListe,Verzeichnis,Auswertung,Monat,Jahr,anzeigen)
			PlotMesswerte(ListOfDays,Tagensverbrauchsdaten,[],'Tag',Auswertung+' Monat '+Monat+'-'+Jahr,'KWh')
			input()

		elif Auswahl == 7:#Jahresverbrauch
			FileListe = fl.ListAllFilesInDiretory(Verzeichnis,'.csv')
			Jahr = input('Jahr Eingeben: ')
			os.system('clear')
			GesamtJahresVerbrauch,JährlicherMonatsdurchschnittverbrauch,Monatsverbrauch,ListOfMonth = Jahresverbrauch(FileListe,Verzeichnis,Auswertung,Jahr,anzeigen)
			PlotMesswerte(ListOfMonth,Monatsverbrauch,[],'Monat',Auswertung+' '+Jahr,'KWh')
			input()

		elif Auswahl == len(HauptMenuListe)+1:#Programm beenden
			break    
        

main()

