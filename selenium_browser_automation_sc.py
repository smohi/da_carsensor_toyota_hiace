from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd

import time


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

#scrapping search results with BeautifulSoup
soup = BeautifulSoup(driver.page_source,'html.parser')
car_listings = soup.find_all('div', class_='cassette') #main div is cassette or cassetteMain or cassetteWrap or cassetteMain__inner

#extracting relavant data from each listings
car_data = [] #empty list to store data

for car in car_listings:
    #extracting individual data fields
    price_tag = car.find('span', class_ = 'price') # defining car price tag
    price = price_tag.find('font').find('font').text.strip() if price_tag else None #aquiring car price
    
    #car specs listing
    spec_list = car.find('dl', class_ = 'specList') #container having the specs
    
    #empty dictionary to store specs
    car_specs = {
        'Price' : price
    }
    
    #extracting data from speclist div
    for detail_box in spec_list.find_all('div', class_='specList__detailBox'):
        label = detail_box.find('dt').text.strip()  #extract labels
        
        #extracting corresponding values for the labels
        if label == 'Year':
            year = detail_box.find('dd', class_ = 'specList__data').find('font').find('font').text.strip()
            car_specs['Year'] = year
        elif label == 'Mileage':
            mileage = detail_box.find('dd', class_='specList__data').find('font').find('font').text.strip()
            car_specs['Mileage'] = mileage + ' km'
    
    ###use similar for color###
    
    #appending data to car data list
    
    car_data.append(car_specs)
    
#converting data into DataFrame (pandas)

df = pd.DataFrame(car_data)

#cleaning and analyzing the price data (if necessary)
df['Price'] = df['Price'].replace('[\D]', '', regex=True).astype(float)  # removing non-numeric characters from price if needed
    
#displaying final dataframe

print(df)



