# example input data
list1 = [{'Code': '73', 'Temperature': '3.4', 'etat': 'Cloudy'}, {'Code': '84', 'Temperature': '7.2', 'etat': 'Sunny'}, {'Code': '91', 'Temperature': '12.3', 'etat': 'Rainy'}]
list2 = [{'Code': '973', 'departement': 'Guyane', 'coordonnee': '[4.0039882, -52.999998]'}, {'Code': '84', 'departement': 'Gironde', 'coordonnee': '[44.837789, -0.57918]'}, {'Code': '73', 'departement': 'Somme', 'coordonnee': '[49.96237, 2.35893]'}, {'Code': '09', 'departement': 'Ariège', 'coordonnee': '[42.9167, 1.0833]'}]

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
# create a new list of dictionaries with the desired keys/values
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

# print the result
print(merged_list)


