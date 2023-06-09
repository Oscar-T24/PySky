from indice import determine_weather_index
from tronque import tronquer
import requests
from PIL import Image
from io import BytesIO
import numpy
from datetime import datetime, timedelta
import csv
from math import sqrt
import pandas as pd
import argparse


# on recupere le nombre de jours différés, 0 par défaut pour aujourdh'ui
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print the value of a command line argument')
    parser.add_argument('-value', help='the value to be printed')
    args = parser.parse_args()
    variable = args.value
    if variable is None:
        variable = 0
    else:
        variable = int(variable)
today = datetime.now()
dif = timedelta(days=variable)
date = today + dif
dateiso = date.isoformat()[:10]

# PRISE DES DEPARTEMENTS, DE LEURS CODES ET DE LEURS COORDONNÉES
f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

# CREATION D'UN TABLEAU
headers = ['code']
df = pd.DataFrame(columns=headers)


# CREATION DE TABLES VIDES POUR CHAQUE COLONNE
temperature = []
humidite_relative = []
temperature_ressentie = []
probabilite_pluie = []
precipitation = []
pression_niveaumer = []
couverture_nuageuse = []
visibility = []
vitesse_vent = []
index_uv = []
air_quality = []
river_discharge = []

# ON REMPLIT LES COLONNES
for e in coordonnees:
    c = e['coordonnee'].split(" ")
    d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])

    # Données de qualité de l'air
    data = pd.read_json(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={x}&longitude={y}&hourly=pm2_5&start_date={dateiso}&end_date={dateiso}")
    quality = data.values.tolist()[1][-1][today.hour]
    air_quality.append(quality)

    data = pd.read_json(f"https://api.open-meteo.com/v1/forecast?latitude={x}&longitude={y}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,pressure_msl,cloudcover,visibility,windspeed_10m,uv_index&forecast_days=1&start_date={dateiso}&end_date={dateiso}")
    temperature.append(data.values.tolist()[1][-1][today.hour])
    humidite_relative.append(data.values.tolist()[2][-1][today.hour])
    temperature_ressentie.append(data.values.tolist()[3][-1][today.hour])
    probabilite_pluie.append(data.values.tolist()[4][-1][today.hour])
    precipitation.append(data.values.tolist()[5][-1][today.hour])
    pression_niveaumer.append(data.values.tolist()[6][-1][today.hour])
    couverture_nuageuse.append(data.values.tolist()[7][-1][today.hour])
    visibility.append(data.values.tolist()[8][-1][today.hour])
    vitesse_vent.append(data.values.tolist()[9][-1][today.hour])
    index_uv.append(data.values.tolist()[10][-1][today.hour])

    # Débit moyen des rivières
    data = pd.read_json(f"https://flood-api.open-meteo.com/v1/flood?latitude={x}&longitude={y}&daily=river_discharge_mean&start_date={dateiso}&end_date={dateiso}&forecast_days=1")
    debit = data.values.tolist()[1][-1][0]
    river_discharge.append(debit)

    print(f"Données météo du {dateiso} extraites pour le département {d} (sur 101)")

liste_departements = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                          '17', '18', '19', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '30', '31',
                          '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47',
                          '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63',
                          '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
                          '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95',
                          '971', '972', '973', '974', '976']

