import folium
import pandas as pd
import numpy as np
import urllib.request
from PIL import Image
import csv
from random import randint
# Load the US states GeoJSON file
url = 'https://raw.githubusercontent.com/python-visualization/folium/master/examples/data'
state_geo = f'{url}/us-states.json'

noms_etats = []
with open('us-states-territories.csv','r',encoding = "ISO-8859-1")as f:
    read = csv.reader(f,delimiter=',')
    for row in read:
        noms_etats.append(row[1])


with open("temperature_data.csv","w") as f:
    ecr = csv.writer(f,delimiter=',')
    ecr.writerow(['FIPS','State','Temperature'])
    fichier = []
    for i in range(57):
        fichier.append([i,noms_etats[i],randint(0,30)])

    ecr.writerows(fichier)

import folium
import random

# create map object
m = folium.Map(location=[48, -102], zoom_start=3)

# add choropleth layer
choropleth = folium.Choropleth(
    geo_data='https://raw.githubusercontent.com/scdoshi/us-geojson/master/geojson/nation/US.geojson',
    fill_color='#'+"".join([random.choice('0123456789ABCDEF') for j in range(6)]),
    fill_opacity=0.7,
    line_opacity=0.2,
).add_to(m)

# loop through features to add sun image
for state in choropleth.geojson['features']:
    state_name = state['properties']['name']
    state_coords = state['geometry']['coordinates'][0][0]
    folium.raster_layers.ImageOverlay(
        image='sun.png',
        bounds=[(state_coords[1], state_coords[0]), (state_coords[1]+1, state_coords[0]+1)],
        opacity=0.7,
        interactive=False,
        cross_origin=False
    ).add_to(m)

# save map as html
m.save('map.html')


