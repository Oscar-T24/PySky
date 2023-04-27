import subprocess
import time
from datetime import datetime, timedelta, date
import sys
import pandas as pd
import argparse

'''
subprocess.run(["python3", "recuperation_donneswebcam.py"])
print('etape 1 finie : actualisation de la base de donnée webcams')
'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Print the value of a command line argument')
    parser.add_argument('-value', help='the value to be printed')
    args = parser.parse_args()
    jours_diff= int(args.value) # 
        
time_depart = time.time()
print('jours de différences',jours_diff)

subprocess.run(["python3", "preparation_dataset_a_trier.py","-value",str(jours_diff)])
print('etape 3 finie : preparation du dataset à classifier')
if int(jours_diff) == 0:
    subprocess.run(["python3", "KNN_meteo.py"])  # script qui associe un état météo à un département
    print('etape 4 finie : analyse de la météo')
else:
    print('etape 4 sautée : demande utilisateur historic data')
subprocess.run(["python3", "cartographie.py"])
print('etape 5 finie :creation d"une carte')
now = datetime.now()
dt_string = now.strftime("%d %H:%M")
print('temps ecoulé pour tout faire : (etape 2,3,4)', time.time() - time_depart)
global temps
temps = time.time() - time_depart
with open('temps_ecoulement.txt', 'a') as f:
    f.write(f'temps ecoule :{temps}s (etape 2,3,4) {dt_string}')
    f.write('\n')
# temps pour faire les étapes 2 à 4 : 4 minutes +/- 10s
# temps pour la partie 1 : 160,7 minutes soit 2,67 heures