if variable == 0:  
    # Si la requête est pour aujourd'hui
    # ON CREE UNE COLONNE POUR L'INDICE DE METEO DETERMINE A PARTIR DES WEBCAMS, ON LA PASSE ENSUITE PAR KNN POUR OBTENIR UNE CLASSE
    indices_meteo = {}

    print("Debut de l'analyse qualitative des images")

    with open('donnees_camerasv2.csv', 'r') as f:
        read = csv.DictReader(f, fieldnames=['lien', 'departement'])
        # determination de l'indice
        erreurs = 0
        succes = 0
        for ligne in read:
            try:
                response = requests.get(ligne["lien"])
                img = Image.open(BytesIO(response.content))
                open_cv_image = numpy.array(img)
                # Convert RGB to BGR
            except:
                print("Problème avec l'ouverture de l'image")
                erreurs += 1
                continue
            no_departement = ligne['departement']
            try:
                open_cv_image = open_cv_image[:, :, ::-1].copy()
                image_tronquee = tronquer(open_cv_image)
            except:
                print("Image trop sombre, problème avec le tronquage")
                erreurs += 1
                continue
            succes += 1
            indices_meteo[no_departement] = determine_weather_index(image_tronquee) # Ne prend que la dernière camera analysée par departement

    print(f"Analyse des images finie ; indexes extraits: {erreurs} erreurs pour {succes} succès. Taux de réussite de {(succes-erreurs)*100/(succes+erreurs)}%")


    # ON TRIE LES INDICES DANS L'ORDRE DES LIGNES
    for i in liste_departements:
        if i not in indices_meteo.keys():
            indices_meteo[i] = "NULL"

    indices_meteov2 = [indices_meteo[liste_departements[i]] for i in range(len(liste_departements))]

    print("Indices triés")

# DETERMINATION DES EVENEMENTS CLIMATIQUES EXTREMES A PARTIR DES DONNEES OBTENUES

mois = str(datetime.now().month)

f = open('normale_precipitation.csv', 'r')
normale = list(csv.DictReader(f, delimiter=','))

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

# Determination de secheresse  selon la page 13 du "Manuel des indicateurs et indices de sécheresse" de l'organisation meteorologique mondiale (OMM)

index_secheresse = [precipitation[i] / float(normale[i][mois]) * 100 for i in range(len(normale))]

print("Determination du risque de secheresse effectué")

# Determination de cannicule selon les seuils departementaux de jour détérminés dans "Système d’alerte canicule et santé : principes, fondements et évaluation" de l'Institut de Veille Sanitaire

seuils = [(1, 35), (2, 33), (3, 34), (4, 36), (5, 34), (6, 31), (7, 35), (8, 33), (9, 34), (10, 35), (11, 35), (12, 36),
          (13, 35), (14, 31), (15, 32), (16, 36), (17, 35), (18, 35), (19, 36), (21, 34), (22, 31), (23, 34),
          (24, 36), (25, 33), (26, 36), (27, 34), (28, 34), (29, 32), ('2A', 33), ('2B', 33), (30, 36), (31, 36),
          (32, 36), (33, 35), (34, 35), (35, 34), (36, 35), (37, 35), (38, 34), (39, 34), (40, 35), (41, 35), (42, 35),
          (43, 32), (44, 34), (45, 34), (46, 36), (47, 36), (48, 33), (49, 34), (50, 31), (51, 34), (52, 34), (53, 34),
          (54, 34), (55, 34), (56, 32), (57, 34), (58, 34), (59, 33), (60, 34), (61, 34), (62, 33), (63, 34), (64, 34),
          (65, 34), (66, 35), (67, 34), (68, 35), (69, 34), (70, 34), (71, 34), (72, 35), (73, 34), (74, 34), (75, 31),
          (76, 33), (77, 34), (78, 33), (79, 35), (80, 33), (81, 36), (82, 36), (83, 35), (84, 36), (85, 34), (86, 35),
          (87, 34), (88, 34), (89, 35), (90, 33), (91, 35), (92, 31), (93, 31), (94, 31), (95, 35)]
temperatures = [e for e in temperature]
canicule = [1 if temperatures[i] >= seuils[i][1] else 0 for i in range(len(seuils))] + ["", "", "", "", ""]

print("Determination de la présence d'une canicule effectuée")

# Determination d'innondation inspirée par KNN se basant sur des valeurs de precipitation, de temperature, de débit des rivières et d'humidité relative durant des innondations historiques françaises (données provenants surtout de Météo France)

probabilite_flood = []

