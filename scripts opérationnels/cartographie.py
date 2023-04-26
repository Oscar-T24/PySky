import pandas as pd
import folium
import csv
import random
from IPython.display import IFrame
from datetime import datetime
from flask import Flask, render_template_string

# PARTIE TRANSFORMATION NOM_DEPARTEMENT --> LATITUDE, LONGITUDE 

from geopy.geocoders import Nominatim

# ----------------------------------------------------------------

# RECUPERATION DE LA TEMPERATURE AVEC SES CORDONNÉES


coordonees = []

with open('coordonnees_departements.csv', 'r') as c:
    read = csv.DictReader(c, delimiter=',', fieldnames=['Code', 'departement', 'coordonnee'])
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

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%H:%M")
print(dt_string)

descripteurs = []
with open('tableau_finalv2.csv', 'r') as f:
    descripteurs = list(csv.reader(f, delimiter=','))[0]  # la ligne 0 correspond aux descripteurs

dico_temperatures_etat = []
with open('tableau_finalv2.csv', 'r') as f:
    read = csv.DictReader(f, delimiter=',', fieldnames=descripteurs)
    # print(list(read)[0])
    for ligne in read:
        dico_temperatures_etat.append(ligne)
descripteurs = [e for e in descripteurs if e != 'Code' and e != 'etat']  # on n'exploite pas ces données visuelles
# print(dico_temperatures_etat)
for donnee in descripteurs:
    folium.Choropleth(  # premier cloropleth pour la temperature
        geo_data=geojson_data,
        name=f"{donnee} à {dt_string}",
        data=merged_data,
        columns=["properties.nom", f"{donnee}"],
        key_on="feature.properties.nom",
        fill_color=random.choice(["YlOrRd", "PuBuGn", "YlGnBu", "PuBu", "PuBu"]),  # ColorBrewer code
        # https://colorbrewer2.org/#type=sequential&scheme=PuBuGn&n=3
        fill_opacity=1,
        line_opacity=0.5,
        legend_name=f"{donnee}UNITÉ ICI",
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2},
        highlight=True,
        show=False,
        overlay=True,
    ).add_to(m)

# folium.Marker(location=[46, 6], icon=folium.Icon(icon='sun')).add_to(m)
# https://www.python-graph-gallery.com/312-add-markers-on-folium-map?utm_content=cmp-true
with open('tableau_finalv2.csv', 'r') as f:
    descripteurs = list(csv.reader(f, delimiter=','))[0]

# Les descripteurs du tableau_finalv2 sont repertoriés ici. Stv en ajouter d'autres modifie KNN_meteo pour les enregistrer dans le tableau à la fin

f = open('tableau_finalv2.csv', 'r')
meteo = list(csv.DictReader(f, delimiter=','))

df = pd.read_csv('departements-france.csv')
departements = df[df.columns[1]].tolist()

for i in range(len(coordonees)):
    try: 
        html = f"""
            <h1>{i} - {departements[i]}</h1>
            <p>Voici les données météo pour ce département:</p>
            <ul>
                <li>Temperature: {meteo[i]["Temperature"]}°C</li>
                <li>Etat: {meteo[i]["etat"]}</li>
                <li>Qualité de l'air: {meteo[i]["air_quality (pm2.5)"]} (pm2.5)</li>
                <li>Débit moyen des rivières: {meteo[i]["river_discharge (m3/s)"]} (m^3/s)</li>
                <li>Probabilité pluie: {meteo[i]["probabilite_pluie (%)"]} (%)</li>
                <li>Précipitation: {meteo[i]["precipitation (mm)"]} (mm)</li>
                <li>Pression atmosphérique: {meteo[i]["pression (hPa)"]} (hPa)</li>
                <li>Couverture nuageuse: {meteo[i]["couverture_nuageuse (%)"]} (%)</li>
                <li>Visibilité: {meteo[i]["visibility (m)"]} (m)</li>
                <li>Vitesse du vent (10m): {meteo[i]["vitesse_vent (km/h)"]} (km/h)</li>
                <li>Index UV: {meteo[i]["index_ux"]}</li>
            </ul>
        """
    except KeyError:
        print('les données recherchées ne coprrepsondent pas à celles de tableau_finalv2.csv ')
        html = f"""
            <p>test</p>
        """
    iframe = folium.IFrame(html=html, width=300, height=350)
    popup = folium.Popup(iframe, max_width=2650)
    try:
        weather = 'cross'
        match dico_temperatures_etat[i + 1]['etat']:
            case 'Cloudy':
                weather = 'cloud'
            case 'Rainy':
                weather = 'rain'
            case 'Sunny':
                weather = 'sun'
            case 'Foggy':
                weather = 'fog'
            case 'Night':
                weather = 'night'
                # ALTERNATIVEMENT : JUSTE UTILISER weather = dico_temperatures_etat[i]['etat'].lower()
        folium.Marker(
            location=coordonees[i],
            popup=popup,
            icon=folium.DivIcon(html=f"""
                            <div>
                            <img src='http://93.14.22.225/{weather}.png'height='35px'width='auto'>
                            </div>"""),
        ).add_to(m)

    except IndexError:
        print('les données du tableau tableau_finalv2.csv et celles de coordonnées_departements ne correspondent pas')
        pass

'''
# Bring the image overlay to the front
fg = folium.FeatureGroup().add_to(m)
fg.add_child(folium.LayerControl())
#m.get_name('Sun')
'''
folium.TileLayer('cartodbpositron', name='carte simplifiee').add_to(m)

folium.LayerControl().add_to(m)  # ajouter le panneau de controle

# Display the map


# PARTIE RENDERING

map_html = m._repr_html_()
IFrame(width=1000, height=500, src=map_html)



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
    app.run(debug=True, host='0.0.0.0', port=4650)

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
"""  #
