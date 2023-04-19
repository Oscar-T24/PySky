from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# list of links to scrape

# set up Selenium driver

# loop through links
with open('donnees_cameras','w') as f:
    ecr = csv.DictWriter(f,delimiter=',',fieldnames=['lien', 'departement'])
    ecr.writeheader()
    ecr.writerow({'lien': 'test', 'departement': 'test'})

for identifiant in range(0,700):

    driver = webdriver.Firefox()

    link = f"https://www.infoclimat.fr/annuaire-webcams-meteo.html#{identifiant}"
    # navigate to the link
    driver.get(link)
    
    # wait for the #webcam image to load
    wait = WebDriverWait(driver, 10)
    img_element = wait.until(EC.presence_of_element_located((By.ID, 'webcam')))
    
    # parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # find the img tag with id 'webcam' and get its src attribute
    img_tag = soup.find('img', {'id': 'webcam'})
    img_src = img_tag['src']
    
    h3_tag = soup.find('h3')
    try :
        h3_text = h3_tag.text.strip()
    except AttributeError:
        h3_text = "NULL"

    # save the img src to a CSV file
    with open('donnees_cameras.csv', mode='w') as file:
        writer = csv.DictWriter(file,fieldnames=['lien','departement'])
        writer.writeheader()
        writer.writerow({'lien': link[:25]+img_src, 'departement': h3_text})

    driver.close()
