import csv
from datetime import datetime
from math import sqrt
import pandas as pd

mois = str(datetime.now().month)

f = open('tableau_finalv2.csv', 'r')
meteo = list(csv.DictReader(f, delimiter=','))

f = open('normale_precipitation.csv', 'r')
normale = list(csv.DictReader(f, delimiter=','))

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))

# Determination de secheresse  selon la page 13 du "Manuel des indicateurs et indices de sécheresse" de l'organisation meteorologique mondiale (OMM)

index_secheresse = [float(meteo[i]['precipitation (mm)']) / float(normale[i][mois]) * 100 for i in range(len(normale))]

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
temperatures = [e["Temperature"] for e in meteo]
canicule = [True if float(temperatures[i]) >= seuils[i][1] else False for i in range(len(seuils))] + ["", "", "", "", ""]

# Determination d'innondation inspirée par KNN se basant sur des valeurs de precipitation, de temperature et de débit des rivières durant des innondations historiques françaises (données provenants surtout de Météo France)

probabilite_flood = []

var2010 = (143.6, 17.7, 234)
garonne2013 = (36.4, 27.1, 2171)
languedoc2014 = (54.7, 16.3, 867)
seine2016 = (10.2, 20.3, 4180)
aude2018 = (94.4, 14.4, 769)
occitanie2020 = (57.5, 17.8, 924)


def distance_3d(t1, t2):
    return sqrt(sum([(t1[i] - t2[i]) ** 2 for i in range(3)]))


def distance_flood(t):
    liste_distances = [distance_3d(t, e) for e in
                       [var2010, garonne2013, languedoc2014, seine2016, aude2018, occitanie2020]]
    return round(sum(liste_distances) / 6, 3)


for e in meteo:
    try:
        probabilite_flood.append(distance_flood(
            (float(e["precipitation (mm)"]), float(e["Temperature"]), float(e["river_discharge (m3/s)"]))))
    except ValueError:
        probabilite_flood.append("")

# ajout au tableau de données principal

df = pd.read_csv('tableau_finalv2.csv')
df["Probabilité sècheresse"] = index_secheresse
df["Probabilité canicule (%)"] = canicule
df["Probabilité innondation"] = probabilite_flood
df.to_csv('tableau_finalv2.csv', index=False)
