import csv
noms_departements = []
with open("departements-france.csv","r") as f:
    ecr = csv.reader(f,delimiter=',')
    for ligne in ecr:
        noms_departements.append(ligne[0])

from random import randint

def randomizer():
    with open("temperature_data.csv","w") as f:
        ecr = csv.writer(f,delimiter=',')
        ecr.writerow(['Code','Temperature'])
        fichier = []
        for i in range(1,len(noms_departements)):
            fichier.append([noms_departements[i],randint(1,40)])

        ecr.writerows(fichier)