import folium

# Create a map centered on France
m = folium.Map(location=[46.5, 2], zoom_start=6)

# Add the regions layer to the map using the provided GeoJSON file
folium.GeoJson(
    'https://france-geojson.gregoiredavid.fr/repo/regions.geojson',
name='Regions' # fonctionne avec les Regions
).add_to(m)

# Add a layer control to the map
folium.LayerControl().add_to(m)

# Save the map to an HTML file
m.save('france_regions_map.html')