#Python3
'''
Mit diesem Programm soll es möglich sein die ermittelten Zählerwerte auszuwerten.
'''

import os,sys
import Lib.FileLib as fl
import Lib.Menu as Menu

#Logfile = 'TagesStromverbrauch_23.08.2021.csv'
Version = 'V0.1.0'
Path = './Daten/'


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

def TagesverbrauchGesamt(Daten):
    '''
    Diese Funktion ermittelt den Gesamttagesverbrauch und gibt Ihn als float-Wert zurück. 
    '''
    Zählerwerte = []
    
    for Zeile in Daten:
        Werte = SplitZeile(Zeile)
        Zählerwerte.append(float(Werte[2].replace(',','.')))
    
    getlen = len(Zählerwerte)-1
    Verbrauch = (Zählerwerte[getlen]-Zählerwerte[0])

    return Verbrauch

def Monatsverbrauch_Tagesverbrauchsanzeige(Fileliste, Monat, Jahr,Anzeige=False):
    '''
    Mit dieser Funktion kann der Verbrauch eines Monats dargestellt werden. Zusätzlich wird auch der Durchschnittliche Tagesverbrauch berechnet und zurückgeben.
    return GesamtMonatsVerbrauch, MonatlicherTagesdurchschnittsverbrauch

    '''
    Monatsliste = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    GesamtMonatsVerbrauch = 0
    MonatlicherTagesdurchschnittsverbrauch = 0
    Tagensverbrauchsdaten = []

    Monat = ErweitereMonatsNummer(Monat)

    if Anzeige: print('Monatsverbrauch für',Monatsliste[int(Monat)-1],Jahr)
    if Anzeige: print()

    for Datei in Fileliste:
        SplitFilename = Datei.split('.')
        if SplitFilename[1] == Monat and SplitFilename[2]==Jahr:
            DateiInhalt = ReadLogFile(Path+Datei)
            GesamtTagesverbrauch = TagesverbrauchGesamt(DateiInhalt)
            if Anzeige: print('Verbrauch am',Datei[-14:-4]+': ',"%.2f" % GesamtTagesverbrauch,'KWh')
            Tagensverbrauchsdaten.append(GesamtTagesverbrauch)
    
    GesamtMonatsVerbrauch = sum(Tagensverbrauchsdaten)
    if GesamtMonatsVerbrauch > 0: MonatlicherTagesdurchschnittsverbrauch = GesamtMonatsVerbrauch/len(Tagensverbrauchsdaten) 
    
    if Anzeige: print()
    if Anzeige: print('Monatsverbrauch:',"%.2f" % GesamtMonatsVerbrauch,'KWh')
    if Anzeige: print('Monatlicher Tagesdurschnittsverbrauch:',"%.2f" % MonatlicherTagesdurchschnittsverbrauch,'KWh')
    
    return GesamtMonatsVerbrauch, MonatlicherTagesdurchschnittsverbrauch

def Stundenverbrauch(Daten,Ausgabe=False):
    '''
    Mit dieser Funktion wird der Tagesverbrauch Stundenweise aufgelistet und es wird eine Liste mit den ermittelten Daten zurückgegeben.
    '''
    ListVerbrauch = []
    for i in range(0,24): #für die Verbrauchsermittlung jeder Stunde
        Zählerwerte = []
        for Zeile in Daten:

            Werte = SplitZeile(Zeile)
            
            if int(GetHourValue(Werte)) == i:
                Zählerwerte.append(float(Werte[2].replace(',','.'))) #Sammelt die Zählerwerte für den Stundenbereich in einer Liste

        getlen = len(Zählerwerte)-1

        if getlen >= 0:
            Verbrauch = (Zählerwerte[getlen]-Zählerwerte[0])*1000 #Berechnet den Verbrauch für die Stunde
            ListVerbrauch.append(Verbrauch) #Liste mit Verbrauchswerten für jede Stunde
            if Ausgabe: print ('Verbrauch von',i,'-',i+1,'Uhr:',"%.2f" % Verbrauch,'Wh')
        else:
            ListVerbrauch.append(None)
    return ListVerbrauch

