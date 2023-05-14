import requests

url = "https://wft-geo-db.p.rapidapi.com/v1/geo/adminDivisions/France/"

headers = {
	"X-RapidAPI-Key": "1a424e039cmsh81347330eaafba0p1dc134jsn482b43cddb9d",
	"X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers)

print(response.text)