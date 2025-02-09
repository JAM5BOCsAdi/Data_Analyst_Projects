import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7',
    'Connection': 'keep-alive'
}
BASE_URL = 'https://www.rejoy.hu'

def get_last_page(soup):
    try:
        pagination = soup.select('nav[aria-label="pagination"] li')
        pages = [int(li.find('span').text) for li in pagination if li.find('span') and li.find('span').text.isdigit()]
        return max(pages) if pages else 1
    except Exception as e:
        print(f"⚠️ Warning: Failed to extract last page number - {e}")
        return 1

def extract_data(item, category):
    try:
        link_tag = item.find('a', href=True)
        link = f"{BASE_URL}{link_tag['href']}" if link_tag else ''

        title_spans = item.select('[data-cy="phone-title"] span')
        title = title_spans[0].text.strip() if len(title_spans) > 0 else ''
        title2 = title_spans[1].text.strip() if len(title_spans) > 1 else ''
        title2_parts = [part.strip() for part in title2.split(',')]

        if category == 'Okosórák':
            # Process title to remove year
            title = re.sub(r'\s*\d{4}$', '', title).strip()
            
            # Split title2 parts
            connectivity = title2_parts[0] if len(title2_parts) > 0 else ''
            color_size_part = title2_parts[1] if len(title2_parts) > 1 else ''
            status = title2_parts[2] if len(title2_parts) > 2 else ''
            
            # Determine GPS and Cellular
            gps = 'Yes' if 'GPS' in connectivity else 'No'
            cellular = 'Yes' if 'Cellular' in connectivity else 'No'
            
            # Extract size and color
            size_match = re.search(r'(\d{2})mm', color_size_part)
            size = int(size_match.group(1)) if size_match else None  # Convert size to integer (mm)
            color = re.sub(r'\s*\d{2}mm', '', color_size_part).strip()
            
            # Process price
            price_div = item.find('span', {'data-cy': 'phone-price'})
            price_text = price_div.text.strip() if price_div else 'N/A'
            price_value = re.sub(r'[^\d]', '', price_text) if price_text != 'N/A' else ''
            price = int(price_value) if price_value.isdigit() else None
            
            # Process warranty
            warranty_div = item.find('div', {'data-cy': 'phone-warranty'})
            warranty = warranty_div.text.strip() if warranty_div else ''
            if warranty.startswith("Garancia:"):
                warranty = warranty.split(": ")[-1].strip()
            
            return {
                'Title': title,
                'GPS': gps,
                'Cellular': cellular,
                'Color': color,
                'Size': size,  # Size is now an integer
                'Status': status,
                'Warranty': warranty,
                'Price': price,
                'Link': link
            }
        else:
            # Existing logic for other categories (Mobiles, Tablets, Laptops)
            color = title2_parts[0] if len(title2_parts) > 0 else ''
            memory = title2_parts[1] if len(title2_parts) > 1 else ''
            status = title2_parts[2] if len(title2_parts) > 2 else ''

            if category in ['Tabletek', 'Laptopok']:
                color, memory = memory, color

            warranty_div = item.find('div', {'data-cy': 'phone-warranty'})
            warranty = warranty_div.text.strip() if warranty_div else ''
            if warranty.startswith("Garancia:"):
                warranty = warranty.split(": ")[-1].strip()

            price_div = item.find('span', {'data-cy': 'phone-price'})
            price_text = price_div.text.strip() if price_div else 'N/A'
            price_value = re.sub(r'[^\d]', '', price_text) if price_text != 'N/A' else ''
            price = int(price_value) if price_value.isdigit() else None

            return {
                'Title': title,
                'Color': color,
                'Memory': memory,
                'Status': status,
                'Warranty': warranty,
                'Price': price,
                'Link': link
            }
    except Exception as e:
        print(f"⚠️ Warning: Failed to extract product data - {e}")
        return None

def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"⚠️ Warning: Received status code {response.status_code} for {url}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Warning: Request error ({e}) on attempt {attempt + 1}/{retries}")
        time.sleep(2)
    print(f"❌ Error: Failed to fetch {url} after {retries} attempts.")
    return None

def scrape_page(page_num, category_url, category_name):
    url = f'{category_url}?page={page_num}&sort=BUY_PRICE_DESC'
    page_html = fetch_page(url)
    if not page_html:
        return []
    soup = BeautifulSoup(page_html, 'html.parser')
    items = soup.find_all('div', {'data-cy': 'phone-item'})
    return [extract_data(item, category_name) for item in items if extract_data(item, category_name) is not None]

def main():
    categories = {
        'Telefonok': 'https://www.rejoy.hu/telefon',
        'Tabletek': 'https://www.rejoy.hu/tablet',
        'Laptopok': 'https://www.rejoy.hu/laptop',
        'Okosórák': 'https://www.rejoy.hu/okosora'
    }

    dataframes = {
        'Mobiles': [],
        'Tablets': [],
        'Laptops': [],
        'Smartwatches': []
    }

    for category, category_url in categories.items():
        print(f"\n📌 Starting to scrape category: {category}")
        first_page_html = fetch_page(f'{category_url}?page=1&sort=BUY_PRICE_DESC')
        if not first_page_html:
            print(f"❌ Error: Skipping {category} due to failed page fetch.")
            continue
        soup = BeautifulSoup(first_page_html, 'html.parser')
        last_page = get_last_page(soup)
        for page in range(1, last_page + 1):
            print(f"➡️ Scraping {category} - Page {page}/{last_page}...")
            scraped_data = scrape_page(page, category_url, category)
            if scraped_data:
                if category == 'Telefonok':
                    dataframes['Mobiles'].extend(scraped_data)
                elif category == 'Tabletek':
                    dataframes['Tablets'].extend(scraped_data)
                elif category == 'Laptopok':
                    dataframes['Laptops'].extend(scraped_data)
                elif category == 'Okosórák':
                    dataframes['Smartwatches'].extend(scraped_data)
            time.sleep(1)

    df_mobiles = pd.DataFrame(dataframes['Mobiles'], columns=['Title', 'Color', 'Memory', 'Status', 'Warranty', 'Price', 'Link'])
    df_tablets = pd.DataFrame(dataframes['Tablets'], columns=['Title', 'Memory', 'Color', 'Status', 'Warranty', 'Price', 'Link'])
    df_laptops = pd.DataFrame(dataframes['Laptops'], columns=['Title', 'Memory', 'Color', 'Status', 'Warranty', 'Price', 'Link'])
    df_smartwatches = pd.DataFrame(dataframes['Smartwatches'], columns=['Title', 'GPS', 'Cellular', 'Color', 'Size', 'Status', 'Warranty', 'Price', 'Link'])

    save_path = 'C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Rejoy_Report/rejoy_products.xlsx'
    with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
        df_mobiles.to_excel(writer, sheet_name='Mobiles', index=False)
        df_tablets.to_excel(writer, sheet_name='Tablets', index=False)
        df_laptops.to_excel(writer, sheet_name='Laptops', index=False)
        df_smartwatches.to_excel(writer, sheet_name='Smartwatches', index=False)
    print(f"\n✅ Scraping completed. Data saved to {save_path}")

if __name__ == '__main__':
    main()
