import requests
import json

def get_department_location(department_code):
    url = f"https://wft-geo-db.p.rapidapi.com/v1/geo/countries/FR/adminDivisions?namePrefix={department_code}"

    headers = {
        "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
        "X-RapidAPI-Key": '1a424e039cmsh81347330eaafba0p1dc134jsn482b43cddb9d',
    }

    response = requests.get(url, headers=headers)
    data = json.loads(response.content.decode('utf-8'))
    print(data)

    if data["data"]:
        latitude = data["data"][0]["latitude"]
        longitude = data["data"][0]["longitude"]
        return (latitude, longitude)
    else:
        return None

print(get_department_location(30))