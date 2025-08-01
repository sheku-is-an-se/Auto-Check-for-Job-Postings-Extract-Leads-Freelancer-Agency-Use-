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
    .scroll_from_origin(scroll_origin, 0, 500)\
    .perform()
time.sleep(1)



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

#Salary SLIDER (Make sure to delete the salary code below to set your salary preferences)
salary_min_box = driver.find_element(By.CLASS_NAME, "salary-filter")
salary_min_box.click()
time.sleep(1)

'''
clickable = driver.find_element(By.CLASS_NAME, "salary-filter-input")
ActionChains(driver) \
        .click(clickable) \
        .perform()
time.sleep(1)
'''
draggable = driver.find_element(By.CLASS_NAME, "salary-filter-input")
actions = ActionChains(driver) 
actions.drag_and_drop_by_offset(draggable,-20, 0).perform()
time.sleep(3)
#------------------------------------------
#---------------------------------------
##############USER DRIVER SEAT############
##############UNCOMMENT TO SET SALARY PREFERENCES(OPTIONAL)###############
'''
#Click salary button
salary_min_box = driver.find_element(By.CLASS_NAME, "salary-filter")
salary_min_box.click()

slider_ranging_down_from_middle= {
    120000: 0,
    110000: -10,
    100000: -20,
    90000: -30,
    80000: -40,
    70000: -50,
    60000: -60,
    50000: -70,
    40000: -80,
    30000: -90,
    20000: -100,
    10000: -110,
    0: -120
}
slider_ranging_up_from_middle = {
    120000: 0,
    140000: 10,
    150000: 20,
    160000: 30,
    170000: 40,
    180000: 50,
    200000: 60,
    210000: 70,
    220000: 80,
    230000: 90,
    240000: 100,
    250000: 120
}


#From 0-250000, please input the salary you want to set the slider to

def set_slider_value(value):
    if value in slider_ranging_up_from_middle:
        slider_value = slider_ranging_up_from_middle[value]
    elif value in slider_ranging_down_from_middle:
        slider_value = slider_ranging_down_from_middle[value]
    else:
        raise ValueError("You did not choose a number between 0-250000")
    return slider_value

slider_value = set_slider_value() #Change this value to set the slider to your desired salary
    
draggable = driver.find_element(By.CLASS_NAME, "salary-filter-input")
actions = ActionChains(driver) 
actions.drag_and_drop_by_offset(draggable,slider_value, 0).perform()
time.sleep(3)
'''
    
#Retrieve the page source
html = driver.page_source

# Parse the HTML with Beautiful Soup
soup = BeautifulSoup(html, 'lxml')

soupdata = print(soup.prettify())


#close the browser
driver.quit()


#I need to click and hold the slider from left to right and pick what salary i want. after that, i'll create an easy to use dictionary holding the values of the slider from 0-25; I cvould just use javascript but this is a python project and im not too proficient in javascript anyways
#Requirements
#simulate a click, hold and drag slider
#move it to my preferences and save
#save values and  compartmentalize