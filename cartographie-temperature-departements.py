import pandas as pd
import folium
from creation_departements_temp import randomizer
import csv

# PARTIE TRANSFORMATION NOM_DEPARTEMENT --> LATITUDE, LONGITUDE 

from geopy.geocoders import Nominatim

def departement_coordinate(departement):
    # Enter the name of the department
    department_name = departement
    # Create a geolocator object
    geolocator = Nominatim(user_agent="geoapiExercises")
    # Use the geolocator to get the location of the department
    location = geolocator.geocode(f"{department_name}, France")
    # Extract the latitude and longitude from the location object
    latitude = location.latitude
    longitude = location.longitude
    return latitude,longitude

#----------------------------------------------------------------

# RECUPERATION DE LA TEMPERATURE AVEC SES CORDONNÉES

import json, requests

def coordinate_temperature(coordonees):
    """
# Dans cet exemple nous allons utiliser le service météo du Meteorologisk institutt de Norvège
# (api.met.no/weatherapi is an interface to a selection of data produced by MET Norway)
# url: https://api.met.no/weatherapi/locationforecast/2.0/documentation
#
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

    return weather['air_temperature'] # la temperature du departement

temperatures = []
'''
with open("departements-france.csv","r") as f:
    spamreader = csv.reader(f, delimiter=',')
    for row in spamreader:
        temperature = {}
        temperature["Temperature"] = coordinate_temperature(departement_coordinate(row[1]))
        temperature["Code"] = row[0]
        temperatures.append(temperature)
        #print(coordinate_temperature(departement_coordinate(row[1])),row[1])


# ecrire le dioctinnaire dans temperatures
with open('temperature_data.csv','w') as f:
    fieldnames = ['Code', 'Temperature']
    ecr = csv.DictWriter(f,delimiter=',',fieldnames=fieldnames)
    ecr.writeheader()
    for e in temperatures:
        ecr.writerow(e)

'''

# Load the GeoJSON file of French department boundaries
geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
geojson_data = folium.GeoJson(geojson_url).data

# Convert the GeoJSON data to a pandas DataFrame
geojson_df = pd.json_normalize(geojson_data["features"])

# Load the dataset of temperature by department
temperature_data = pd.read_csv("temperature_data.csv", dtype={"Code": str})

# Merge the dataset with the GeoJSON file using the department code as the common key
merged_data = pd.merge(geojson_df, temperature_data, left_on="properties.code", right_on="Code")

# Create a choropleth map of the temperature
m = folium.Map(location=[46.5, 2], zoom_start=6)
# Add a layer control to the map
bbox = [[30, 5], [35, 9]] # COORDONNÉES 
# bbox = [[latitudemin,longitudemin],[latitudemax,longitudemax]]
folium.raster_layers.ImageOverlay(
    image='sun.png',
    bounds = [[41, 5], [45, 9]],
    opacity=1,
    overlay=True, 
    control=True,
).add_to(m)
"""
folium.raster_layers.ImageOverlay(
    image='sun.png',
    bounds = [[41, 5], [45, 9]],
    opacity=1,
    name = 'Sun'
).add_to(m)
"""
folium.Choropleth(
    geo_data=geojson_data,
    name="Temperature",
    data=merged_data,
    columns=["properties.nom", "Temperature"],
    key_on="feature.properties.nom",
    fill_color="YlOrRd",
    fill_opacity=1,
    line_opacity=0.5,
    legend_name="Temperature (°C)",
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2},
).add_to(m)


'''
# Bring the image overlay to the front
fg = folium.FeatureGroup().add_to(m)
fg.add_child(folium.LayerControl())
#m.get_name('Sun')
'''
folium.LayerControl().add_to(m)

# Display the map
from IPython.display import IFrame

# PARTIE RENDERING

map_html = m._repr_html_()
IFrame(width=1000, height=500, src=map_html)

from flask import Flask, render_template_string

app = Flask(__name__)

@app.route("/")
def map():
    # ... (the code that generates the map)
    # Save the map to a temporary file and get the HTML as a string
    tmp_file = "tmp_map.html"
    m.save(tmp_file)
    with open(tmp_file, "r") as f:
        map_html = f.read()
    # Return the HTML string
    return render_template_string(map_html)

if __name__ == "__main__":
    app.run(debug=True)

m.save("temperature_map.html")

# Ajouter une interface de visualisation en direct