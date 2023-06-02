
import subprocess 
import time

while True:
    time_depart = time.time()
    subprocess.run(["python3", "recuperation_donneswebcam.py"])
    print('etape 1 finie : actualisation de la base de donnée webcams')
    global temps
    temps = time.time() - time_depart
    with open('temps_ecoulement.txt','a') as f:
        f.write(f'temps ecoule :{temps}s pour la recuperation des données caméras')
        f.write('\n')