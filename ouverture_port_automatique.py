from time import sleep
from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep


options = ChromeOptions()
options.add_argument("--start-maximized")
chrome_driver = webdriver.Chrome(options=options)

chrome_driver.get("http://192.168.1.1")
sleep(15)

for i in range(5065,8000):

    nom_nat = f'pysky{i}'
    #chrome_driver.get("http://86.241.3.36:81/index.htm1")
    # verification :
    chrome_driver.implicitly_wait(5)

    #assert chrome_driver.title == "Device(IPCamera)", ''.format(chrome_driver.title)

    # <button id="monitor_link" type="button" onclick="javascript:btndisp()" style="height:30px; width:100px;"><script>document.write(str_signin);</script>Sign in</button>
    #login = chrome_driver.find_element(By.ID, "body")
    #login.click()


    #chrome_driver.execute("document.getElementById('main').setAttribute('src','');")
    sleep(1.5)
    nom = chrome_driver.find_element(By.ID, "nat_rulename")
    port1 = chrome_driver.find_element(By.ID, "nat_extport")
    ip = chrome_driver.find_element(By.ID, "nat_dstip_p3")
    port2 = chrome_driver.find_element(By.ID, "nat_dstport")
    submit = chrome_driver.find_element(By.NAME, "action_add")
    #submit = chrome_driver.find_element_by_name("name_attribute_value")

    nom.clear()
    port1.clear()
    port2.clear()

    nom.send_keys(nom_nat)
    port1.send_keys(str(i))
    port2.send_keys(str(i))
    ip.send_keys('72')
    submit.click()


