import os
import time

time_depart = time.time()
with open("recuperation_donneswebcam.py") as f:
    exec(f.read())
#exec('recuperation_donneswebcam.py')
print('etape 1 finie : actualisation de la base de donnée webcams')
with open("preparation_dataset_machinelearning_supervisé.py") as f:
    exec(f.read())
print('etape 2 finie : preparation du dataset de supervisation')
with open("KNN_meteo.py") as f:
    exec(f.read())
print('etape 3 finie : analyse de la météo')
print('temps ecoulé pour tout faire : ',time.time() - time_depart)
