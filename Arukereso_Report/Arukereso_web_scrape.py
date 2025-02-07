from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7',
    'Connection': 'keep-alive'
}

base_url = 'https://www.arukereso.hu/mobiltelefon-c3277/?orderby=2'

def scrape_page(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    products = soup.find_all('div', class_='product-box-container clearfix')
    button_links = []
    
    for product in products:
        buttons = product.find_all('a', class_=lambda x: x and ('button-orange' in x or 'button-blue' in x))
        for button in buttons:
            href = button.get('href')
            if href:
                if not href.startswith('http'):
                    href = f'https://www.arukereso.hu{href}' if href.startswith('/') else href
                if 'button-orange' in button.get('class', []):
                    href += '#termek-leiras'
                button_links.append(href)
    
    return button_links

def get_total_pages():
    response = requests.get(base_url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch total pages.")
        return 1
    
    soup = BeautifulSoup(response.content, 'html.parser')
    pagination_div = soup.find('div', class_='pagination hidden-xs')
    if not pagination_div:
        return 1
    
    # Extract total pages from pagination text
    pagination_text = pagination_div.find('p')
    if pagination_text:
        try:
            total_pages = int(pagination_text.get_text(strip=True).split('/')[-1])
            return total_pages
        except:
            pass
    
    # Fallback to page links
    page_links = pagination_div.find_all('a')
    max_page = 1
    for link in page_links:
        text = link.get_text(strip=True)
        if text.isdigit():
            max_page = max(max_page, int(text))
    return max_page

def scrape_product_specs(url):
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return {}
    
    soup = BeautifulSoup(response.content, 'html.parser')
    specs_table = soup.find('table', class_='property-sheet')
    if not specs_table:
        return {}
    
    specs = {}
    for row in specs_table.find_all('tr'):
        if 'property-title' in row.get('class', []):
            continue  # Skip header rows
        
        name = row.find('td', class_='property-name')
        value = row.find('td', class_='property-value')
        if name and value:
            specs[name.get_text(strip=True)] = value.get_text(strip=True)
    
    return specs

# Scrape all pages
total_pages = get_total_pages()
all_links = []

for page in range(1, total_pages + 1):
    if page == 1:
        url = base_url
    else:
        start = (page - 1) * 25
        url = f"{base_url}&start={start}"
    print(f"Scraping page {page}: {url}")
    all_links.extend(scrape_page(url))
    time.sleep(1)

# Scrape product specifications
all_specs = []
for link in all_links:
    if '#termek-leiras' in link:
        print(f"Scraping product specs: {link}")
        specs = scrape_product_specs(link)
        if specs:
            specs['URL'] = link
            all_specs.append(specs)
        time.sleep(1)

# Save to CSV
df = pd.DataFrame(all_specs)
df.to_csv('C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Arukereso_Report/scraped_products.csv', index=False, encoding='utf-8-sig')
print(f"Scraped {len(all_specs)} product specifications. Saved to scraped_products.csv")