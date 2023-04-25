import csv
import pandas as pd
from datetime import datetime

today = datetime.now()

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

air_quality = []
river_discharge = []
probabilite_pluie = []
precipitation = []
pression = []
couverture_nuageuse = []
visibility = []
vitesse_vent = []
index_ux = []


for e in coordonnees:
    c = e['coordonnee'].split(" ")
    d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])
    print(d)
    # Données de qualité de l'air
    data = pd.read_json(f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={x}&longitude={y}&hourly=pm2_5&start_date={today.isoformat()[:10]}&end_date={today.isoformat()[:10]}")
    quality = data.values.tolist()[1][-1][today.hour]
    air_quality.append(quality)
    

    # Débit moyen des rivières
    data = pd.read_json(f"https://flood-api.open-meteo.com/v1/flood?latitude={x}&longitude={y}&daily=river_discharge_mean&start_date={today.isoformat()[:10]}&end_date={today.isoformat()[:10]}&forecast_days=1")
    debit = data.values.tolist()[1][-1][0]
    river_discharge.append(debit)

    data = pd.read_json(f"https://api.open-meteo.com/v1/forecast?latitude={x}&longitude={y}&hourly=precipitation_probability,precipitation,surface_pressure,cloudcover,visibility,windspeed_10m,uv_index&forecast_days=1&start_date={today.isoformat()[:10]}&end_date={today.isoformat()[:10]}")

    probabilite_pluie.append(data.values.tolist()[1][-1][today.hour])
    precipitation.append(data.values.tolist()[2][-1][today.hour])
    pression.append(data.values.tolist()[3][-1][today.hour])
    couverture_nuageuse.append(data.values.tolist()[4][-1][today.hour])
    visibility.append(data.values.tolist()[5][-1][today.hour])
    vitesse_vent.append(data.values.tolist()[6][-1][today.hour])
    index_ux.append(data.values.tolist()[7][-1][today.hour])


print(air_quality)
df = pd.read_csv('tableau_finalv2.csv')
df["air_quality (pm2.5)"] = air_quality
df["river_discharge (m3/s)"] = river_discharge
df["probabilite_pluie (%)"] = probabilite_pluie
df["precipitation (mm)"] = precipitation
df["pression (hPa)"] = pression
df["couverture_nuageuse (%)"] = couverture_nuageuse
df["visibility (m)"] = visibility
df["vitesse_vent (km/h)"] = vitesse_vent
df["index_ux"] = index_ux
df.to_csv('tableau_finalv2.csv', index=False)
