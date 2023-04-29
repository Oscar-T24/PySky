import subprocess
import time
from datetime import datetime
import argparse
import os

'''
subprocess.run(["python3", "recuperation_donneswebcam.py"])
print('etape 1 finie : actualisation de la base de donnée webcams')
'''
def main(jours_diff):
    '''
    execute la totalité des scripts necessaires à lk'actualisation de la carte pour une date donnéee
    '''
    time_depart = time.time()
    try:    
        os.remove('donnes_meteo.csv') # supprimer le fichier 'donnes_meteo.csv' afin d'en generer un nouveau
    except: # si le fichier est inexistant, pas besoin de le supprimer
        pass

    print('jours de différences', jours_diff)

    assert os.path.isfile(os.path.join('', 'donnees_meteo_classifiees.csv')) == True,'fichier données météos classifiées introuvable ! Veuillez lancer preparation_dataset_machinelearning_supervisé.py'

    subprocess.run(["python3", "preparation_dataset_a_trier.py","-value",str(jours_diff)])
    print('etape 3 finie : preparation du dataset à classifier')

    assert os.path.isfile(os.path.join('', 'donnes_meteo.csv')) == True,'fichier données météos introuvable ! Veuillez relancer run.py de nouveau'

    subprocess.run(["python3", "cartographie.py"])
    print('etape 5 finie :creation d"une carte')
    now = datetime.now()
    dt_string = now.strftime("%d %H :%M")
    print('temps ecoulé pour tout faire : (etape 2,3,4)', time.time() - time_depart)
    global temps
    temps = time.time() - time_depart
    with open('temps_ecoulement.txt', 'a') as f:
        f.write(f'temps ecoule :{temps}s (etape 2,3,4) {dt_string}')
        f.write('\n')
    # temps pour faire les étapes 2 à 4 : 4 minutes +/- 10s
    # temps pour la partie 1 : 160,7 minutes soit 2,67 heures
    return 

if __name__ == '__main__':
    try: 
        parser = argparse.ArgumentParser(description='afficher valeur de la commande de ligne')
        parser.add_argument('-value', help='la valeur à afficher')
        args = parser.parse_args()
        jours_diff= int(args.value)
        main(jours_diff)
    except ValueError:
        # si value n'est pas défini, ne pas executer d'actualisation
        pass
        
