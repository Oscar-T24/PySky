import csv
import pandas as pd
from datetime import datetime

today = datetime.now()

f = open('coordonnees_departements.csv', 'r')
coordonnees = list(csv.DictReader(f))
def normale(cle_api, annees):
    """
    str, int --> None
    Donne les valeurs normales pour la clé API pour chaque mois dans chaque department, calculé à partir des données des annees dernieres années.
    Attention, ça prend a peu près 40min pour annees = 10
    Marche avec les cle_api suivants:
    weathercode
    temperature_2m_max
    temperature_2m_min
    apparent_temperature_max
    apparent_temperature_min
    sunrise
    sunset
    uv_index_max
    uv_index_clear_sky_max
    precipitation_sum
    rain_sum
    showers_sum
    snowfall_sum
    precipitation_hours
    precipitation_probability_max
    windspeed_10m_max
    windgusts_10m_max
    winddirection_10m_dominant
    shortwave_radiation_sum
    et0_fao_evapotranspiration
    """
    with open(f'normale_{cle_api}.csv', 'w', newline='') as n:
        normale = csv.writer(n)
        normale.writerow(["Code", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12"])
        for e in coordonnees:
            c = e['coordonnee'].split(" ")
            d, x, y = e['Code'], float(c[0][1:-2]), float(c[-1][:-2])
            print(f"Calcul de la {cle_api} moyenne par mois du département {d}")
            normales_dep = [d]
            for mois in ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]:
                normales_dep_mois = []
                for year in range(today.year - annees - 1, today.year - 1):
                    data = pd.read_json(f'https://archive-api.open-meteo.com/v1/archive?latitude={x}&longitude={y}&start_date={year}-{mois}-15&end_date={year}-{mois}-15&daily={cle_api}&timezone=Europe%2FLondon')
                    data_traite = data.values.tolist()[1][-1][0]
                    normales_dep_mois.append(data_traite)
                normales_dep.append(round(sum(normales_dep_mois)/len(normales_dep_mois), 4))
            normale.writerow(normales_dep)
