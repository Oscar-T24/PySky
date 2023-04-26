from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import csv
import re
from geopy.geocoders import Nominatim

# list of links to scrape

# set up Selenium driver

# loop through links
'''
with open('donnees_cameras','w') as f:
    ecr = csv.DictWriter(f,delimiter=',',fieldnames=['lien', 'departement'])
    ecr.writeheader()
    ecr.writerow({'lien': 'test', 'departement': 'test'})
'''
def get_department(commune_name):
    geolocator = Nominatim(user_agent="my-app")
    #commune_name = commune_name.encode('ISO 8859-1').decode('utf-8')
    print(commune_name)
    if 'Paris' in commune_name:  # on sait pas pk ca marche pas avec Paris (renbvoi 13 mais c Marseille ca)
        return '75'
    location = geolocator.geocode(commune_name + ", France")
    if location:
        return "".join(re.findall(r'-?\d+', location.raw['display_name']))[:2]
    else:
        return None

cameras = []
for identifiant in range(0,700):

    driver = webdriver.Firefox()

    link = f"https://www.infoclimat.fr/annuaire-webcams-meteo.html#{identifiant}"
    # navigate to the link
    driver.get(link)
    
    # wait for the #webcam image to load
    wait = WebDriverWait(driver, 10)
    img_element = wait.until(ec.presence_of_element_located((By.ID, 'webcam')))
    
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # find the img tag with id 'webcam' and get its src attribute
    img_tag = soup.find('img', {'id': 'webcam'})
    img_src = img_tag['src']
    
    h3_tag = soup.find('h3')
    global no_departement
    no_departement = ''
    try :
        h3_text = h3_tag.text.strip()
        try :
            no_departement =  re.findall(r'\d+', h3_text[h3_text.index('de'):])
        except ValueError:
            # nunméro pas présent
            no_departement = get_department(h3_text[h3_text.index('de') + 2:h3_text.index('(')])
    except AttributeError:
        h3_text = "NULL"
    
    departement = {'lien': link[:25]+img_src, 'departement': no_departement}
    if departement['department'] != '':
        cameras.append(departement)
    print('ajout de ',{'lien': link[:25]+img_src, 'departement': no_departement})
    driver.close()
    # save the img src to a CSV file
with open('donnees_cameras.csv', mode='w') as file:
        writer = csv.DictWriter(file,fieldnames=['lien','departement'])
        writer.writeheader()
        writer.writerows(cameras)

