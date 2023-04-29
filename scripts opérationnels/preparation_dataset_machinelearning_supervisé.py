import tkinter as tk
import subprocess
from PIL import ImageTk as itk
from random import choice
import requests
import numpy
from io import BytesIO
from tkinter import ttk
from PIL import Image
import cv2
import csv


def display_image(image):
    '''
    générer une fenetre tkinter pour interfacer le choix de l'utilisateur
    '''

    root = tk.Tk()

    try :
        blue, green, red = cv2.split(image)
    except ValueError: # en cas de problmeme d'image
        return
    image = cv2.merge((red, green, blue))
    image = Image.fromarray(image)
    from PIL import ImageTk as itk
    img = itk.PhotoImage(image)
    canvas = tk.Canvas(root, width=500, height=500)  # tk.Canvas(root, width=img.width(), height=img.height())
    canvas.create_image(0, 0, anchor='nw', image=img)
    canvas.pack()

    weather_label = ttk.Label(root, text='Select Weather:')
    weather_label.pack(pady=10)
    weather_var = tk.StringVar(root)
    weather_dropdown = ttk.Combobox(root, textvariable=weather_var, values=['Sunny', 'Rainy', 'Cloudy', 'Foggy', 'Night'])
    weather_dropdown.pack()

    save_button = ttk.Button(root, text='Sauvegarder', command=lambda: [ajouter(weather_var.get()), root.destroy()])
    save_button.pack(pady=20)

    quitter = ttk.Button(root, text='Arreter', command=lambda:[ajouter('ARRETER'), root.destroy()])
    quitter.pack(pady=20)

    root.mainloop()

def ajouter(etat):
    f = open('temp_meteo.txt', 'w')
    f.write(etat)
    print('Ecriture de', etat)
    f.close()




# FIN DU MPENU TKINTER --------------------------------------------------------------------------------------------------------------------

#subprocess.run(["python3", "preparation_dataset_a_trier.py"])

f = open('donnees_meteo.csv', 'r')
data = list(csv.DictReader(f))

f = open("donnees_camerasv2.csv", "r")
cameras = list(csv.DictReader(f))

f = open("donnees_meteo_classifiees.csv", "a")
ecr = csv.DictWriter(f, delimiter=",", fieldnames=["code","Date","Temperature (°C)","Humidite_relative (%)","Temperature_ressentie (°C)","Probabilite_pluie (%)","Precipitation (mm)","Pression (0m)(hPa)","Couverture_nuageuse (%)","Visibility (m)","Vitesse_vent (km/h)","Index_UV","Air_quality (pm2.5)","River_discharge (m3/s)","Probabilité sècheresse","Probabilité canicule (%)","Probabilité innondation","Indice","Etat_meteo"])

def eval_photo():
    '''
    ajoute (append) une nouvelle ligne au fichier donnes_meteo_classifiees.csv à partir d'une image de webcam tirée au hazard depuis donnees_camerasv2.csv
    '''
    ligne = choice(cameras)
    url = ligne["lien"]
    dep = ligne["departement"]
    try:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
    except:
        print('erreur lors du decodage de l"image')
        return
    global open_cv_image
    open_cv_image = numpy.array(img) # Image bon format?
    display_image(open_cv_image)


    f = open("temp_meteo.txt", "r+")
    utilisateur = f.read() # recup
    f.write("")

    if utilisateur == 'ARRETER':
        return 'stop'
    elif utilisateur is None:
        return
    
    try:
        meteo_dep = [e for e in data if e["code"] == dep][0]
    except:
        raise ValueError("le fichier donnees_meteo.csv est incomplet car le departement associé n'a pas pu etre trouve")
    meteo_dep["Etat_meteo"] = utilisateur
    ecr.writerow(meteo_dep)

while True:
    match eval_photo():
        case None:
            pass
        case 'stop':
            break

f.close()
