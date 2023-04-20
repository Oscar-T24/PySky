import subprocess
import time

'''
subprocess.run(["python3", "recuperation_donneswebcam.py"])
print('etape 1 finie : actualisation de la base de donnée webcams')
'''
from datetime import datetime
while True:
    time_depart = time.time()
    #subprocess.run(["python3", "preparation_dataset_machinelearning_supervisé.py"])
    print('etape 2 finie : preparation du dataset de supervisation')
    subprocess.run(["python3", "preparation_dataset_a_trier.py"])
    print('etape 3 finie : preparation du dataset à classifier')
    subprocess.run(["python3", "KNN_meteo.py"])
    print('etape 4 finie : analyse de la météo')
    #subprocess.run(["python3", "cartographie-temperature-departements.py"])
    #print('etape 5 finie :creation d"une carte')
    now = datetime.now()
    dt_string = now.strftime("%d %H:%M")
    print('temps ecoulé pour tout faire : (etape 2,3,4)',time.time() - time_depart)
    global temps
    temps = time.time() - time_depart
    with open('temps_ecoulement.txt','a') as f:
        f.write(f'temps ecoule :{temps}s (etape 2,3,4) {dt_string}')
        f.write('\n')
    with open('cartographie-temperature-departements.py','a') as f: #ecrire sur le fichier cartographie pour relancer flask
        f.write('a')
# temps pour faire les étapes 2 à 4 : 4 minutes +/- 10s
# temps pour la partie 1 : 160,7 minutes soit 2,67 heures


