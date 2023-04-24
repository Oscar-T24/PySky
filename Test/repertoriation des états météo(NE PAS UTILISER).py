
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
                open_cv_image = open_cv_image[:, :, ::-1].copy() 
                etat_meteo = prediction(open_cv_image)
                print('prediction pour le departement ',no_departement,' :',etat_meteo)

            except :
                print("probleme avec l'indexation de l'image") 
            
            if no_departement != None :            
                    dico_etats_meteos.append({'Code':no_departement,'etat':etat_meteo})
            #print(dico_etats_meteos)

            # dans certains cas, le departement n'est pas indiqué dans les parentheses

#faire une moyenne des etats par departements :i.e, si on a plusieurs météos différentes dans un département, on pourra prendre la météo qui est majoritaire , si il n'y a pas de majorité on prend au hazard

# JUSTE POUR DEBUGER

'''
dico_etats_meteos = [{'Code': '64', 'etat': 'Foggy'}, {'Code': '11', 'etat': 'Rainy'}, {'Code': '17', 'etat': 'Cloudy'}, {'Code': '54', 'etat': 'Rainy'}, {'Code': '74', 'etat': 'Cloudy'}, {'Code': '34', 'etat': 'Cloudy'}, {'Code': '54', 'etat': 'Cloudy'}, {'Code': '42', 'etat': 'Rainy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '57', 'etat': 'Cloudy'}, {'Code': '33', 'etat': 'Cloudy'}, {'Code': '75', 'etat': 'Cloudy'}, {'Code': '59', 'etat': 'Sunny'}, {'Code': '74', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Rainy'}, {'Code': '41', 'etat': 'Cloudy'}, {'Code': '54', 'etat': 'Cloudy'}, {'Code': '47', 'etat': 'Rainy'}, {'Code': '85', 'etat': 'Cloudy'}, {'Code': '29', 'etat': 'Rainy'}, {'Code': '2', 'etat': 'Cloudy'}, {'Code': '30', 'etat': 'Cloudy'}, {'Code': '50', 'etat': 'Cloudy'}, {'Code': '85', 'etat': 'Cloudy'}, {'Code': '14', 'etat': 'Sunny'}, {'Code': '2', 'etat': 'Cloudy'}, {'Code': '61', 'etat': 'Rainy'}, {'Code': '63', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '05', 'etat': 'Foggy'}, {'Code': '03', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '34', 'etat': 'Sunny'}, {'Code': '69', 'etat': 'Rainy'}, {'Code': '68', 'etat': 'Rainy'}, {'Code': '91', 'etat': 'Cloudy'}, {'Code': '57', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Foggy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '68', 'etat': 'Rainy'}, {'Code': '64', 'etat': 'Sunny'}, {'Code': '73', 'etat': 'Rainy'}, {'Code': '31', 'etat': 'Foggy'}, {'Code': '31', 'etat': 'Foggy'}, {'Code': '57', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '38', 'etat': 'Cloudy'}, {'Code': '17', 'etat': 'Foggy'}, {'Code': '63', 'etat': 'Rainy'}, {'Code': '64', 'etat': 'Rainy'}, {'Code': '63', 'etat': 'Rainy'}, {'Code': '46', 'etat': 'Cloudy'}, {'Code': '59', 'etat': 'Rainy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '42', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Rainy'}, {'Code': '03', 'etat': 'Foggy'}, {'Code': '68', 'etat': 'Cloudy'}, {'Code': '25', 'etat': 'Cloudy'}, {'Code': '44', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Rainy'}, {'Code': '01', 'etat': 'Cloudy'}, {'Code': '42', 'etat': 'Cloudy'}, {'Code': '11', 'etat': 'Cloudy'}, {'Code': '67', 'etat': 'Foggy'}, {'Code': '06', 'etat': 'Rainy'}, {'Code': '74', 'etat': 'Rainy'}, {'Code': '19', 'etat': 'Sunny'}, {'Code': '60', 'etat': 'Sunny'}, {'Code': 
'12', 'etat': 'Rainy'}, {'Code': '67', 'etat': 'Cloudy'}, {'Code': '81', 'etat': 'Rainy'}, {'Code': '90', 'etat': 'Foggy'}, {'Code': '66', 'etat': 'Rainy'}, {'Code': '01', 'etat': 'Cloudy'}, {'Code': '08', 'etat': 'Sunny'}, {'Code': '38', 'etat': 'Rainy'}, {'Code': '31', 'etat': 'Rainy'}, {'Code': '38', 'etat': 'Cloudy'}, {'Code': '63', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Cloudy'}, {'Code': '72', 'etat': 'Sunny'}, {'Code': '06', 'etat': 'Rainy'}, {'Code': '63', 'etat': 'Rainy'}, {'Code': '59', 'etat': 'Foggy'}, {'Code': '84', 'etat': 'Foggy'}, {'Code': '01', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Cloudy'}, {'Code': '17', 'etat': 'Cloudy'}, {'Code': '06', 'etat': 'Cloudy'}, {'Code': '79', 'etat': 'Foggy'}, {'Code': '73', 'etat': 'Rainy'}, {'Code': '73', 'etat': 'Sunny'}, {'Code': '73', 'etat': 'Sunny'}, {'Code': '73', 'etat': 'Foggy'}, {'Code': '73', 'etat': 
'Sunny'}, {'Code': '73', 'etat': 'Sunny'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '66', 'etat': 'Rainy'}, {'Code': '66', 'etat': 'Rainy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '01', 'etat': 'Cloudy'}, {'Code': 
'69', 'etat': 'Rainy'}, {'Code': '76', 'etat': 'Sunny'}, {'Code': '64', 'etat': 'Foggy'}, {'Code': '30', 'etat': 'Rainy'}, {'Code': '11', 'etat': 'Cloudy'}, {'Code': '04', 'etat': 'Foggy'}, {'Code': '69', 'etat': 'Sunny'}, {'Code': '30', 'etat': 'Cloudy'}, {'Code': '69', 'etat': 'Rainy'}, {'Code': '11', 'etat': 'Rainy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '38', 'etat': 'Foggy'}, {'Code': '64', 'etat': 'Sunny'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '64', 'etat': 'Foggy'}, {'Code': '19', 'etat': 'Cloudy'}, {'Code': '09', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Cloudy'}, {'Code': '66', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Foggy'}, {'Code': '82', 'etat': 'Rainy'}, {'Code': '43', 'etat': 'Rainy'}, {'Code': '34', 'etat': 'Cloudy'}, {'Code': '45', 'etat': 'Cloudy'}, {'Code': '53', 'etat': 'Cloudy'}, {'Code': '68', 'etat': 'Rainy'}, {'Code': '69', 'etat': 'Cloudy'}, {'Code': '84', 'etat': 'Rainy'}, {'Code': '48', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Rainy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Sunny'}, {'Code': '64', 'etat': 'Foggy'}, {'Code': '56', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Rainy'}, {'Code': '09', 'etat': 'Rainy'}, {'Code': '88', 'etat': 'Cloudy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '71', 'etat': 'Cloudy'}, {'Code': '16', 'etat': 'Sunny'}, {'Code': '76', 'etat': 'Cloudy'}, {'Code': '57', 'etat': 'Rainy'}, {'Code': '68', 'etat': 'Rainy'}, {'Code': '06', 'etat': 'Rainy'}, {'Code': '69', 'etat': 'Rainy'}, {'Code': '74', 'etat': 'Rainy'}, {'Code': '41', 'etat': 'Rainy'}, {'Code': '17', 'etat': 'Rainy'}, {'Code': '81', 'etat': 'Rainy'}, {'Code': '07', 'etat': 'Rainy'}, {'Code': '43', 'etat': 'Cloudy'}, {'Code': '30', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '05', 'etat': 'Sunny'}, {'Code': '22', 'etat': 'Cloudy'}, {'Code': '87', 'etat': 'Cloudy'}, {'Code': '25', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Rainy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Rainy'}, {'Code': '65', 'etat': 'Cloudy'}, {'Code': '01', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Foggy'}, {'Code': '80', 'etat': 'Cloudy'}, {'Code': '60', 'etat': 'Cloudy'}, {'Code': '17', 'etat': 'Cloudy'}, {'Code': '43', 'etat': 'Cloudy'}, {'Code': '68', 'etat': 'Rainy'}, {'Code': '44', 'etat': 'Rainy'}, {'Code': '85', 'etat': 'Rainy'}, {'Code': '24', 'etat': 'Cloudy'}, {'Code': '73', 'etat': 'Cloudy'}, {'Code': '77', 'etat': 'Cloudy'}, {'Code': '69', 'etat': 'Rainy'}, {'Code': '40', 'etat': 'Cloudy'}, {'Code': '88', 'etat': 'Rainy'}, {'Code': 
'26', 'etat': 'Cloudy'}, {'Code': '85', 'etat': 'Rainy'}, {'Code': '83', 'etat': 'Cloudy'}, {'Code': '39', 'etat': 'Rainy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '91', 'etat': 'Cloudy'}, {'Code': '78', 'etat': 'Cloudy'}, {'Code': '74', 'etat': 'Cloudy'}, {'Code': '38', 'etat': 'Rainy'}, {'Code': '07', 'etat': 'Rainy'}, {'Code': '26', 'etat': 'Rainy'}, {'Code': '65', 'etat': 'Cloudy'}, {'Code': '13', 'etat': 'Cloudy'}, {'Code': '41', 'etat': 'Cloudy'}, {'Code': '28', 'etat': 'Cloudy'}, {'Code': '05', 'etat': 'Rainy'}, {'Code': '25', 'etat': 'Sunny'}, {'Code': '22', 'etat': 'Rainy'}, {'Code': '02', 'etat': 'Cloudy'}, {'Code': '59', 'etat': 'Rainy'}, {'Code': '56', 'etat': 'Cloudy'}, {'Code': '11', 'etat': 'Sunny'}, {'Code': '38', 'etat': 'Cloudy'}, {'Code': '28', 'etat': 'Cloudy'}, {'Code': '34', 'etat': 'Cloudy'}, {'Code': '59', 'etat': 'Cloudy'}, {'Code': '91', 
'etat': 'Sunny'}, {'Code': '16', 'etat': 'Cloudy'}, {'Code': '42', 'etat': 'Rainy'}, {'Code': '69', 'etat': 'Cloudy'}, {'Code': '75', 'etat': 'Cloudy'}, {'Code': '86', 'etat': 'Cloudy'}, {'Code': '17', 'etat': 'Rainy'}, 
{'Code': '06', 'etat': 'Rainy'}, {'Code': '43', 'etat': 'Rainy'}, {'Code': '22', 'etat': 'Rainy'}, {'Code': '65', 'etat': 'Rainy'}, {'Code': '83', 'etat': 'Cloudy'}, {'Code': '88', 'etat': 'Rainy'}]
'''
dico = etats_meteos = sorted(dico_etats_meteos,key=lambda dico_etats_meteos: dico_etats_meteos['Code'])
'''
dico_etats_meteos = [dico_etats_meteos[i] for i in range(1,len(dico_etats_meteos)-1) if dico_etats_meteos[i]['Code'] != dico_etats_meteos[i-1]['Code'] and dico_etats_meteos[i]['Code'] != dico_etats_meteos[i+1]['Code'] ]
print(dico_etats_meteos)
'''
with open('etats_departements.csv','w') as f:
    # creer / actualiser un csv pour létat météo d'un departement
    lect = csv.DictWriter(f,fieldnames=['Code','etat'])
    lect.writeheader()
    lect.writerows(dico_etats_meteos)

# MERGING DES DEUX CSV : TEMPERATURE ET ETAT
# reading two csv files

data1 = pd.read_csv('temperature_data.csv')
data2 = pd.read_csv('etats_departements.csv')
  
# using merge function by setting how='inner'
merged_df = pd.merge(data1, data2, 
                   on='Code', 
                   how='inner')
  
# displaying result
print(merged_df)
merged_df.to_csv('tableau_final.csv', index=False)


# ETAPE SUIVANTE :enlever les doublons

df = pd.read_csv('tableau_final.csv')
grouped = df.groupby('Code')['etat'].value_counts()
new_df = pd.DataFrame({'etat': grouped.groupby(level=0).idxmax().apply(lambda x: x[1])}).reset_index()
temp_df = pd.read_csv('temperature_data.csv')
f_df = pd.merge(temp_df, new_df,  on='Code', how='inner')

f_df.to_csv('tableau_finalv2.csv', index=False)

