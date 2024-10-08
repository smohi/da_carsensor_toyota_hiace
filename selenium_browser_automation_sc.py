from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

#initializing webdriver using chromedriver to download automatically download if not available
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))   

#going to the target website homepage to initiate search
url = "https://www.carsensor.net/"
driver.get(url) #opens chrome browser window

#finding the searchbox
search_box = driver.find_element(By.NAME, 'KW') #in carsensor's search box, serchbox input field name is 'KW'

#inputting search text
search_box.send_keys("トヨタ ハイエース") #searching for toyota hiace 

search_box.submit()

