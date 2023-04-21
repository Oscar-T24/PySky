import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import csv
import requests
from PIL import Image
from io import BytesIO
import numpy
import re
import pandas as pd
import json
import cv2
import time


from indice import determine_weather_index #argument : image cv2
from tronque import tronquer # argument : chemin d'acces photo

# Function to display image and dropdown menu for weather selection
def display_image(image):
    # Create tkinter window
    root = tk.Tk()

    # Open file dialog and select image file

    # Load image and display in window
    blue,green,red = cv2.split(image)
    image = cv2.merge((red,green,blue))
    image = Image.fromarray(image)
    from PIL import ImageTk as itk
    img = itk.PhotoImage(image)
    canvas = tk.Canvas(root, width=500, height=500) #tk.Canvas(root, width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()

    # Create dropdown menu for weather selection
    weather_label = ttk.Label(root, text='Select Weather:')
    weather_label.pack(pady=10)
    weather_var = tk.StringVar(root)
    weather_dropdown = ttk.Combobox(root, textvariable=weather_var, values=['Sunny', 'Rainy', 'Cloudy', 'Foggy', 'Night'])
    weather_dropdown.pack()

    # Create button to save weather and close window
    save_button = ttk.Button(root, text='Save Weather', command=lambda:[ajouter(weather_var.get()),root.destroy()])
    save_button.pack(pady=20)
    my_button2= ttk.Button(root, text= "arreter", command=lambda:[quitter(),root.destroy()])
    my_button2.pack(pady=20)

    root.mainloop()

arreter = False

def ajouter(etat):
    f = open('temp_meteo.txt','w')
    f.write(etat)
    print('ecriture de',etat)
    f.close()

def quitter():
    global arreter
    arreter = True

# PARTIE 2 -------------------------------------

def coordinate_temperature(coordonees):

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

dico_etats_meteos = []
if __name__ == "__main__":
    try: 
        with open('donnees_cameras.csv','r',encoding="ISO-8859-1") as f:
            read = csv.DictReader(f,fieldnames=['lien','departement'])
            # DETERMINATION DE L'ÉTAT MÉTÉO
            for ligne in read: 
                if ligne['departement'] != 'NULL' and 'webcam_error.png' not in ligne['lien'] and ligne['lien'] != 'lien':
                    url = ligne['lien'] 
                    if True:
                    #try: 
                        response = requests.get(url)
                        img = Image.open(BytesIO(response.content))
                        #img.save("webcam_image.jpg", "JPEG") 
                        open_cv_image = numpy.array(img) 
                        # Convert RGB to BGR 
                    #except:
                    if True == False:
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
                    global indice
                    global etat_meteo
                    #try : 
                        # PARTIE DETERMINATION
                    open_cv_image = open_cv_image[:, :, ::-1].copy() 
                    image_tronquee = tronquer(open_cv_image)
                    indice = determine_weather_index(open_cv_image)
                    display_image(open_cv_image)
                    with open('temp_meteo.txt','r') as f:
                            etat_meteo = f.read()
                    with open('temp_meteo.txt','w') as f:
                        f.write('')
                    #except :
                        #print("probleme avec l'indexation de l'image") 
                        #indice = 'NULL'
                    
                    if no_departement != None :   
                            coordonnes = sum([d['coordonnee'].strip('][').split(', ') for d in departements_numeros if d['Code'] == no_departement],[])
                            coordonnes = [float(i) for i in coordonnes]
                            try :
                                meteo = coordinate_temperature(coordonnes)
                                dico_etats_meteos.append({'Code':no_departement,'coordonnees':coordonnes,'indice':indice,'temperature':meteo['air_temperature'],'humidite':meteo['relative_humidity'],'weather':etat_meteo})
                            except IndexError:
                                print('PROBLEME')
                    if arreter == True:
                        assert True == False
                    #print(dico_etats_meteos)

    except AssertionError:
        print('FINALISATION DES DONNÉES ENTRÉES')
        dico_etats_meteos = sorted(dico_etats_meteos,key=lambda dico_etats_meteos: dico_etats_meteos['Code'])
        with open('donnes_classifiees.csv','a') as f:
            
            # creer / actualiser un csv pour létat météo d'un departement
            lect = csv.DictWriter(f,fieldnames=['Code','coordonnees','indice','temperature','humidite','weather'])
            #lect.writeheader() juste pour la première fois
            lect.writerows(dico_etats_meteos)