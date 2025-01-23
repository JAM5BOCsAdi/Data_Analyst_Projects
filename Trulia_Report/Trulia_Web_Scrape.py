
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
import requests
import pandas

# ------------ HTTP Request ------------
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
}
# store website in variable
website = 'https://www.trulia.com/CA/San_Diego/'
# get request
response = requests.get(website, headers=headers)
# status code
response.status_code

# ------------ Soup Object ------------
soup = BeautifulSoup(response.content,'html.parser')
soup

print(f"Soup HTML: {soup}")

# ------------ Results ------------
results_container = soup.find_all('li',{'class':'Grid__CellBox-sc-144isrp-0 sc-84372ace-0 yoWOn cEFmzn'})
print(f"Results_Container: {len(results_container)}")
print(f"Results_Container: {results_container}")

# ------------ Update Results ------------
# Get rid of unnecessary "li" elements that are hidden.
# So in other words, just keep the 'data-testid' attributes
results_update =[]
for r in results_container:
    if r.has_attr('data-testid'):
        results_update.append(r)
print(f"Results_Update: {len(results_update)}")
print(f"Results Update: {results_update}")

# ------------ Concatenate 2 URL Parts to get absolute URL ------------
# URL Part 1
# We combine URL Part 1 with URL part 2, in order to get the absolute URL
url_part1 = 'https://www.trulia.com'
url_part2 = []

for item in results_update:
    link_div = item.find_all('div',{'data-testid':'property-card-details'})
    print(f'link_div: {link_div}')
    print(f'Len of link_div: {len(link_div)}')
    for link in link_div:
        url_part2.append(link.find('a').get('href'))
print(f'Url Part 2:\n{url_part2}')
print(f'Len of Url Part 2: {len(url_part2)}')

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