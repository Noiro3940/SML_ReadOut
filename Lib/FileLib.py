#Python 3
'''
die FileLib soll eine paar funktionen bereitstellen, damit der Umgang mit Dateien einfacher wird.
'''
import zipfile #https://docs.python.org/3/library/zipfile.html
import tarfile
import os


def ReadFile(Filename):
    '''
    Mit dieser Funktion wird der Inhalt einer Datei ausgelesen und zurückgegeben.
    '''
    F = open(Filename,"r")
    return F.read()

def Write2File(Filename,Daten):
    '''
    Mit dieser Funktion wird eine DatenString in eine NeueZeile einer Datei geschrieben.
    '''
    F = open(Filename,"a")
    F.write(Daten+'\n')

def ListAllFilesInDiretory(SearchString):
    '''
    Mit dieser Funktion wird eine Liste zurückgegeben mit den gefundenen Files.
    Der SearchString schaut auf den kompletten FileName.
    '''
    FileListe = []
    for FilesInOrdner in os.listdir('.'):
        i = FilesInOrdner.find(SearchString)
        if i >=0:
            FileListe.append(FilesInOrdner)
    return FileListe

def UnzipProblemReport(PrFilename):
    '''
    Mit dieser Funktion kann der Problemreport ausgepackt werden.
    '''
    try:
        # create a ZipFile object by opening file
        zip_obj= zipfile.ZipFile(PrFilename,"r")
        zip_obj.setpassword(b'24Xg9hWvuG')#Passwort zum unzippen des Problemreports
        #extract all files 
        zip_obj.extractall(PrFilename+'~') 
        #close the zip file
        zip_obj.close()
    except:
        input('Konnte Datei '+PrFilename+' nicht finden!, weiter mit Enter!')

def UnzipSingleFileFromProblemReport(PrFilename,FileInside):
    '''
    Mit dieser Funktion kann der Problemreport ausgepackt werden.
    '''
    try:
        # create a ZipFile object by opening file
        zip_obj= zipfile.ZipFile(PrFilename,"r")
        zip_obj.setpassword(b'24Xg9hWvuG')#Passwort zum unzippen des Problemreports
        #extract all files 
        zip_obj.extract(FileInside) 
        #close the zip file
        zip_obj.close()
    except:
        input('Konnte '+PrFilename+' nicht finden. Weiter mit Enter!')

def UnzipAllFilesFromFileWithoutPassword(Filename):
    '''
    Mit dieser Funktion kann eine Zip-Datei ausgepackt werden.
    '''
    # create a ZipFile object by opening file
    zip_obj= zipfile.ZipFile(Filename,"r")
    #extract all files 
    zip_obj.extractall(Filename+'~') 
    #close the zip file
    zip_obj.close()

def UnzipTarFile(Filename):
    '''
    Mit dieser Funktion kann eine Tar-Datei ausgepackt werden.
    '''
    try:
        # create a ZipFile object by opening file
        Tar_obj= tarfile.open(Filename,"r")
        #extract all files 
        Tar_obj.extractall(Filename+'~')
        #close the zip file
        Tar_obj.close()
    except:
        input('Konnte '+Filename+' nicht finden! Weiter mit Enter!')