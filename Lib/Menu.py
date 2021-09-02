#Python 3
'''
Dieses ist eine Lib mit der es möglich sein soll ein Menu für das Terminal zu erstellen. 
'''

import os,sys
from colorama import *

class Menu(object):

    def __init__(self, WelcomeTitle='Willkommen im Hauptmenu'):
        self.titel = WelcomeTitle

    def ClearScreen(self):
        '''
        Mit dieser Funktion wird der Bildschirm gesäubert
        '''
        self.Plattform = sys.platform.lower()
        if self.Plattform =='linux':
            os.system('clear')
        elif self.Plattform == 'windows':
            os.system('cls')
        elif self.Plattform == 'win32':
            os.system('cls')
        return self.Plattform

    def Display(self, ListOfMenuSteps,LastMenuStep):
        while True:
            self.ClearScreen()
            Counter = 1
            print(self.titel)
            print()
            #print(Style.RESET_ALL)
            for Entry in ListOfMenuSteps:
                print(str(Counter)+'.',Entry)
                Counter +=1
            print(str(Counter)+'.',LastMenuStep)
            print()
            Menupoint = input('Menupunkt auswählen: ')
            try:
                IntMenuPoint = int(Menupoint)
                if (IntMenuPoint <= len(ListOfMenuSteps)+1) and (IntMenuPoint > 0):
                    return IntMenuPoint
                else:
                    input('Falsche Eingabe')
                    #print(Style.RESET_ALL)
                    continue
            except:
                input('Falsche Eingabe')
                #print(Style.RESET_ALL)
                continue



