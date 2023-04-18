# TP Choixpeau magique

import csv

def distance(el1, el2):
    """ dict, dict -> int
    renvoie la distance de Manhattan entre 2 images positions
    """
    d = 0
    attributs = ['indice','temperature','humidite']
    for q in attributs :
        d += abs(float(el1[q])-float(el2[q]))
    return d


def charge_table(nom_fichier):
    """ str -> list
    renvoie une liste de dictionnaires
    """
    with open(nom_fichier,'r') as f:
        lect = csv.DictReader(f, delimiter = ',',fieldnames=['Code','coordonnees','indice','temperature','humidite','weather'])
        liste_eleves = []
        for row in lect :
            # partie nouvelle
            if row['indice'] != 'NULL':
                liste_eleves.append(row)
    return liste_eleves[1:]
    

def frequences_des_maisons(table):
    """ list -> dict
    prend en paramètre une liste de dictionnaires (élèves)
    renvoie le dictionnaire des fréquences des maisons
    """
    d = {}
    for e in table :
        m = e['weather']
        if m not in d:
            d[m] = 1
        else :
            d[m] += 1

    for m in d :
        d[m] = d[m]/len(table)
        
    return d


def meteo_majoritaire(table):
    """ list -> str
    prend en paramètre une liste de dictionnaires (élèves)
    renvoie la maison la plus représentée
    """
    dict_freq = frequences_des_maisons(table)
    freq_max = 0
    for m in dict_freq :
        if dict_freq[m] > freq_max :
            maison = m
            freq_max = dict_freq[m]
            
    return maison

def k_plus_proches_voisins(nouveau, table, k):
    '''
    nouveau : un dictionnaire contenant les informations d'un éleve à classer
    table : une liste de dictionnaire d'élèves déja enregistrés
    k : le nombre de voisins à integrer 

    :out : liste de longueur k des plus proches voisins
    '''
    distances = {} # dictionnaire de distances et de l'indice de l'éleve dans la liste d'éleves identifiés
    for i in range(len(table)):
        distances[i] = distance(table[i],nouveau)
    distances = sorted(distances.items(), key=lambda item: item[1])[:k] # on ne garde que les k premiers
    # distances : un tuple (indice_eleve, distance)
    eleves_k = [{} for _ in range(k)] # creer une liste de dictionnaires
    for i in range(len(distances)):
        eleves_k[i] = table[distances[i][0]]
    return eleves_k

def meteo_majoritaire(table):
    maisons = ['Rainy','Cloudy','Foggy','Sunny']
    return sorted(frequences_des_maisons(table).items(), key=lambda item: item[1],reverse=True)[0][0] # on peux enlever le second [0] pour afficher le score en plus

def alocation_meteo():
    table_supervisee = charge_table('donnes_classifiees.csv')
    with open('donnes_a_classifie.csv') as f:
        lect = csv.DictReader(f, delimiter = ',',fieldnames=['Code','coordonnees','indice','temperature','humidite','weather'])
        global elements_assigner
        elements_assigner = []
        for row in lect:
            if row['indice'] != 'NULL':
                elements_assigner.append(row)

    for i in range(1,len(elements_assigner)):
        elements_assigner[i]['weather'] = meteo_majoritaire(k_plus_proches_voisins(elements_assigner[i],table_supervisee,3))
        # ETAPE SUIVANTE : enlever les doublons
    
    from collections import Counter

    # Group the dictionaries by their 'Code' value
    groups = {}
    for d in elements_assigner:
        code = d['Code']
        if code not in groups:
            groups[code] = []
        groups[code].append(d)

    # Merge the dictionaries with the same 'Code' value
    merged = []
    for code, group in groups.items():
        # Count the occurrences of each 'weather' value
        weather_counts = Counter(d['weather'] for d in group)
        # Find the most common 'weather' value
        most_common_weather = weather_counts.most_common(1)[0][0]
        # Merge the dictionaries with the same 'Code' value and keep the most common 'weather' value
        merged_dict = {
            'Code': code,
            'coordonnees': group[0]['coordonnees'],
            'indice': group[0]['indice'],
            'temperature': group[0]['temperature'],
            'humidite': group[0]['humidite'],
            'weather': most_common_weather
        }
        merged.append(merged_dict)
        a_ecrire = []
        for i in range(1,len(merged)):
            a_ecrire.append({'Code':merged[i]['Code'],'Temperature':merged[i]['temperature'],'etat':merged[i]['weather']})
    with open('tableau_finalv2.csv','w') as f:
        ecr = csv.DictWriter(f,delimiter=',',fieldnames=['Code','Temperature','etat'])
        ecr.writeheader()
        ecr.writerows(a_ecrire)
    
alocation_meteo()