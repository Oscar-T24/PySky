
import csv
from prediction import prediction 
import requests
from PIL import Image
from io import BytesIO
import numpy
import re
import time
import pandas as pd

from geopy.geocoders import Nominatim
import re

def get_department(commune_name):
    geolocator = Nominatim(user_agent="my-app")
    location = geolocator.geocode(commune_name + ", France")
    if location:
        return "".join(re.findall(r'-?\d+',location.raw['display_name']))[:2]
    else:
        return None

read = []

global departements_numeros
departements_numeros = []

with open('coordonnees_departements.csv','r') as f:
    lect = csv.DictReader(f,delimiter=',')
    try:
        for row in lect:
            departements_numeros.append(row)
    except:
        pass

global dico_etats_meteos
dico_etats_meteos = []

with open('donnees_cameras.csv','r') as f:
    read = csv.DictReader(f,fieldnames=['lien','departement'])
    # DETERMINATION DE L'ÉTAT MÉTÉO
    for ligne in read: 
        if ligne['departement'] != 'NULL' and 'webcam_error.png' not in ligne['lien']:
            url = ligne['lien']
            try: 
                response = requests.get(url)
                img = Image.open(BytesIO(response.content))
                #img.save("webcam_image.jpg", "JPEG") 
                open_cv_image = numpy.array(img) 
                # Convert RGB to BGR 
            except:
                print("probleme de recuperation d'image")
                continue # on skip l'iteration actuelle
            no_departement = re.findall(r'\d+', ligne['departement'])
            if len(no_departement) == 1:
                no_departement = ''.join(no_departement)
            else:
                try : 
                    # si on a pas le~numéo, essayer de geopy le nom de la commune pour trouver
                    no_departement = get_department(ligne['departement'][ligne['departement'].index('de'):ligne['departement'].index('(')])
                    print('utilisation reussie de geopy',ligne['departement'][ligne['departement'].index('de'):ligne['departement'].index('(')],'numero determiné',no_departement)
                except:
                    # probleme avec Geopy : numero sauté
                    continue
            try : 
                # INDICE DE METEO
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                etat_meteo = 'Lol'

            except :
                print("probleme avec l'indexation de l'image") 
            
            if no_departement != None :   
                    coordonnes = [d['coordonnee'] for d in departements_numeros if d['Code'] == no_departement]      
                    dico_etats_meteos.append({'coordonnees':coordonnes,'temperatures':5})
                    print(coordonnes)
            #print(dico_etats_meteos)

dico = etats_meteos = sorted(dico_etats_meteos,key=lambda dico_etats_meteos: dico_etats_meteos['Code'])
'''
dico_etats_meteos = [dico_etats_meteos[i] for i in range(1,len(dico_etats_meteos)-1) if dico_etats_meteos[i]['Code'] != dico_etats_meteos[i-1]['Code'] and dico_etats_meteos[i]['Code'] != dico_etats_meteos[i+1]['Code'] ]
print(dico_etats_meteos)
'''
assert True == False

with open('clean_donnees_cameras.csv','w') as f:
    # creer / actualiser un csv pour létat météo d'un departement
    lect = csv.DictWriter(f,fieldnames=['Code','longitude','latitude','temperature','humidite'])
    lect.writeheader()
    lect.writerows(dico_etats_meteos)