import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7',
    'Connection': 'keep-alive'
}
BASE_URL = 'https://www.rejoy.hu'

def get_last_page(soup):
    pagination = soup.select('nav[aria-label="pagination"] li')
    pages = []
    for li in pagination:
        page = li.find('span')
        if page and page.text.isdigit():
            pages.append(int(page.text))
    return max(pages) if pages else 1

def extract_phone_data(item):
    link_tag = item.find('a', href=True)
    link = f"{BASE_URL}{link_tag['href']}" if link_tag else ''
    
    title_spans = item.select('[data-cy="phone-title"] span')
    title = title_spans[0].text.strip() if len(title_spans) > 0 else ''  # Title1 is now just the main title
    
    # Title2 will be split into Color, Memory, and Status
    title2 = title_spans[1].text.strip() if len(title_spans) > 1 else ''
    title2_parts = [part.strip() for part in title2.split(',')]  # Split by comma and remove leading/trailing whitespace
    
    # Extract Color, Memory, and Status (if they exist)
    color = title2_parts[0] if len(title2_parts) > 0 else ''
    memory = title2_parts[1] if len(title2_parts) > 1 else ''
    status = title2_parts[2] if len(title2_parts) > 2 else ''
    
    # Extract warranty with the label ("Garancia: ") left in, but split after ": "
    warranty_div = item.find('div', {'data-cy': 'phone-warranty'})
    warranty = warranty_div.text.strip() if warranty_div else ''
    
    # Split the string at ": " and get the second part (i.e., the duration "2 év")
    if warranty.startswith("Garancia:"):
        warranty = warranty.split(": ")[-1].strip()  # Take the part after ": "
    
    # Extract price
    price_div = item.find('span', {'data-cy': 'phone-price'})
    price = price_div.text.strip() if price_div else 'N/A'
    
    return {
        'Title': title,  # Title is now the first part
        'Color': color,  # Color from Title2
        'Memory': memory,  # Memory from Title2
        'Status': status,  # Status from Title2
        'Warranty': warranty,  # Warranty will now just contain the duration (e.g., "2 év")
        'Price': price,  # Price
        'Link': link
    }


def scrape_page(page_num):
    url = f'https://www.rejoy.hu/telefon/?page={page_num}&sort=BUY_PRICE_DESC'
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to fetch page {page_num}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.find_all('div', {'data-cy': 'phone-item'})
    return [extract_phone_data(item) for item in items]

def main():
    # Get first page to determine total pages
    first_page = scrape_page(1)
    soup = BeautifulSoup(requests.get(f'{BASE_URL}/telefon/?page=1&sort=BUY_PRICE_DESC', headers=headers).text, 'html.parser')
    last_page = get_last_page(soup)
    
    all_data = []
    for page in range(1, last_page + 1):
        print(f"Scraping page {page}/{last_page}")
        all_data.extend(scrape_page(page))
        time.sleep(1)  # Respectful delay
    
    # Convert to pandas DataFrame
    df = pd.DataFrame(all_data)
    
    # Save to CSV with proper encoding (UTF-8 with accents support)
    df.to_csv('rejoy_phones.csv', index=False, encoding='utf-8-sig')
    print("Scraping completed. Data saved to rejoy_phones.csv")

if __name__ == '__main__':
    main()