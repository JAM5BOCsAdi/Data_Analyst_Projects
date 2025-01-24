
# ************************* Part 1 *************************

# Links:
# Base URL: https://www.arukereso.hu/mobiltelefon-c3277/?orderby=2
# Second URL: https://www.arukereso.hu/mobiltelefon-c3277/samsung/galaxy-z-fold6-5g-1tb-12gb-ram-dual-sm-f956b-p1102673305/


# ------------ Imports ------------
from bs4 import BeautifulSoup
import requests
import pandas

# ------------ HTTP Request ------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}
# store website in variable
website = 'https://www.arukereso.hu/mobiltelefon-c3277/?orderby=2'
# get request
response = requests.get(website, headers=headers)
# status code
response.status_code

# ------------ Soup Object ------------
soup = BeautifulSoup(response.content,'html.parser')

print(f"Soup HTML: {soup}")


# div class="product-box-container clearfix"
# ------------ Results ------------
products = soup.find_all('div',{'class':'product-box-container clearfix'})
print(f"Results_Container: {len(products)}")
print(f"Results_Container: {products}")

# ------------ Update Results ------------

# ------------ Concatenate 2 URL Parts to get absolute URL ------------

# ------------ Get Data from First Link ------------

# ------------ Put all together and loop through all results on page 1 ------------

# ------------ Multiple Pages - San Diego ------------


# ************************* Part 2 *************************



# ************************* Part 3 *************************