var2010 = (143.6, 17.7, 234, 75.1)
garonne2013 = (36.4, 27.1, 2171, 63.6)
languedoc2014 = (54.7, 16.3, 867, 85.6)
seine2016 = (10.2, 20.3, 4180, 75.7)
aude2018 = (94.4, 14.4, 769, 90.3)
occitanie2020 = (57.5, 17.8, 924, 80.2)


def distance_4d(t1, t2):
    return sqrt(sum([(t1[i] - t2[i]) ** 2 for i in range(4)]))

def distance_flood(t):
    if t[2] is None:
        return 0
    liste_distances = [distance_4d(t, e) for e in [var2010, garonne2013, languedoc2014, seine2016, aude2018, occitanie2020]]
    return round(sum(liste_distances), 3)

for i in range(len(precipitation)): # On a que les données d'humidité pour la france metropolitaine
    try:
        probabilite_flood.append(distance_flood((precipitation[i], temperature[i], river_discharge[i], humidite_relative[i])))
    except ValueError:
        probabilite_flood.append("")

def z_score_normalization(distance, ensemble_distances=probabilite_flood):
    """
    float, list --> float
    Processus de normalisation z-score: Determination de l'intensité de la variance de la distance pour KNN par rapport a la moyenne de ensemble_distances
    """
    return abs((distance - numpy.mean(ensemble_distances)) / numpy.std(ensemble_distances))

probabilite_floodv2 = [z_score_normalization(e) if e != 0 else None for e in probabilite_flood]


print("Determination du risque d'innondations effectué")

print("Calcul des probabilités de catastrophes naturelles effectué")


# ON IMPORTE LES COLONNES

print("Importation de toutes les données dans le tableau")

df["code"] = liste_departements
df["Date"] = [date.isoformat()[:10] for i in range(101)]
df["Temperature (°C)"] = temperature
df["Humidite_relative (%)"] = humidite_relative
df["Temperature_ressentie (°C)"] = temperature_ressentie
df["Probabilite_pluie (%)"] = probabilite_pluie
df["Precipitation (mm)"] = precipitation
df["Pression (0m)(hPa)"] = pression_niveaumer
df["Couverture_nuageuse (%)"] = couverture_nuageuse
df["Visibility (m)"] = visibility
df["Vitesse_vent (km/h)"] = vitesse_vent
df["Index_UV"] = index_uv
df["Air_quality (pm2.5)"] = air_quality
df["River_discharge (m3/s)"] = river_discharge
df["Probabilité sècheresse"] = index_secheresse
df["Probabilité canicule (%)"] = canicule
df["Probabilité innondation"] = probabilite_floodv2
if variable == 0:  # Si la requête est pour aujourd'hui
    df["Indice"] = indices_meteov2
else:
    df["Indice"] = [None for i in range(101)]
df["Etat_meteo"] = [None for i in range(101)]
df.to_csv('donnees_meteo.csv', index=False)

"""
from TESTINUTILE import create_table
import time
DEOBGAGE : verifier que donnes_meteo contient bien tous les élements attendus
create_table('donnees_meteo.csv')
with open('donnees_meteo.csv','r') as f:
    print(list(csv.reader(f))[0])
time.sleep(1344)
"""

