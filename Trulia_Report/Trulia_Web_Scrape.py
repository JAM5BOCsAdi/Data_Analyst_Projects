from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import time

# Setup Chrome driver
service = Service('C:/Users/orada/Documents/Data_Analyst/Data_Analyst_Projects/Trulia_Report/ChromeDriver/chromedriver-win64/chromedriver.exe')
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("accept-language=en-GB,en-US;q=0.9,en;q=0.8,hu;q=0.7")
options.add_argument("accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36")

try:
    # Initialize the Chrome driver
    driver = webdriver.Chrome(service=service, options=options)

    # Maximize the browser window
    driver.maximize_window()

    # Load the page
    url = 'https://www.trulia.com/CA/San_Diego/'
    driver.get(url)

    # Wait for the initial content to load
    print("Waiting for the page to load...")
    time.sleep(10)

    # Automatically scroll the page
    print("Scrolling the page...")
    scroll_pause_time = 2  # Pause between each scroll
    screen_height = driver.execute_script("return window.screen.height;")  # Browser window height
    i = 1  # Scroll iteration
    while True:
        # Scroll down one screen height at a time
        driver.execute_script(f"window.scrollTo(0, {screen_height * i});")
        i += 1
        time.sleep(scroll_pause_time)

        # Check if reaching the end of the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if screen_height * i > scroll_height:
            print("Reached the bottom of the page.")
            break

    print("Finished scrolling.")

    # Fetch the page source using BeautifulSoup
    print("Fetching the page source...")
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Extract property links
    print("Extracting property links...")
    results = soup.find_all('li', {'class': 'Grid__CellBox-sc-144isrp-0 sc-84372ace-0 yoWOn cEFmzn', 'data-testid': True})
    property_links = ['https://www.trulia.com' + item.find('a')['href'] for item in results if item.find('a')]

    # Print the results
    print(f"Total Listings Found: {len(results)}")
    print(f"Total Property Links: {len(property_links)}")
    print(property_links)
    
    first_link = property_links[0]
    print(f"First Property Link: {first_link}")
    
    response = driver.get(first_link)
    
    

except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the WebDriver session
    print("Closing the browser...")
    driver.quit()
