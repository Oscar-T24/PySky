from indice import determine_weather_index
from tronque import tronquer
import requests
from PIL import Image
from io import BytesIO
import numpy
import re
import csv
import pandas as pd
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim

with open('diff_jours.txt','r+') as f:
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

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

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


for e in coordonnees:
    c = e['coordonnee'].split(" ")
    d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])
    print(d)

    data = pd.read_json(f"https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&hourly=temperature_2m,relativehumidity_2m,apparent_temperature,precipitation_probability,precipitation,pressure_msl,cloudcover,visibility,windspeed_10m,uv_index&forecast_days=1&start_date={date.isoformat()[:10]}&end_date={date.isoformat()[:10]}")
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


indices_meteo = {}

def get_department(commune_name):
    geolocator = Nominatim(user_agent="my-app")
    commune_name = commune_name.encode('ISO 8859-1').decode('utf-8')
    print(commune_name)
    if 'Paris' in commune_name:  # on sait pas pk ca marche pas avec Paris (renbvoi 13 mais c Marseille ca)
        return '75'
    location = geolocator.geocode(commune_name + ", France")
    if location:
        return "".join(re.findall(r'-?\d+', location.raw['display_name']))[:2]
    else:
        return None

with open('donnees_camerasv2.csv', 'r') as f:
    read = csv.DictReader(f, fieldnames=['lien', 'departement'])
    # determination de l'indice
    for ligne in read:
        try: 
            response = requests.get(ligne["lien"])
            img = Image.open(BytesIO(response.content))
            open_cv_image = numpy.array(img)
            # Convert RGB to BGR 
        except : 
            print('ERREUR')
            continue
        no_departement = ligne['departement']
        try:
            open_cv_image = open_cv_image[:, :, ::-1].copy()
            image_tronquee = tronquer(open_cv_image)
        except:
            print("problemes d'indexations ou autre avec tronuqer")
            continue
        indices_meteo[no_departement] =  determine_weather_index(image_tronquee) # NE MARCHE PAS AVEC LA CORSE
        print(indices_meteo[no_departement])
        # UNE SEULE camera par departement 

for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, "2A", "2B", 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 971, 972, 973, 974, 976]:
    if i not in indices_meteo.keys():
        indices_meteo[str(i)] = "NULL"

print(sorted(list(indices_meteo.items()))) # TRI MAL LES DEPARTEMENTS ET LES METS SUR LE TABLEAU DANS LE MAUVAIS ORDRE
# on comble les departements sans infos avec les temperatures

df = pd.read_csv('tableau_finalv2.csv')
df["air_quality (pm2.5)"] = air_quality
df["river_discharge (m3/s)"] = river_discharge
df["probabilite_pluie (%)"] = probabilite_pluie
df["precipitation (mm)"] = precipitation
df["pression (hPa)"] = pression_niveaumer
df["couverture_nuageuse (%)"] = couverture_nuageuse
df["visibility (m)"] = visibility
df["vitesse_vent (km/h)"] = vitesse_vent
df["index_ux"] = index_ux
df["Etat_meteo"] = [e[1] for e in sorted(list(indices_meteo.items()))]
df.to_csv('tableau_finalv2.csv', index=False)