if variable == 0: # Si la requête est pour aujourd'hui
    # ALGORITHME KNN DETERMINATION METEO

    # determination des fieldnames qui serviront tout le long
    descriteurs = []
    with open('donnees_meteo.csv', 'r') as f:
        descripteurs = list(csv.reader(f))[0]

    def distance(el1, el2):
        """ dict, dict -> int
        renvoie la distance de Manhattan entre 2 images positions
        """
        d = 0
        #attributs = ['Temperature (°C)','Humidite_relative (%)','Temperature_ressentie (°C)','Probabilite_pluie (%)','Precipitation (mm)','Pression (0m)(hPa)','Couverture_nuageuse (%)','Visibility (m)','Vitesse_vent (km/h)','River_discharge (m3/s)','Probabilité innondation','Indice'] # LA COLONNE 'Air_quality (pm2.5)' est vide !!! 'Probabilité canicule (%)' est un booléen !!!
        attributs = ['Temperature (°C)','Humidite_relative (%)','Temperature_ressentie (°C)','Probabilite_pluie (%)','Visibility (m)','Indice','Pression (0m)(hPa)']
        for q in attributs: # on examine certains attributs du departements dont on cherchhe à déterminer l'état météo et les departements classifiés
            d += abs(float(el1[q]) - float(el2[q]))
        return d


    def charge_table(nom_fichier):
        """ str -> list
        renvoie une liste de dictionnaires
        """
        with open(nom_fichier, 'r') as f:
            lect = csv.DictReader(f, delimiter=',', fieldnames=descripteurs)
            liste_dict = []
            for row in lect:
                # partie nouvelle
                if row['Indice'] != 'NULL':
                    liste_dict.append(row)
        return liste_dict[1:]


    def frequence_etats(table):
        """ list -> dict
        prend en paramètre une liste de dictionnaires (élèves)
        renvoie le dictionnaire des fréquences des maisons
        """
        d = {}
        for e in table:
            m = e['Etat_meteo']
            if m not in d:
                d[m] = 1
            else:
                d[m] += 1

        for m in d:
            d[m] = d[m] / len(table)

        return d


    def meteo_majoritaire(table):
        """ list -> str
        prend en paramètre une liste de dictionnaires (élèves)
        renvoie la maison la plus représentée
        """
        dict_freq = frequence_etats(table)
        freq_max = 0
        for m in dict_freq:
            if dict_freq[m] > freq_max:
                maison = m
                freq_max = dict_freq[m]

        return maison


    def k_plus_proches_voisins(nouveau, table, k):
        '''
        nouveau : un dictionnaire contenant les informations d'une image à classer
        table : une liste d'images déjas classifiées (en provenance de donnees_classifiees)
        k : le nombre de voisins à integrer

        :out : liste de longueur k des plus proches voisins
        '''
        distances = {}  # dictionnaire de distances et de l'indice de l'éleve dans la liste d'éleves identifiés
        for i in range(len(table)):
            distances[i] = distance(table[i], nouveau)
        distances = sorted(distances.items(), key=lambda item: item[1])[:k]  # on ne garde que les k premiers
        # distances : un tuple (indice_eleve, distance)
        eleves_k = [{} for _ in range(k)]  # creer une liste de dictionnaires
        for i in range(len(distances)):
            eleves_k[i] = table[distances[i][0]]
        return eleves_k


    def meteo_majoritaire(table):
        meteos = ['Rainy', 'Cloudy', 'Foggy', 'Sunny', 'Night']
        return sorted(frequence_etats(table).items(), key=lambda item: item[1], reverse=True)[0][0]  # on peux enlever le second [0] pour afficher le score en plus


    def alocation_meteo():
        '''
        associe à chaque département un état météo basé sur un dataset supervisé
        '''
        table_supervisee = charge_table('donnees_meteo_classifiees.csv') # charger le dataset classifé qui sert de support
        with open('donnees_meteo.csv') as f:
            # ouvrir le fichier à charger
            lect = csv.DictReader(f, delimiter=',',
                                  fieldnames=descripteurs)
            global meteo_associee
            meteo_associee = []
            for row in lect:
                if row['Indice'] != 'NULL':
                    meteo_associee.append(row)

        for i in range(1,len(meteo_associee)):
            meteo_associee[i]['Etat_meteo'] = meteo_majoritaire(k_plus_proches_voisins(meteo_associee[i], table_supervisee, 3))
        with open('donnees_meteo.csv','w') as f:
            ecr = csv.DictWriter(f,fieldnames=descripteurs)
            ecr.writerows(meteo_associee)

        print('algorithme KNN terminé')

    alocation_meteo()

print("Tableau donnees_meteo.csv mis à jour!")
