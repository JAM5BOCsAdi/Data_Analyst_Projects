import requests
from bs4 import BeautifulSoup
import time
import pandas as pd
import re
from datetime import datetime
import pyodbc

# Headers for the requests
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7',
    'Connection': 'keep-alive'
}

BASE_URL = 'https://www.rejoy.hu'

# SQL Server connection setup
def get_sql_server_connection():
    server = 'DESKTOP-3FSNRUN'
    database = 'RejoyProducts'
    connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
    return pyodbc.connect(connection_string)

# SQL table creation query templates
create_table_queries = {
    'Mobiles': '''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Mobiles' AND xtype = 'U')
        CREATE TABLE Mobiles (
            Time VARCHAR(20),
            Title VARCHAR(255),
            Color VARCHAR(50),
            Memory VARCHAR(50),
            Status VARCHAR(50),
            Warranty VARCHAR(50),
            Price INT,
            Link VARCHAR(255)
        )
    ''',
    'Tablets': '''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Tablets' AND xtype = 'U')
        CREATE TABLE Tablets (
            Time VARCHAR(20),
            Title VARCHAR(255),
            Memory VARCHAR(50),
            Color VARCHAR(50),
            Status VARCHAR(50),
            Warranty VARCHAR(50),
            Price INT,
            Link VARCHAR(255)
        )
    ''',
    'Laptops': '''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Laptops' AND xtype = 'U')
        CREATE TABLE Laptops (
            Time VARCHAR(20),
            Title VARCHAR(255),
            CPU VARCHAR(100),
            RAM VARCHAR(50),
            Graphics VARCHAR(50),
            Memory VARCHAR(50),
            Color VARCHAR(50),
            Status VARCHAR(50),
            Warranty VARCHAR(50),
            Price INT,
            Link VARCHAR(255)
        )
    ''',
    'Smartwatches': '''
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name = 'Smartwatches' AND xtype = 'U')
        CREATE TABLE Smartwatches (
            Time VARCHAR(20),
            Title VARCHAR(255),
            GPS VARCHAR(10),
            Cellular VARCHAR(10),
            Color VARCHAR(50),
            Size INT,
            Status VARCHAR(50),
            Warranty VARCHAR(50),
            Price INT,
            Link VARCHAR(255)
        )
    '''
}

# Create table if it doesn't exist
def create_table_if_not_exists(conn, table_name):
    cursor = conn.cursor()
    cursor.execute(create_table_queries.get(table_name, ''))
    conn.commit()

