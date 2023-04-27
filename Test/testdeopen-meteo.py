import requests
import json

# Set the API endpoint URL
# Set the latitude and longitude coordinates of the location
lat = 52.52
lon = 13.4

start_date = '2021-04-01'#'AAAA-MM-JJ'
end_date = '2021-04-02'

url = f"https://archive-api.open-meteo.com/v1/era5?latitude={lat}&longitude={lon}&start_date={start_date}&end_date={end_date}&hourly=temperature_2m"


# Set the date for which you want to retrieve the weather data
date = "2003-04-24T12:00:00Z"

'''
ON PEUX AJOUTER LES PARAMETRES ICI POUR FAIRE PLUS FACILMENET
params = {
    "latitude": float(lat),
    "longitude": float(lon),
    # autres parametres
}
'''
# Make the API call and get the response
response = requests.get(url) #params=params

# Parse the JSON response
data = json.loads(response.text)

print(data)
# Extract the temperature value from the response
#temperature = data["forecast"]["temperature"]["value"]

#print(f"The temperature at {lat}, {lon} on {date} was {temperature}°C.")
