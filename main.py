from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import time
import os

from gpt import generateItemAssessment

# Pulls firefox profile so you can keep login data for accounts
profilePath = os.getenv("FIREFOX_PROFILE")

if not profilePath:
    raise ValueError("Environment variable is not set!")

profile = FirefoxProfile(profilePath)
options = Options()
options.profile = profile

driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

# TODO: MAKE URL DYNAMIC VIA EXTENTION?
# Sets URL to the website
url = ""

if not url:
    raise ValueError("The URL variable must be assigned a string!")

driver.get(url)

wait = WebDriverWait(driver, 5)

# This will allow you to use the login form if no browser profile is set above.
# You can either implement a loop for multiple logins or modify the "send_keys" values to support a single login.
'''
# Selector for the email login field
emailField = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w."
                                                                        "x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb."
                                                                        "x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3[type='text']")))

# Selector for the password field
passwordField = wait.until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "input.x1i10hfl.xggy1nq.x1s07b3s.x1kdt53j.x1a2a7pz.xjbqb8w."
                                                                        "x1ejq31n.xd10rxx.x1sy0etr.x17r0tee.x9f619.xzsf02u.x1uxerd5.x1fcty0u.x132q4wb."
                                                                        "x1a8lsjc.x1pi30zi.x1swvt13.x9desvi.xh8yej3[type='password']")))

# 48 - 57 is the series that enters the actual information
emailField.send_keys("email")

time.sleep(2)

passwordField.send_keys("password")

time.sleep(2)

loginButton = driver.find_element(By.CSS_SELECTOR, 'div[aria-label="Accessible login button"]')
loginButton.click()
'''
# Selectors are stored in a variable for the item information
priceDivs = ".x193iq5w.xeuugli.x13faqbe.x1vvkbs.x1xmvt09.x1lliihq.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.xudqn12.x676frb.x1lkfr7t.x1lbecb7.xk50ysn.xzsf02u"
itemDescriptionDivs = ".xz9dl7a.x4uap5.xsag5q8.xkhd6sd.x126k92a"

# When selectors meet the EC the variables below will be assigned the information
targetPriceDivs = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, priceDivs)))
targetItemDescriptionDivs = wait.until(expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, itemDescriptionDivs)))

# Simple for loop that strips the text for only the information we need
for priceDiv, itemDiscDiv in zip(targetPriceDivs, targetItemDescriptionDivs):
    price = priceDiv.text.strip()
    description = itemDiscDiv.text.strip()
    
    # Calls the function in gpt.py for the actual response back
    gptResponse = generateItemAssessment(price, description)

    # Debugging
    print("Price:", price)
    print("Description:", description)
    print(gptResponse)

# Close the driver (closes the browser window)
driver.quit()
