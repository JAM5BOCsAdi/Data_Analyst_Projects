from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Setup Chrome driver
service = Service('C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Trulia_Report/ChromeDriver/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("accept-language=en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7")
options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=options)

# Load the page
url = 'https://www.trulia.com/CA/San_Diego/'
driver.get(url)

# Wait for the page to load (use a specific CSS selector for property listings)
try:
    WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'li[data-testid="property-card"]'))
    )
    print("Page has loaded successfully.")
except Exception as e:
    print(f"Error occurred: {e}")

# Grab the page source 
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# Extract property links
results = soup.find_all('li', {'class': 'Grid__CellBox-sc-144isrp-0 sc-84372ace-0 yoWOn cEFmzn', 'data-testid': True})
property_links = ['https://www.trulia.com' + item.find('a')['href'] for item in results if item.find('a')]

# Print the results
print(f"Total Listings Found: {len(results)}")
print(f"Total Property Links: {len(property_links)}")
print(property_links)

driver.quit()
