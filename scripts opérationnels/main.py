import subprocess
import time

time_depart = time.time()
#subprocess.run(["python3", "recuperation_donneswebcam.py"])
#exec('recuperation_donneswebcam.py')
print('etape 1 finie : actualisation de la base de donnée webcams')
subprocess.run(["python3", "preparation_dataset_machinelearning_supervisé.py"])
print('etape 2 finie : preparation du dataset de supervisation')
subprocess.run(["python3", "KNN_meteo.py"])
print('etape 3 finie : analyse de la météo')
print('temps ecoulé pour tout faire : ',time.time() - time_depart)
