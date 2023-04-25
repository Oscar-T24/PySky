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
        print(f"Calcul de la precipitation moyenne par mois du département {d}")
        normales_dep = [d]
        for mois in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
            normales_dep_mois = []
            for year in range(today.year - 11, today.year - 1):
                data = pd.read_json(f'https://archive-api.open-meteo.com/v1/archive?latitude={x}&longitude={y}&start_date={year}-{mois}-15&end_date={year}-{mois}-15&daily=precipitation_sum&timezone=Europe%2FLondon')
                #print(data.to_string())
                precipitation = data.values.tolist()[1][-1][0] # 2 car c'est le troisième paramètre que l'on appelle de l'API
                #print(precipitation)
                normales_dep_mois.append(precipitation)
            normales_dep.append(round(sum(normales_dep_mois)/len(normales_dep_mois), 4))
        normale.writerow(normales_dep)
