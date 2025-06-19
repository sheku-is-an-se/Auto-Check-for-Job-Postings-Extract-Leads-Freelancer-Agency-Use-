# 🕸️ Extract jobs from RemoteOK HTML
# imported libaries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import time



#Set up Chromedriver
driver = webdriver.Chrome()

#Navigate to remoteok
driver.get("https://remoteok.com/")



#Locate the dropdown menu for location and click
location_button = driver.find_element(By.CSS_SELECTOR, ".location-filter-input")
time.sleep(1)
location_button.click()
time.sleep(1)
print(driver.find_element(By.TAG_NAME, "tr").get_attribute('data-offset') == '3')

'''
iframe = driver.find_element(By.TAG_NAME, "tr").get_attribute('3')
ActionChains(driver)\
    .scroll_to_element(iframe)\
    .perform()
'''
location_dropdown = driver.find_element(By.CLASS_NAME, "location-filter-results").find_elements(By.TAG_NAME, "div")

for element in location_dropdown:
    if element.text == "🌏 Worldwide":
        print('I found the US')
        element.click()
        time.sleep(3)
        break
   
    





#Locate the United STates tag





#for location in location_dropdown:
    #print(location.text)




# Locate the search box element
search_box = driver.find_element(By.CLASS_NAME, "search-filter-input")
search_box.click()
time.sleep(1)

# Type text into the search box
search_box.send_keys("Python")

#Enter Result in search box
search_box.send_keys(Keys.RETURN)
time.sleep(3)





#cRetrieve the page source
html = driver.page_source

# Parse the HTML with Beautiful Soup
soup = BeautifulSoup(html, 'lxml')

#print(soup.prettify())


#close the browser
driver.quit()


#search box element
#class="search active"
