import folium

# Define the bounding box of the department you want to add the image overlay to
bbox = [[37, 5], [41, 9]]
# UTILISÉ POUR PARAMETRER LA TAILLE DE L'IMAGE

# Create a choropleth map
m = folium.Map(location=[43.38, 5.4], zoom_start=11)

# Add the department boundary to the map as a GeoJSON layer
geojson = "https://france-geojson.gregoiredavid.fr/repo/departements.geojson"
if geojson:
    folium.GeoJson(
        geojson,
        name='Department Boundary',
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'blue', 'weight': 2}
    ).add_to(m)

# Add the image overlay to the map for the specified bounding box
from PIL import Image
image = Image.open('sun.jpg')
image.resize((4000,4000))
image.save('sun.jpg')

image = 'sun.jpg'
if image:
    folium.raster_layers.ImageOverlay(
        image=image,
        bounds=bbox,
        opacity=1,
        width=2000,
        height=2000,
    ).add_to(m)

# Add a layer control to the map so that the user can toggle the visibility of the department boundary and image overlay
folium.LayerControl().add_to(m)

# Display the map
m.save("TESTSUN.html")