# Save data to SQL Server
def save_to_sql(dataframe, table_name, conn):
    create_table_if_not_exists(conn, table_name)
    cursor = conn.cursor()
    
    insert_queries = {
        'Smartwatches': '''
            IF NOT EXISTS (SELECT 1 FROM Smartwatches WHERE Link = ? AND Time = ?)
            INSERT INTO Smartwatches (Time, Title, GPS, Cellular, Color, Size, Status, Warranty, Price, Link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        'Laptops': '''
            IF NOT EXISTS (SELECT 1 FROM Laptops WHERE Link = ? AND Time = ?)
            INSERT INTO Laptops (Time, Title, CPU, RAM, Graphics, Memory, Color, Status, Warranty, Price, Link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        'Tablets': '''
            IF NOT EXISTS (SELECT 1 FROM Tablets WHERE Link = ? AND Time = ?)
            INSERT INTO Tablets (Time, Title, Memory, Color, Status, Warranty, Price, Link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''',
        'Mobiles': '''
            IF NOT EXISTS (SELECT 1 FROM Mobiles WHERE Link = ? AND Time = ?)
            INSERT INTO Mobiles (Time, Title, Color, Memory, Status, Warranty, Price, Link)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
    }

    query = insert_queries.get(table_name)
    if query:
        for _, row in dataframe.iterrows():
            params = (row['Link'], row['Time']) + tuple(row)
            cursor.execute(query, params)
            if cursor.rowcount > 0:
                print(f"✅ Record added: {row['Title']} - {row['Link']}")
            else:
                print(f"🔄 Skipped (duplicate): {row['Title']} - {row['Link']}")
        conn.commit()

# Fetch the page content with retries
def fetch_page(url, retries=3):
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"⚠️ Warning: Status code {response.status_code} for {url}")
        except requests.exceptions.RequestException as e:
            print(f"⚠️ Warning: Request error ({e}) on attempt {attempt + 1}/{retries}")
        time.sleep(2)
    print(f"❌ Error: Failed to fetch {url} after {retries} attempts.")
    return None

# Get last page number for pagination
def get_last_page(soup):
    try:
        pagination = soup.select('nav[aria-label="pagination"] li')
        pages = [int(li.find('span').text) for li in pagination if li.find('span') and li.find('span').text.isdigit()]
        return max(pages) if pages else 1
    except Exception as e:
        print(f"⚠️ Warning: Failed to extract last page number - {e}")
        return 1

# Extract data based on category
def extract_data(item, category, current_time):
    try:
        link_tag = item.find('a', href=True)
        link = f"{BASE_URL}{link_tag['href']}" if link_tag else ''
        title_spans = item.select('[data-cy="phone-title"] span')
        title = title_spans[0].text.strip() if len(title_spans) > 0 else ''
        title2 = title_spans[1].text.strip() if len(title_spans) > 1 else ''
        title2_parts = [part.strip() for part in title2.split(',')]

        time_column = current_time

        warranty_div = item.find('div', {'data-cy': 'phone-warranty'})
        warranty_text = warranty_div.text.strip() if warranty_div else ''
        warranty_years = int(re.search(r'\d+', warranty_text).group()) if warranty_text else None

        price_div = item.find('span', {'data-cy': 'phone-price'})
        price_text = price_div.text.strip() if price_div else 'N/A'
        price_value = re.sub(r'[^\d]', '', price_text) if price_text != 'N/A' else ''
        price = int(price_value) if price_value.isdigit() else None

        category_map = {
            'Laptopok': lambda: {
                'Time': time_column,
                'Title': title,
                'CPU': title2_parts[1] if len(title2_parts) > 1 else '',
                'RAM': re.sub(r'\s*GB$', '', title2_parts[2]).strip() if len(title2_parts) > 2 else '',
                'Graphics': title2_parts[3].strip() if len(title2_parts) > 3 else '',
                'Memory': title2_parts[0] if len(title2_parts) > 0 else '',
                'Color': title2_parts[1] if len(title2_parts) > 1 else '',
                'Status': title2_parts[2] if len(title2_parts) > 2 else '',
                'Warranty': warranty_years,
                'Price': price,
                'Link': link
            },
            'Telefonok': lambda: {
                'Time': time_column,
                'Title': title,
                'Color': title2_parts[1] if len(title2_parts) > 1 else '',
                'Memory': title2_parts[0] if len(title2_parts) > 0 else '',
                'Status': title2_parts[2] if len(title2_parts) > 2 else '',
                'Warranty': warranty_years,
                'Price': price,
                'Link': link
            },
            'Tabletek': lambda: {
                'Time': time_column,
                'Title': title,
                'Color': title2_parts[1] if len(title2_parts) > 1 else '',
                'Memory': title2_parts[0] if len(title2_parts) > 0 else '',
                'Status': title2_parts[2] if len(title2_parts) > 2 else '',
                'Warranty': warranty_years,
                'Price': price,
                'Link': link
            },
            'Okosórák': lambda: {
                'Time': time_column,
                'Title': re.sub(r'\s*\d{4}$', '', title).strip(),
                'GPS': 'Yes' if 'GPS' in title2_parts[0] else 'No',
                'Cellular': 'Yes' if 'Cellular' in title2_parts[0] else 'No',
                'Color': re.sub(r'\s*\d{2}mm', '', title2_parts[1]).strip(),
                'Size': int(re.search(r'(\d{2})mm', title2_parts[1]).group(1)) if 'mm' in title2_parts[1] else None,
                'Status': title2_parts[2] if len(title2_parts) > 2 else '',
                'Warranty': warranty_years,
                'Price': price,
                'Link': link
            }
        }

        return category_map.get(category, lambda: None)()

    except Exception as e:
        print(f"⚠️ Warning: Failed to extract product data - {e}")
        return None

# Scrape data from a given page
def scrape_page(page_num, category_url, category_name, current_time):
    url = f'{category_url}?page={page_num}&sort=BUY_PRICE_DESC'
    page_html = fetch_page(url)
    if not page_html:
        return []
    soup = BeautifulSoup(page_html, 'html.parser')
    items = soup.find_all('div', {'data-cy': 'phone-item'})
    return [extract_data(item, category_name, current_time) for item in items if extract_data(item, category_name, current_time) is not None]

# Main scraping and saving logic
def main():
    # Category mapping for the correct keys in dataframes
    category_to_dataframe_key = {
        'Telefonok': 'Mobiles',
        'Tabletek': 'Tablets',
        'Laptopok': 'Laptops',
        'Okosórák': 'Smartwatches'
    }

    categories = {
        'Telefonok': 'https://www.rejoy.hu/telefon',
        'Tabletek': 'https://www.rejoy.hu/tablet',
        'Laptopok': 'https://www.rejoy.hu/laptop',
        'Okosórák': 'https://www.rejoy.hu/okosora'
    }

    # Get current time and format it hourly (e.g., 2025-02-09_01)
    current_time = datetime.now().strftime("%Y-%m-%d_") + f"{datetime.now().hour:02d}"

    dataframes = {
        'Mobiles': [],
        'Tablets': [],
        'Laptops': [],
        'Smartwatches': []
    }

    conn = get_sql_server_connection()  # Connect to SQL Server

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
            scraped_data = scrape_page(page, category_url, category, current_time)
            if scraped_data:
                # Use the mapping to store data under the correct key
                dataframe_key = category_to_dataframe_key.get(category)
                if dataframe_key:
                    dataframes[dataframe_key].extend(scraped_data)
            time.sleep(1)

    # Save data to SQL Server
    print(f"\n✅ Saving data to SQL Server...")
    save_to_sql(pd.DataFrame(dataframes['Mobiles']), 'Mobiles', conn)
    save_to_sql(pd.DataFrame(dataframes['Tablets']), 'Tablets', conn)
    save_to_sql(pd.DataFrame(dataframes['Laptops']), 'Laptops', conn)
    save_to_sql(pd.DataFrame(dataframes['Smartwatches']), 'Smartwatches', conn)

    print(f"\n✅ Scraping completed and data saved to SQL Server.")
    conn.close()

if __name__ == '__main__':
    main()