def Jahresverbrauch(Fileliste,Jahr,Anzeige=False):
    '''
    Mit dieser Funktion kann der Verbrauch eines Jahres dargestellt werden. Zusätzlich wird auch der Durchschnittliche Monatsverbrauch berechnet und zurückgeben.
    return GesamtJahresVerbrauch, JährlicherMonatsdurchschnittverbrauch
    '''
    Monatsliste = ['Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember']
    Monatsverbrauch = []
    GesamtJahresVerbrauch = 0
    JährlicherMonatsdurchschnittverbrauch=0

    if Anzeige: print('Jahresverbrauch für',Jahr)
    if Anzeige: print()

    for Monat in range(1,13):
        Verbrauch,DVerbrauch = Monatsverbrauch_Tagesverbrauchsanzeige(Fileliste,Monat,Jahr,False)
        Monatsverbrauch.append(Verbrauch)
        if Anzeige and Verbrauch > 0: print(Monatsliste[Monat-1]+':',"%.2f" % Verbrauch,'KWh')
    
    GesamtJahresVerbrauch = sum(Monatsverbrauch)
    if GesamtJahresVerbrauch > 0: JährlicherMonatsdurchschnittverbrauch = GesamtJahresVerbrauch/len(Monatsverbrauch)
    if Anzeige: print()
    if Anzeige: print('Jahresverbrauch:',"%.02f" % GesamtJahresVerbrauch,'KWh')
    if Anzeige: print('Jährlicher Monatsdurchschnittsverbrauch:',"%.2f" % JährlicherMonatsdurchschnittverbrauch,'KWh')

    return GesamtJahresVerbrauch, JährlicherMonatsdurchschnittverbrauch

def DurchschnittlicherJahresverbrauch(Daten):
    VerbrauchAmTag = TagesverbrauchGesamt(Daten)*365
    return VerbrauchAmTag

def main():
    LogFile = ''
    Switch = 'AN'
    anzeigen = True
    while True:
        HauptMenuListe = ['Logfile auswählen','Daten anzeigen','Darstellung Tagesverbrauch An/AUS','Durchschnittlicher-Jahresverbrauch','Monatsverbrauch anzeigen', 'Jahresverbrauch']
        HauptMenu = Menu.Menu('Auswertung Stromzähler-Logfile '+Version+', Logfile: '+LogFile+' Tagesverbrauch: '+Switch) 
        Auswahl = HauptMenu.Display(HauptMenuListe,'Beenden')
        
        if Auswahl == 1:
            FileListe = fl.ListAllFilesInDiretory(Path,'.csv')
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
            DateiInhalt = ReadLogFile(Path+LogFile)
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
            DateiInhalt = ReadLogFile(Path+LogFile)
            JVerbrauch = DurchschnittlicherJahresverbrauch(DateiInhalt)
            Kosten = JVerbrauch*0.29
            print('Durchschnittlicher Jahresverbrauch ist:',"%.2f" % JVerbrauch,'KWh' )
            print('Kosten:',"%.2f" % Kosten,'€') 
            input()

        elif Auswahl == 5:
            FileListe = fl.ListAllFilesInDiretory(Path,'.csv')
            Monat = input('Monat Eingeben: ')
            Jahr = input('Jahr Eingeben: ')
            os.system('clear')
            Monatsverbrauch_Tagesverbrauchsanzeige(FileListe,Monat,Jahr,anzeigen)
            input()

        elif Auswahl == 6:
            FileListe = fl.ListAllFilesInDiretory(Path,'.csv')
            Jahr = input('Jahr Eingeben: ')
            os.system('clear')
            Jahresverbrauch(FileListe,Jahr,anzeigen)
            input()

        elif Auswahl == len(HauptMenuListe)+1:#Programm beenden
            break    
        

main()

