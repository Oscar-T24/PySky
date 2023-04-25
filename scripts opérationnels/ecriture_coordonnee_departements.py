import csv

from geopy.geocoders import Nominatim

coordonees = []


def departement_coordinate(departement):
    # Enter the name of the department
    # print(departement.encode('ISO 8859-1').decode('utf-8'))#.encode('ISO 8859-1')
    department_name = departement.encode('ISO 8859-1').decode('utf-8')
    # Create a geolocator object
    geolocator = Nominatim(user_agent="geoapiExercises")
    # Use the geolocator to get the location of the department
    location = geolocator.geocode(f"{department_name}, France")
    # Extract the latitude and longitude from the location object
    latitude = location.latitude
    longitude = location.longitude
    return latitude, longitude


with open('departements-france.csv', 'r') as f:
    read = csv.DictReader(f, delimiter=',',
                          fieldnames=['code_departement', 'nom_departement', 'code_region', 'nom_region'])
    for ligne in read:
        if ligne != 'nom_departement':
            coordonees.append({'Code': ligne['code_departement'], 'departement': ligne['nom_departement'],
                               'coordonnee': list(
                                   departement_coordinate(ligne['nom_departement']))})  # .encode('utf-8')

with open('coordonnees_departements.csv', 'w') as f:
    ecr = csv.DictWriter(f, delimiter=',', fieldnames=['Code', 'departement', 'coordonnee'])
    ecr.writeheader()
    ecr.writerows(coordonees)
