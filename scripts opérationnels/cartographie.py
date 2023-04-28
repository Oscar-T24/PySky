import pandas as pd
import folium
import csv
import random
from IPython.display import IFrame
from datetime import datetime

now = datetime.now()

# PARTIE TRANSFORMATION NOM_DEPARTEMENT --> LATITUDE, LONGITUDE 

from geopy.geocoders import Nominatim

# ---------------INTERPRETATION DES DONNES ENVOYES ------------------------------

coordonees = []

with open('coordonnees_departements.csv', 'r') as c:
    read = csv.DictReader(c, delimiter=',', fieldnames=['code', 'departement', 'coordonnee'])
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
temperature_data = pd.read_csv("donnees_meteo.csv", dtype={"code": str})

# Merge the dataset with the GeoJSON file using the department code as the common key
merged_data = pd.merge(geojson_df, temperature_data, left_on="properties.code", right_on="code")

# Create a choropleth map of the temperature
m = folium.Map(location=[46.5, 2], zoom_start=6)
# Add a layer control to the map


# bbox = [[latitudemin,longitudemin],[latitudemax,longitudemax]]

# datetime object containing current date and time
now = datetime.now()
dt_string = now.strftime("%H:%M")

descripteurs = []
with open('donnees_meteo.csv', 'r') as f:
    descripteurs = list(csv.reader(f, delimiter=','))[0]  # la ligne 0 correspond aux descripteurs
    #descripteurs = [e for e in descripteurs if e != 'code' and e != 'Date' and e !='Air_quality (pm2.5)' and e != 'Etat_meteo' and e != 'Indice']  # on n'exploite pas ces données visuelles

descripteurs = ['Temperature (°C)','Humidite_relative (%)','Temperature_ressentie (°C)','Probabilite_pluie (%)','Precipitation (mm)','Pression (0m)(hPa)','Couverture_nuageuse (%)','Visibility (m)','Vitesse_vent (km/h)','Index_UV','River_discharge (m3/s)','Probabilité sècheresse','Probabilité innondation']
# on modifie expressement les descripteurs pour n'inclure que ceux qu'on veux mettre en cloropleth
for donnee in descripteurs:
    a = folium.Choropleth(  # premier cloropleth pour la temperature
        geo_data=geojson_data,
        name=f"{donnee} à {dt_string}",
        data=merged_data,
        columns=["properties.nom", f"{donnee}"],
        key_on="feature.properties.nom",

        # CODE COULEUR 

        # "YlOrRd" : temperatures + ressenti
        # 'BuPu' : humidite + % pluie + precipitation 
        #  'GnRd' : air_quality + UV index (PRGn si ca marche pas)
        # 'RdBu' : pression + couverture nuageuse
        # 'Greys' : visibilité + vitesse vent 
        # 'Blues' : River discharge + pbilité inondation
        # 'RdGy' : pbilité secheresse
        # 'Reds' : cancicule

        fill_color= random.choice(["YlOrRd", "PuBuGn", "YlGnBu", "PuBu"]),  # ColorBrewer code A CHANGER
        # https://colorbrewer2.org/#type=sequential&scheme=PuBuGn&n=3
        fill_opacity=1,
        line_opacity=0.5,
        legend_name=f"{donnee}",
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2},
        highlight=True,
        show=False,
        overlay=True,
    )
    # SUPPRIMER LES LEGENDES
    for key in a._children:
        if key.startswith('color_map'):
            del(a._children[key])      
    a.add_to(m)

# folium.Marker(location=[46, 6], icon=folium.Icon(icon='sun')).add_to(m)
# https://www.python-graph-gallery.com/312-add-markers-on-folium-map?utm_content=cmp-true

# Les descripteurs du tableau_finalv2 sont repertoriés ici. Stv en ajouter d'autres modifie KNN_meteo pour les enregistrer dans le tableau à la fin

f = open('donnees_meteo.csv', 'r')
descripteurs = list(csv.reader(f, delimiter=','))[0]
f = open('donnees_meteo.csv', 'r')
meteo = list(csv.DictReader(f, delimiter=','))

