
# ************************* Part 1 *************************

# Links:
# https://www.trulia.com/CA/San_Diego/
# https://www.trulia.com/home/12360-carmel-country-rd-301-san-diego-ca-92130-65237705

# All the Cities that we are interested in:
# 1. San Diego
# 2. Albuquerque
# 3. Colorado
# 4. Philadelphia
# 5. Indianapolis
# 6. Las Vegas 
# 7. Washington
# 8. Miami
# 9. New York
# 10. San Francisco

# ------------ Imports ------------
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# ------------ Selenium Setup ------------
# Set up Chrome WebDriver
service = Service('C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Trulia_Report/ChromeDriver/chromedriver-win64/chromedriver.exe')
driver = webdriver.Chrome(service=service)

# Load the page
url = 'https://www.trulia.com/CA/San_Diego/'
driver.get(url)

# Grab the page source after rendering
page_source = driver.page_source

# Parse the rendered HTML with BeautifulSoup
soup = BeautifulSoup(page_source, 'html.parser')
print (f"Soup: {soup}")

# ------------ Results ------------
results_container = soup.find_all('li', {'class': 'Grid__CellBox-sc-144isrp-0 sc-84372ace-0 yoWOn cEFmzn'})
print(f"Results_Container: {results_container}")
print(f"Results_Container: {len(results_container)}")

# ------------ Update Results ------------
# Keep only 'li' elements with the 'data-testid' attribute
results_update = []
for r in results_container:
    if r.has_attr('data-testid'):
        results_update.append(r)
print(f"Results_Update: {len(results_update)}")
print(f"Results_Update: {results_update}")

# ------------ Concatenate 2 URL Parts to get absolute URL ------------
# URL Part 1
url_part1 = 'https://www.trulia.com'
url_part2 = []

for item in results_update:
    link_div = item.find_all('div', {'data-testid': 'property-card-details'})
    for link in link_div:
        url_part2.append(link.find('a').get('href'))

print(f'Total Links Found: {len(url_part2)}')
print(f'Total Links Found: {url_part2}')

# ------------ Clean Up Selenium ------------

# ------------ Get Data from First Link ------------
# Address
# Bedrooms
# Bathrooms
# Sqft
# Year built
# Parking
# Price

# ------------ Put all together and loop through all results on page 1 ------------

# ------------ Multiple Pages - San Diego ------------


# ************************* Part 2 *************************



# ************************* Part 3 *************************

driver.quit()