import requests
from bs4 import BeautifulSoup
import csv
import time

# list of links to scrape
links = ["https://www.infoclimat.fr/annuaire-webcams-meteo.html#431", "https://www.infoclimat.fr/annuaire-webcams-meteo.html#556", "https://www.infoclimat.fr/annuaire-webcams-meteo.html#611"]

# loop through links
for link in links:
    # send a GET request to the link
    response = requests.get(link)
    time.sleep(2)
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    time.sleep(2)
    # find the img tag with id 'webcam' and get its src attribute
    img_tag = soup.find('img', {'id': 'webcam'})
    img_src = img_tag['src']
    
    # save the img src to a CSV file
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([link, img_src])
