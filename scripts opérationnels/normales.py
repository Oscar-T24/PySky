import csv
import pandas as pd
from datetime import datetime

today = datetime.now()

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

with open('normale.csv', 'w', newline='') as n:
    normale = csv.writer(n)
    normale.writerow(["Code", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
    for e in coordonnees:
        c = e['coordonnee'].split(" ")
        d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])
        print(f"Calcul de l'humidité moyenne par mois du département {d}")
        normales_dep = [d]
        for mois in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            normales_dep_mois = []
            for year in range(today.year - 31, today.year - 1):
                data = pd.read_json(f'https://archive-api.open-meteo.com/v1/archive?latitude={x}&longitude={y}&start_date={year}-{mois}-15&end_date={year}-{mois}-15&hourly=temperature_2m,relativehumidity_2m,precipitation,soil_moisture_0_to_7cm')
                #print(data.to_string())
                liste = data.values.tolist()[2][-1] # 2 car c'est le troisième paramètre que l'on appelle de l'API
                #print(liste)
                normales_dep_mois.append(round(sum(liste)/len(liste), 4))
            normales_dep.append(round(sum(normales_dep_mois)/len(normales_dep_mois), 4))
        normale.writerow(normales_dep)
