from selenium import webdriver
import time

# Launch Firefox browser
driver = webdriver.Firefox()

# Open custom map URL
driver.get("https://webcam-live.creaweather.fr/Meteo60.html")
time.sleep(5)
# Execute JavaScript to get all pins on the map
pins = driver.execute_script("return document.querySelectorAll('.gm-style-iw-d');")

# Iterate through each pin
for pin in pins:
    # Click on the pin to open the popup window
    driver.execute_script("arguments[0].click();", pin)

    # Get the link attached to the pin using JavaScript
    link = driver.execute_script("return document.querySelector('.gm-style-iw-e a').href;")
    
    # Print the link
    print(link)

    # Close the popup window
    driver.execute_script("document.querySelector('.gm-style-iw-i-c').click();")

# Close the browser
