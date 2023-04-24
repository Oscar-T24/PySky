import pandas as pd
import folium
from creation_departements_temp import randomizer

randomizer()

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
folium.Choropleth(
    geo_data=geojson_data,
    name="Temperature",
    data=merged_data,
    columns=["properties.nom", "Temperature"],
    key_on="feature.properties.nom",
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Temperature (°C)",
).add_to(m)

# Add a layer control to the map
folium.LayerControl().add_to(m)

# Display the map

m.save("temperature_map.html")
