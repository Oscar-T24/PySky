from indice import determine_weather_index
from tronque import tronquer
import requests
from PIL import Image
from io import BytesIO
import numpy
from datetime import datetime, timedelta
import csv
from math import sqrt
import pandas as pd
import argparse

variable = 0

if variable == 0: # Si la requête est pour aujourd'hui
    # ALGORITHME KNN DETERMINATION METEO

    # determination des fieldnames qui serviront tout le long
    descriteurs = []
    with open('donnees_meteo.csv', 'r') as f:
        descripteurs = list(csv.reader(f))[0]


    def distance(el1, el2):
        """ dict, dict -> int
        renvoie la distance de Manhattan entre 2 images positions
        """
        d = 0
        attributs = ['Temperature (°C)','Humidite_relative (%)','Temperature_ressentie (°C)','Probabilite_pluie (%)','Precipitation (mm)','Pression (0m)(hPa)','Couverture_nuageuse (%)','Visibility (m)','Vitesse_vent (km/h)','River_discharge (m3/s)','Probabilité innondation','Indice'] # LA COLONNE 'Air_quality (pm2.5)' est vide !!! 'Probabilité canicule (%)' est un booléen !!!
        for q in attributs:
            if type(el1[q]) == str:
                from random import randint
                el1[q] = randint(0,100)
            d += abs(float(el1[q]) - float(el2[q]))
        return d


    def charge_table(nom_fichier):
        """ str -> list
        renvoie une liste de dictionnaires
        """
        with open(nom_fichier, 'r') as f:
            lect = csv.DictReader(f, delimiter=',', fieldnames=descripteurs)
            liste_dict = []
            for row in lect:
                # partie nouvelle
                if row['Indice'] != 'NULL':
                    liste_dict.append(row)
        return liste_dict[1:]


    def frequence_etats(table):
        """ list -> dict
        prend en paramètre une liste de dictionnaires (élèves)
        renvoie le dictionnaire des fréquences des maisons
        """
        d = {}
        for e in table:
            m = e['Etat_meteo']
            if m not in d:
                d[m] = 1
            else:
                d[m] += 1

        for m in d:
            d[m] = d[m] / len(table)

        return d


    def meteo_majoritaire(table):
        """ list -> str
        prend en paramètre une liste de dictionnaires (élèves)
        renvoie la maison la plus représentée
        """
        dict_freq = frequence_etats(table)
        freq_max = 0
        for m in dict_freq:
            if dict_freq[m] > freq_max:
                maison = m
                freq_max = dict_freq[m]

        return maison


    def k_plus_proches_voisins(nouveau, table, k):
        '''
        nouveau : un dictionnaire contenant les informations d'une image à classer
        table : une liste d'images déjas classifiées (en provenance de donnees_classifiees)
        k : le nombre de voisins à integrer

        :out : liste de longueur k des plus proches voisins
        '''
        distances = {}  # dictionnaire de distances et de l'indice de l'éleve dans la liste d'éleves identifiés
        for i in range(len(table)):
            distances[i] = distance(table[i], nouveau)
        distances = sorted(distances.items(), key=lambda item: item[1])[:k]  # on ne garde que les k premiers
        # distances : un tuple (indice_eleve, distance)
        eleves_k = [{} for _ in range(k)]  # creer une liste de dictionnaires
        for i in range(len(distances)):
            eleves_k[i] = table[distances[i][0]]
        return eleves_k


    def meteo_majoritaire(table):
        meteos = ['Rainy', 'Cloudy', 'Foggy', 'Sunny', 'Night']
        return sorted(frequence_etats(table).items(), key=lambda item: item[1], reverse=True)[0][0]  # on peux enlever le second [0] pour afficher le score en plus


    def alocation_meteo():
        '''
        associe à chaque département un état météo basé sur un dataset supervisé
        '''
        table_supervisee = charge_table('donnees_meteo_classifiees.csv') # charger le dataset classifé qui sert de support
        with open('donnees_meteo.csv') as f:
            # ouvrir le fichier à charger
            lect = csv.DictReader(f, delimiter=',',
                                  fieldnames=descripteurs)
            global meteo_associee
            meteo_associee = []
            for row in lect:
                if row['Indice'] != 'NULL':
                    meteo_associee.append(row)

        for i in range(1,len(meteo_associee)):
            meteo_associee[i]['Etat_meteo'] = meteo_majoritaire(k_plus_proches_voisins(meteo_associee[i], table_supervisee, 3))
            print(meteo_associee[i]['Etat_meteo'])
        with open('donnees_meteo.csv','w') as f:
            ecr = csv.DictWriter(f,fieldnames=descripteurs)
            ecr.writerows(meteo_associee)

        print('algorithme KNN terminé')

    alocation_meteo()

print("Tableau donnees_meteo.csv mis à jour!")
