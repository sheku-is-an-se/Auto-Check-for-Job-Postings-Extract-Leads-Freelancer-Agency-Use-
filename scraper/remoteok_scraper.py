# 🕸️ Extract jobs from RemoteOK HTML
# imported libaries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
import time



#Set up Chromedriver
driver = webdriver.Chrome()

#atempt to put browser in full screen
driver.maximize_window()

#Navigate to remoteok
driver.get("https://remoteok.com/")

#Scroll to element
iframe = driver.find_element(By.CLASS_NAME, "box")
scroll_origin = ScrollOrigin.from_element(iframe)
ActionChains(driver)\
    .scroll_from_origin(scroll_origin, 0, 300)\
    .perform()




#Locate the dropdown menu for location and click
location_button = driver.find_element(By.CSS_SELECTOR, ".location-filter-input")
time.sleep(1)
location_button.click()
time.sleep(1)
print(driver.find_element(By.TAG_NAME, "tr").get_attribute('data-offset') == '3')


location_dropdown = driver.find_element(By.CLASS_NAME, "location-filter-results").find_elements(By.TAG_NAME, "div")

for element in location_dropdown:
    if element.text == "🇺🇸 United States":
        print('I found the US')
        element.click()
        time.sleep(1)
        break
   



# Locate the search box element
search_box = driver.find_element(By.CLASS_NAME, "search-filter-input")
search_box.click()
time.sleep(1)

# Type text into the search box
search_box.send_keys("Python")

#Enter Result in search box
search_box.send_keys(Keys.RETURN)
time.sleep(1)

#Salary( MINIMUM )
#Change the number (0-100)k
salary_min_box = driver.find_element(By.CLASS_NAME, "salary-filter")
salary_min_box.click()

#click and hold slider to 50
clickable = driver.find_element(By.CLASS_NAME, "salary-filter-input")
ActionChains(driver) \
        .click(clickable) \
        .perform()
time.sleep(1)

#UNCOMMENT AND REPLACE CLICK AND HOLD SLIDER TO 50. THE PLACEHOLDER IS FOR TESTING PURPOSED AS THE MOMEMNT
'''
draggable = driver.find_element(By.ID, "draggable")
start = draggable.location
finish = driver.find_element(By.ID, "droppable").location
ActionChains(driver) \
    .drag_and_drop_by_offset(draggable, finish['x'] - start['x'], finish['y'] - start['y']) \
    .perform()
'''


#Retrieve the page source
html = driver.page_source

# Parse the HTML with Beautiful Soup
soup = BeautifulSoup(html, 'lxml')

soupdata = print(soup.prettify())

#---------------------------------------
##############USER DRIVER SEAT############
##############UNCOMMENT TO SET PREFERENCES(OPTIONAL)###############
#---------------------------------------

#close the browser
driver.quit()


#I need to click and hold the slider from left to right and pick what salary i want. after that, i'll create an easy to use dictionary holding the values of the slider from 0-25; I cvould just use javascript but this is a python project and im not too proficient in javascript anyways