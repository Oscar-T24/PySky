import csv
import re
from geopy.geocoders import Nominatim

def get_department(commune_name):
    geolocator = Nominatim(user_agent="my-app")
    #commune_name = commune_name.encode('ISO 8859-1').decode('utf-8')
    print(commune_name)
    if 'Paris' in commune_name:  # on sait pas pk ca marche pas avec Paris (renbvoi 13 mais c Marseille ca)
        return '75'
    location = geolocator.geocode(commune_name + ", France")
    if location:
        return "".join(re.findall(r'-?\d+', location.raw['display_name']))[:2]
    else:
        return None

cameras_update = []
with open('donnees_cameras.csv','r') as f:
    cameras = list(csv.DictReader(f,delimiter=','))
for camera in cameras:
    departement = camera['departement']
    #print(camera)
    if departement != 'NULL' and departement != None:
        try :
            if type(departement) == int:
                no_departement = departement
            else:
                no_departement =  re.findall(r'\d+', departement[departement.index('de'):])
        except ValueError:
                    # nunméro pas présent quand on cherche le site web 
            if 'de' not in departement:
                continue
            no_departement = get_department(departement[departement.index('de') + 2:departement.index('(')])
        if no_departement == []:
            continue # si geopy n'a pas pu trouver le numéro
        try :
            departement = {'lien': camera['lien'], 'departement': "".join(no_departement)}
        except TypeError:
            departement = {'lien': camera['lien'], 'departement': str(no_departement)}
        if departement['departement'] != 'NULL' and 'webcam_error.png' not in camera['lien']:
            cameras_update.append(departement)

with open('donnees_camerasv2.csv', mode='w') as file:
            writer = csv.DictWriter(file,fieldnames=['lien','departement'])
            writer.writeheader()
            writer.writerows(cameras_update)