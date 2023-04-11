import pandas as pd
import geopandas as gpd
import folium

# Step 1: Collect data
df = pd.read_csv('FD_csv_EEC20.csv')

# Step 2: Prepare the data
df = df.dropna()
df = df.astype({'Department': str, 'Employment Rate': float})

# Step 3: Geocode the data
geocode = gpd.tools.geocode(df['Region'], provider='nominatim', user_agent='my_application')
df = pd.concat([df, geocode], axis=1)

# Step 4: Create a map
m = folium.Map(location=[46.5, 2], zoom_start=6)
folium.Choropleth(
    geo_data='https://france-geojson.gregoiredavid.fr/repo/regions.geojson',
    name='choropleth',
    data=df,
    columns=['Departement', 'Employment Rate'],
    key_on='feature.properties.code',
    fill_color='YlGn',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Employment Rate (%)'
).add_to(m)
folium.LayerControl().add_to(m)
m.save('employment_rate_map.html')