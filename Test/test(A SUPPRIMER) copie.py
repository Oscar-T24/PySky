
import csv
import requests
from PIL import Image
from io import BytesIO
import numpy
import json

from geopy.geocoders import Nominatim
import re

global dico_etats_meteos


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
    url = requests.get(f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}7&lon={longitude}", headers=headers)
    text = url.text

    # Get JSON data
    data = json.loads(text)
    #print(data)

    # Process JSON data
    units = data["properties"]["meta"]["units"]
    weather = data["properties"]["timeseries"][0]["data"]["instant"]["details"]  
    return weather

print(coordinate_temperature([43.88566272770907,-0.5092243304975015]))