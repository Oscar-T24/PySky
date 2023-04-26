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

# RECUPERE LA DATE DEMANDÉE PAR L'UTILISATEUR, PAR DEFAULT LA DATE D'AUJOURD'HUI
with open('diff_jours.txt', 'r+') as f:
    global variable
    variable = f.read()
    if variable == '':
        variable = 0
    else:
        variable = int(variable)
    f.write('')

today = datetime.now()
dif = timedelta(days=variable)
date = today + dif

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
index_ux = []
air_quality = []
river_discharge = []

# ON REMPLIT LES COLONNES
for e in coordonnees:
    c = e['coordonnee'].split(" ")
    d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])

    data = pd.read_json(f"https://api.open-meteo.com/v1/forecast?latitude={x}&longitude={y}&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,pressure_msl,cloudcover,visibility,windspeed_10m,uv_index&forecast_days=1&start_date={date.isoformat()[:10]}&end_date={date.isoformat()[:10]}")
    temperature.append(data.values.tolist()[1][-1][today.hour])
    humidite_relative.append(data.values.tolist()[2][-1][today.hour])
    temperature_ressentie.append(data.values.tolist()[3][-1][today.hour])
    probabilite_pluie.append(data.values.tolist()[4][-1][today.hour])
    precipitation.append(data.values.tolist()[5][-1][today.hour])
    pression_niveaumer.append(data.values.tolist()[6][-1][today.hour])
    couverture_nuageuse.append(data.values.tolist()[7][-1][today.hour])
    visibility.append(data.values.tolist()[8][-1][today.hour])
    vitesse_vent.append(data.values.tolist()[9][-1][today.hour])
    index_ux.append(data.values.tolist()[10][-1][today.hour])

    # Données de qualité de l'air
    data = pd.read_json(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={x}&longitude={y}&hourly=pm2_5&start_date={date.isoformat()[:10]}&end_date={date.isoformat()[:10]}")
    quality = data.values.tolist()[1][-1][today.hour]
    air_quality.append(quality)

    # Débit moyen des rivières
    data = pd.read_json(f"https://flood-api.open-meteo.com/v1/flood?latitude={x}&longitude={y}&daily=river_discharge_mean&start_date={date.isoformat()[:10]}&end_date={date.isoformat()[:10]}&forecast_days=1")
    debit = data.values.tolist()[1][-1][0]
    river_discharge.append(debit)

    print(f"Données météo extraites pour le département {d} (sur 101)")

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
            print("Probleme avec le tronquage de l'image")
            erreurs += 1
            continue
        succes += 1
        indices_meteo[no_departement] = determine_weather_index(image_tronquee) # Ne prend que la dernière camera analysée par departement

print(f"Analyse des images finie ; indexes extraits: {erreurs} erreurs pour {succes} succès. Taux de réussite de {(succes-erreurs)*100/(succes+erreurs)}%")



# ON TRIE LES INDICES DANS L'ORDRE DES LIGNES
liste_departements = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16',
                      '17', '18', '19', '21', '22', '23', '24', '25', '26', '27', '28', '29', '2A', '2B', '30', '31',
                      '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45', '46', '47',
                      '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59', '60', '61', '62', '63',
                      '64', '65', '66', '67', '68', '69', '70', '71', '72', '73', '74', '75', '76', '77', '78', '79',
                      '80', '81', '82', '83', '84', '85', '86', '87', '88', '89', '90', '91', '92', '93', '94', '95',
                      '971', '972', '973', '974', '976']
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
canicule = [True if temperatures[i] >= seuils[i][1] else False for i in range(len(seuils))] + ["", "", "", "", ""]

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

probabilite_floodv2 = [None if e == 0 else e for e in probabilite_flood]

print("Determination du risque d'innondations effectué")


print("Calcul des probabilités de catastrophes naturelles effectué")


# ON IMPORTE LES COLONNES

print("Importation de toutes les données dans le tableau")

df["code"] = liste_departements
df["Date"] = [date for i in range(101)]
df["temperature (°C)"] = temperature
df["humidite_relative (%)"] = humidite_relative
df["temperature_ressentie (°C)"] = temperature_ressentie
df["probabilite_pluie (%)"] = probabilite_pluie
df["precipitation (mm)"] = precipitation
df["pression (0m)(hPa)"] = pression_niveaumer
df["couverture_nuageuse (%)"] = couverture_nuageuse
df["visibility (m)"] = visibility
df["vitesse_vent (km/h)"] = vitesse_vent
df["index_ux"] = index_ux
df["air_quality (pm2.5)"] = air_quality
df["river_discharge (m3/s)"] = river_discharge
df["Probabilité sècheresse"] = index_secheresse
df["Probabilité canicule (%)"] = canicule
df["Probabilité innondation"] = probabilite_flood
df["Indice"] = indices_meteov2
df["Etat_meteo"] = [None for i in range(101)]
df.to_csv('donnees_meteo_a_classifier.csv', index=False)

print("Tableau donnees_meteo.csv mis à jour!")
