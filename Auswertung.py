#Python3
'''
Mit diesem Programm soll es möglich sein die ermittelten Zählerwerte auszuwerten.
'''

import os,sys
import Lib.FileLib as fl
import Lib.Menu as Menu

#Logfile = 'TagesStromverbrauch_23.08.2021.csv'
Version = '0.0.1'

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

def GetValues(Zeile=str):
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
    Zeit = Werte[1]
    TimeSplit = Zeit.split(':')
    return TimeSplit[0]

def TagesverbrauchGesamt(Daten):
    '''
    Diese Funktion ermittelt den Gesamttagesverbrauch und gibt Ihn als float-Wert zurück. 
    '''
    Zählerwerte = []
    
    for Zeile in Daten:
        Werte = GetValues(Zeile)
        Zählerwerte.append(float(Werte[2].replace(',','.')))
    
    getlen = len(Zählerwerte)-1
    Verbrauch = (Zählerwerte[getlen]-Zählerwerte[0])
    return Verbrauch

def Stundenverbrauch(Daten,Ausgabe=False):
    '''
    Mit dieser Funktion wird der Tagesverbrauch Stundenweise aufgelistet und es wird eine Liste mit den ermittelten Daten zurückgegeben.
    '''
    ListVerbrauch = []
    for i in range(0,24):
        Zählerwerte = []
        for Zeile in Daten:
            
            if int(GetHourValue(GetValues(Zeile))) == i:
                Werte = GetValues(Zeile)
                Zählerwerte.append(float(Werte[2].replace(',','.')))

        getlen = len(Zählerwerte)-1

        if getlen >= 0:
            Verbrauch = (Zählerwerte[getlen]-Zählerwerte[0])*1000
            ListVerbrauch.append(Verbrauch)
            if Ausgabe:
                print ('Verbrauch von',i,'-',i+1,'Uhr:',"%.2f" % Verbrauch,'Wh')
        else:
            ListVerbrauch.append(None)
    return ListVerbrauch

def Jahresverbrauch(Daten):
    VerbrauchAmTag = TagesverbrauchGesamt(Daten)*365
    return VerbrauchAmTag


def main():
    LogFile = ''
    Switch = 'AN'
    anzeigen = True
    while True:
        HauptMenuListe = ['Logfile auswählen','Daten anzeigen','Darstellung Tagesverbrauch An/AUS','Durchschnittlicher-Jahresverbrauch']
        HauptMenu = Menu.Menu('Auswertung Stromzähler-Logfile '+Version+', Logfile: '+LogFile+' Tagesverbrauch: '+Switch) 
        Auswahl = HauptMenu.Display(HauptMenuListe,'Beenden')
        
        if Auswahl == 1:
            FileListe = fl.ListAllFilesInDiretory('.csv')
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
            DateiInhalt = ReadLogFile(LogFile)
            Stundenverbrauch(DateiInhalt,anzeigen)
            print('Gesamt Tagesverbrauch:',"%.2f" % TagesverbrauchGesamt(DateiInhalt),'KWh')
            input()

        elif Auswahl ==3:#Schaltet die Darstellung des Stundenverbrauchs Aus/Ein
            if anzeigen:
                Switch = 'Aus'
                anzeigen = False            
            else:
                Switch = 'An'
                anzeigen = True

        elif Auswahl ==4:
            DateiInhalt = ReadLogFile(LogFile)
            JVerbrauch = Jahresverbrauch(DateiInhalt)
            Kosten = JVerbrauch*0.29
            print('Durchschnittlicher Jahresverbrauch ist:',"%.2f" % JVerbrauch,'KWh' )
            print('Kosten:',"%.2f" % Kosten,'€') 
            input()

        elif Auswahl == len(HauptMenuListe)+1:#Programm beenden
            break    
        

main()