df = pd.read_csv('coordonnees_departements.csv')
departements = [(df[df.columns[0]].tolist()[i], df[df.columns[1]].tolist()[i]) for i in range(len(df[df.columns[1]].tolist()))]

for i in range(len(coordonees)):
    try:
        html = f"""
        <h1>{departements[i][0]} - {departements[i][1]}</h1>
        <p>Voici les données météo pour ce département:</p>
        <ul>
            <li>Date: {meteo[i]["Date"]}</li>
            <li>Temperature: {meteo[i]["Temperature (°C)"]}°C</li>
            <li>Humidité relative: {meteo[i]["Humidite_relative (%)"]}%</li>
            <li>Temperature (ressentie): {meteo[i]["Temperature_ressentie (°C)"]}°C</li>
            <li>Probabilité qu'il pleuve: {meteo[i]["Probabilite_pluie (%)"]}%</li>
            <li>Precipitation: {meteo[i]["Precipitation (mm)"]} mm</li>
            <li>Pression à 0m: {meteo[i]["Pression (0m)(hPa)"]} hPa</li>
            <li>Couverture nuageuse: {meteo[i]["Couverture_nuageuse (%)"]}%</li>
            <li>Visibilité: {meteo[i]["Visibility (m)"]} m</li>
            <li>Vitesse du vent (0m): {meteo[i]["Vitesse_vent (km/h)"]} km/h</li>
            <li>Index UV: {meteo[i]["Index_UV"]}</li>
            <li>Qualité de l'aire: {meteo[i]["Air_quality (pm2.5)"]} (PM 2.5)</li>
            <li>Débit moyen des rivières: {meteo[i]["River_discharge (m3/s)"]} m^3/s</li>
            <li>Probabilité de sècheresse: {meteo[i]["Probabilité sècheresse"]}</li>
            <li>Canicule: {meteo[i]["Probabilité canicule (%)"]}</li>
            <li>Probablité innondation: {meteo[i]["Probabilité innondation"]}</li>
            <li>Météo: {meteo[i]["Etat_meteo"]}</li>
        </ul>
        """
    except IndexError:
        print(f'les données recherchées ne coprrepsondent pas à celles de donnees_meteo.csv {departements[i][0]} - {departements[i][1]} \n ou il manque les DOM-TOM dans donneees_meteo.csv (script preparation_dataset_a_trier.py mal executé)')
        html = f"""
            <p>Reessayer</p>
        """
    iframe = folium.IFrame(html=html, width=300, height=300)
    popup = folium.Popup(iframe, max_width=2650)
    try:
        weather = 'circle'
        match meteo[i]['Etat_meteo']:
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
            case "NULL":
                weather = "cross"
                # ALTERNATIVEMENT : JUSTE UTILISER weather = dico_meteo[i]['etat'].lower()
        '''
        if weather == 'circle':
            icone = folium.DivIcon(html=f"""
                             <svg height="100" width="100">
                                <circle cx="50" cy="50" r="40" stroke="black" stroke-width="3" fill="black" />
                            </svg> """),
        else:
            icone = folium.DivIcon(html=f"""
                            <div>
                            <img src='http://93.14.22.225/{weather}.png'height='35px'width='auto'>
                            </div>"""),
        '''
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

html = f'<h2 style="position:absolute;top:10px;left:50%;transform:translateX(-50%);background-color:white;padding:5px;border:1px solid black;z-index:1000;">Temps de la carte: {meteo[0]["Date"]}</h2>'
m.get_root().html.add_child(folium.Element(html))
'''
# Bring the image overlay to the front
fg = folium.FeatureGroup().add_to(m)
fg.add_child(folium.LayerControl())
#m.get_name('Sun')
'''
folium.TileLayer('cartodbpositron', name='carte simplifiee').add_to(m)

layer_control = folium.LayerControl(position='topright', collapsed=True)
m.add_child(layer_control)
 


'''
folium.LayerControl(
    collapsed=True,
).add_to(m)  # ajouter le panneau de controle
'''
# Display the map


# PARTIE RENDERING

map_html = m._repr_html_()
IFrame(width=1000, height=500, src=map_html)
'''
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
'''
m.save("templates/map.html")

print('ecriture reussie')

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
