import requests
from bs4 import BeautifulSoup
import csv

# Define the URL of the Meteofrance website that displays temperature data for each department
url = "https://www.meteofrance.com/cartes-plans/observations/releves-temperature"

# Send a GET request to the website and get the HTML content
response = requests.get(url)
html_content = response.content

# Parse the HTML content with Beautiful Soup
soup = BeautifulSoup(html_content, 'html.parser')

# Find the table that contains the temperature data for each department
table = soup.find('table', {'class': 'table-hover'})

# Get the rows of the table
rows = table.find_all('tr')

# Create a new CSV file and write the temperature data for each department to it
with open('temperatures.csv', mode='w') as file:
    writer = csv.writer(file)
    writer.writerow(['Department', 'Temperature'])

    for row in rows:
        cells = row.find_all('td')
        if len(cells) == 3:
            department = cells[0].text.strip()
            temperature = cells[2].text.strip()
            writer.writerow([department, temperature])
