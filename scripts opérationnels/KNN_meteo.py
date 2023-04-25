import requests
import csv
import json


def coordinate_temperature(coordonees):
    """
# Dans cet exemple nous allons utiliser le service météo du Meteorologisk institutt de Norvège
# (api.met.no/weatherapi is an interface to a selection of data produced by MET Norway)
# url: https://api.met.no/weatherapi/locationforecast/2.0/documentation

# Grâce à Google Maps, nous trouvons que les coordonnées de l'IUT à Mont de Marsan sont
# latitude 43.88566272770907, longitude -0.5092243304975015
#
# Ce qui nous donne l'URL suivante pour accéder aux prévisions météo au format JSON:
# https://api.met.no/weatherapi/locationforecast/2.0/compact?lat=43.88566272770907&lon=-0.5092243304975015
# Fetch data from URL
    """
    latitude = coordonees[0]
    longitude = coordonees[1]
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0',
               'Cache-Control': 'no-cache, no-store, must-revalidate', 'Pragma': 'no-cache', 'Expires': '0'}
    url = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}7&lon={longitude}",
                       headers=headers)
    text = url.text

    # Get JSON data
    data = json.loads(text)
    # print(data)

    # Process JSON data
    units = data["properties"]["meta"]["units"]
    weather = data["properties"]["timeseries"][0]["data"]["instant"]["details"]
    return weather


def distance(el1, el2):
    """ dict, dict -> int
    renvoie la distance de Manhattan entre 2 images positions
    """
    d = 0
    attributs = ['indice', 'temperature', 'humidite']
    for q in attributs:
        d += abs(float(el1[q]) - float(el2[q]))
    return d


def charge_table(nom_fichier):
    """ str -> list
    renvoie une liste de dictionnaires
    """
    with open(nom_fichier, 'r') as f:
        lect = csv.DictReader(f, delimiter=',',
                              fieldnames=['Code', 'coordonnees', 'indice', 'temperature', 'humidite', 'pression',
                                          'weather'])
        liste_eleves = []
        for row in lect:
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
    for e in table:
        m = e['weather']
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
    dict_freq = frequences_des_maisons(table)
    freq_max = 0
    for m in dict_freq:
        if dict_freq[m] > freq_max:
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
    maisons = ['Rainy', 'Cloudy', 'Foggy', 'Sunny', 'Night']
    return sorted(frequences_des_maisons(table).items(), key=lambda item: item[1], reverse=True)[0][
        0]  # on peux enlever le second [0] pour afficher le score en plus


def alocation_meteo():
    table_supervisee = charge_table('donnes_classifiees.csv')
    with open('donnes_a_classifie.csv') as f:
        lect = csv.DictReader(f, delimiter=',',
                              fieldnames=['Code', 'coordonnees', 'indice', 'temperature', 'humidite', 'pression',
                                          'weather'])
        global elements_assigner
        elements_assigner = []
        for row in lect:
            if row['indice'] != 'NULL':
                elements_assigner.append(row)

    for i in range(1, len(elements_assigner)):
        elements_assigner[i]['weather'] = meteo_majoritaire(
            k_plus_proches_voisins(elements_assigner[i], table_supervisee, 3))
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
            'pression': group[0]['pression'],
            'weather': most_common_weather
        }
        merged.append(merged_dict)
        '''
        for i in range(len(merged)):
            print(merged[i]['Code'])
        '''

        a_ecrire = []
        for i in range(1, len(merged)):
            a_ecrire.append(
                {'Code': merged[i]['Code'], 'Temperature': merged[i]['temperature'], 'etat': merged[i]['weather']})

    global codes_complets
    codes_complets = []

    with open('coordonnees_departements.csv', 'r') as f:  # pour combler les trous
        lect = csv.DictReader(f, fieldnames=['Code', 'departement', 'coordonnee'])
        for row in lect:
            codes_complets.append(row)
    codes_complets.pop(0)
    '''
        for i in range(len(a_ecrire)):
            if 'etat' in a_ecrire[i].keys():
                if a_ecrire[i]['etat'] != '':
                    print(a_ecrire[i]['Code'],a_ecrire[i])
    '''
    # print(codes_complets[1])
    # DEBOGAGE
    with open('tableau_finalv2.csv', 'w') as f:
        ecr = csv.DictWriter(f, delimiter=',', fieldnames=['Code', 'Temperature', 'etat'])
        ecr.writeheader()

        list1 = a_ecrire
        list2 = codes_complets

        merged_list = []
        for item in list2:
            match_found = False
            for d in list1:
                if d['Code'] == item['Code']:
                    merged_list.append(d)
                    match_found = True
                    break
            if not match_found:
                new_dict = {'Code': item['Code'], 'coordonnee': item['coordonnee']}
                merged_list.append(new_dict)
        '''
                # example input data
        list1 = a_ecrire # dictionnaire avcec des données potentiellements manquantes
        list2 = codes_complets # donnes pour completer les blancs de departements
        # create a dictionary from each input list where the keys are the 'Code' values
        dict1 = {d['Code']: d for d in list1}
        dict2 = {d['Code']: d for d in list2}

        # loop over the missing dictionaries in list1 and update with coordonnee if found in list2
        for d in list1:
            if d['Code'] in dict2:
                d2 = dict2[d['Code']]
                d.update({'coordonnee': d2['coordonnee']})
            else:
                d.update({'coordonnee': ''})

        # merge the updated dictionaries from list1 and the dictionaries from list2 into a single dictionary
        merged_dict = {**dict1, **dict2}

        # create a new list of dictionaries with the desired keys/values
        merged_list = []
        for code, d in merged_dict.items():
            if code in dict1:
                # retrieve 'Temperature' and 'etat' from the dictionary in list1
                temperature = dict1[code].get('Temperature', None)
                etat = dict1[code].get('etat', None)
                merged_list.append({'Code': code, 'Temperature': temperature, 'etat': etat, 'coordonnee': d.get('coordonnee', '')})
            else:
                # only keep 'Code' and 'coordonnee' for missing dictionaries
                merged_list.append({'Code': code, 'coordonnee': d.get('coordonnee', '')})

        merged_list = sorted(merged_list, key=lambda merged_list: merged_list['Code']) 
        merged_list.pop(-1)
        
        for i in range(len(merged_list)):
            if etat in merged_list[i].keys():
                if merged_list[i]['etat'] != '':
                    print(merged_list[i]['Code'],merged_list[i])
        
        # DEBOGAGE
        '''
        for i in range(len(merged_list)):
            if 'Temperature' in merged_list[i].keys():  # si le dictionnaire est bon
                # merged_list[i].pop('coordonnee')
                ecr.writerow(merged_list[i])
            else:
                coordonnee = merged_list[i]['coordonnee'].strip('][').split(', ')
                coordonnee = [float(e) for e in coordonnee]
                code = {'Code': merged_list[i]['Code'],
                        'Temperature': coordinate_temperature(coordonnee)['air_temperature'], 'etat': 'NULL'}
                ecr.writerow(code)


alocation_meteo()
