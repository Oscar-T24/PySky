
import pandas as pd
import folium
import csv
import numpy
from random import randint

# PARTIE TRANSFORMATION NOM_DEPARTEMENT --> LATITUDE, LONGITUDE 

from geopy.geocoders import Nominatim


#----------------------------------------------------------------

# RECUPERATION DE LA TEMPERATURE AVEC SES CORDONNÉES


coordonees = []

with open('coordonnees_departements.csv','r') as f:
    read = csv.DictReader(f,delimiter=',',fieldnames=['Code','departement','coordonnee'])
    for ligne in read:
        coordonees.append("".join(ligne['coordonnee']).strip('][').split(', '))

coordonees.pop(0)
for coordonnee in coordonees:
    for i in range(len(coordonnee)):
        coordonnee[i] = float(coordonnee[i])

# Load the GeoJSON file of French department boundaries
geojson_url = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
geojson_data = folium.GeoJson(geojson_url).data

# Convert the GeoJSON data to a pandas DataFrame
geojson_df = pd.json_normalize(geojson_data["features"])

# Load the dataset of temperature by department
temperature_data = pd.read_csv("tableau_finalv2.csv", dtype={"Code": str})

# Merge the dataset with the GeoJSON file using the department code as the common key
merged_data = pd.merge(geojson_df, temperature_data, left_on="properties.code", right_on="Code")

'''
list_of_dicts = merged_data.to_dict(orient='records')
print(list_of_dicts)
import time
time.sleep(5)
'''

# Create a choropleth map of the temperature
m = folium.Map(location=[46.5, 2], zoom_start=6)
# Add a layer control to the map

# bbox = [[latitudemin,longitudemin],[latitudemax,longitudemax]]
'''
folium.raster_layers.ImageOverlay(
    image='sun.png',
    bounds = [[41, 5], [45, 9]],
    opacity=1,
    overlay=True, 
    control=True,
).add_to(m)
'''
"""
folium.raster_layers.ImageOverlay(
    image='sun.png',
    bounds = [[41, 5], [45, 9]],
    opacity=1,
    name = 'Sun'
).add_to(m)
"""
from datetime import datetime

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%H:%M")
print(dt_string)

folium.Choropleth( # on instancie l'element chloropleth pour pouvoir le modifier apres sa definition
    geo_data=geojson_data,
    name=f"Temperature à {dt_string}",
    data=merged_data,
    columns=["properties.nom", "Temperature"],
    key_on="feature.properties.nom",
    fill_color="YlOrRd",
    fill_opacity=1,
    line_opacity=0.5,
    legend_name="Temperature (°C)",
    style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2},
    highlight=True,
    overlay=True,
).add_to(m)

#folium.Marker(location=[46, 6], icon=folium.Icon(icon='sun')).add_to(m)
#https://www.python-graph-gallery.com/312-add-markers-on-folium-map?utm_content=cmp-true

html=f"""
        <h1>LOL</h1>
        <p>You can use any html here! Let's do a list:</p>
        <ul>
            <li>Item 1</li>
            <li>Item 2</li>
        </ul>
        </p>
        <p>And that's a <a href="https://www.python-graph-gallery.com">link</a></p>
    """


dico_temperatures_etat = []
with open('tableau_finalv2.csv','r') as f:
    read = csv.DictReader(f,delimiter=',',fieldnames=['Code','Temperature','etat'])
    for ligne in read:
        dico_temperatures_etat.append(ligne)

for i in range(len(coordonees)):
    iframe = folium.IFrame(html=html, width=200, height=200)
    popup = folium.Popup(iframe, max_width=2650)
    try:
        weather = 'cross'
        match dico_temperatures_etat[i]['etat']:
                case 'Cloudy':
                    weather = 'cloud'
                case 'Rainy':
                    weather = 'rain'
                case 'Sunny':
                    weather = 'sun'
                case 'Foggy':
                    weather = 'fog'
        folium.Marker(
                        location=coordonees[i],
                        popup=popup,
                        icon=folium.DivIcon(html=f"""
                            <div>
                            <img src='http://93.14.22.225/{weather}.png'height='35px'width='auto'>
                            </div>"""),
            ).add_to(m)
           
    except IndexError:
        #print('pas assez de departements')
        pass

'''
# Bring the image overlay to the front
fg = folium.FeatureGroup().add_to(m)
fg.add_child(folium.LayerControl())
#m.get_name('Sun')
'''
folium.TileLayer('cartodbpositron', name='cartodbpositron').add_to(m)

folium.LayerControl().add_to(m)

# Display the map
from IPython.display import IFrame

# PARTIE RENDERING

map_html = m._repr_html_()
IFrame(width=1000, height=500, src=map_html)


from flask import Flask, render_template_string, url_for

app = Flask(__name__)

@app.route("/")
def map():
    # ... (the code that generates the map)
    # Save the map to a temporary file and get the HTML as a string
    tmp_file = "tmp_map.html"
    m.save(tmp_file)
    with open(tmp_file, "r") as f:
        map_html = f.read()
    # Generate the URL for the remote favicon
    favicon_url = "http://93.14.22.225/favicon.ico"
    # Return the HTML string with the favicon link tag
    return render_template_string(
        f"<html><head><link rel='shortcut icon' href='{favicon_url}'></head><body>{map_html}</body></html>"
    )

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0', port=4650)

m.save("temperature_map.html")

# Ajouter une interface de visualisation en direct

# ce qu'il reste à faire :  supprimer les doublons dans le csv
"""
    @app.route("/")
'''
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
    app.run(debug=True,host='0.0.0.0', port=4650)
'''
"""#aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa