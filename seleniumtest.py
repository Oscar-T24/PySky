from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv

# list of links to scrape

# set up Selenium driver

# loop through links
for identifiant in range(135,614):

    driver = webdriver.Chrome()

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
    with open('data.csv', mode='a') as file:
        writer = csv.writer(file)
        writer.writerow([link[:26]+img_src,h3_text])
