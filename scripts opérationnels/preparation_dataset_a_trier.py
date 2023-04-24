
import csv
from indice import determine_weather_index
from tronque import tronquer
import requests
from PIL import Image
from io import BytesIO
import numpy
import re
import time
import pandas as pd
import json
import cv2

from geopy.geocoders import Nominatim
import re

global dico_etats_meteos


def coordinate_temperature(coordonees):
    """
# Dans cet exemple nous allons utiliser le service météo du Meteorologisk institutt de Norvège
# (api.met.no/weatherapi is an interface to a selection of data produced by MET Norway)
# url: https://api.met.no/weatherapi/locationforecast/2.0/documentation

# Grâce à Google Maps, nous trouvons que les coordonnées de l'IUT à Mont de Marsan sont
# latitude 43.88566272770907, longitude -0.5092243304975015
#
# Ce qui nous donne l'URL suivante pour accéder aux prévisions météo au format JSON:
# https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=43.88566272770907&lon=-0.5092243304975015
# Fetch data from URL
    """
    latitude = coordonees[0]
    longitude = coordonees[1]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
    url = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}7&lon={longitude}", headers=headers)
    text = url.text

    # Get JSON data
    data = json.loads(text)
    #print(data)

    # Process JSON data
    units = data["properties"]["meta"]["units"]
    weather = data["properties"]["timeseries"][0]["data"]["instant"]["details"]  
    return weather

def get_department(commune_name):
    geolocator = Nominatim(user_agent="my-app")
    commune_name = commune_name.encode('ISO 8859-1').decode('utf-8')
    print(commune_name)
    if 'Paris' in commune_name: # on sait pas pk ca marche pas avec Paris (renbvoi 13 mais c Marseille ca)
        return '75'
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

dico_etats_meteos = []

with open('donnees_cameras.csv','r',encoding="ISO-8859-1") as f:
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
            try:
                no_departement = re.findall(r'\d+', ligne['departement'])
            except TypeError:
                print("Except no_departement")
                continue
            if len(no_departement) == 1:
                no_departement = ''.join(no_departement)
            else:
                try : 
                    # si on a pas le~numéo, essayer de geopy le nom de la commune pour trouver
                    no_departement = get_department(ligne['departement'][ligne['departement'].index('de')+2:ligne['departement'].index('(')])
                    print('utilisation reussie de geopy',ligne['departement'][ligne['departement'].index('de')+2:ligne['departement'].index('(')],'numero determiné',no_departement)
                except:
                    # probleme avec Geopy : numero sauté
                    continue
            global indice
            try : 
                # INDICE DE METEO
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                image_tronquee = tronquer(open_cv_image)
                indice = determine_weather_index(open_cv_image)
            except :
                print("probleme avec l'indexation de l'image") 
                indice = 'NULL'
            
            if no_departement != None :   
                    coordonnes = sum([d['coordonnee'].strip('][').split(', ') for d in departements_numeros if d['Code'] == no_departement],[])
                    coordonnes = [float(i) for i in coordonnes]
                    try :
                        meteo = coordinate_temperature(coordonnes)
                        dico_etats_meteos.append({'Code':no_departement,'coordonnees':coordonnes,'indice':indice,'temperature':meteo['air_temperature'],'humidite':meteo['relative_humidity'],'weather':''})
                    except IndexError:
                        print('PROBLEME')
            #print(dico_etats_meteos)

dico_etats_meteos = sorted(dico_etats_meteos,key=lambda dico_etats_meteos: dico_etats_meteos['Code'])

# on comble les departements sans infos avec les temperatures

with open('donnes_a_classifie.csv','w') as f:
    # creer / actualiser un csv pour létat météo d'un departement
    lect = csv.DictWriter(f,fieldnames=['Code','coordonnees','indice','temperature','humidite','weather'])
    lect.writeheader()
    lect.writerows(dico_etats_meteos)
