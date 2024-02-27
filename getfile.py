from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def crawl_urls_recursive(driver, url, depth=3):
    if depth == 0:
        return

    print(f"Crawling URLs from: {url}")

    try:
        # Open the web page
        driver.get(url)

        # Use WebDriverWait to wait for <a> tags with href attribute to be present on the page
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))

        # Find all <a> tags with href attribute
        links = driver.find_elements(By.TAG_NAME, 'a')

        # Print and crawl only the URLs with href="/"
        for link in links:
            href = link.get_attribute('href')
            if href == "/":
                print(href)
                crawl_urls_recursive(driver, url + href, depth-1)

    except TimeoutException as e:
        print(f"Timed out waiting for page to load: {e}")
    except Exception as e:
        print(f"Error: {e}")

def crawl_urls(url):
    # Specify the path to the directory containing ChromeDriver executable
    chrome_driver_path = '/path/to/directory/chromedriver'

    # Set up Chrome options
    chrome_options = webdriver.ChromeOptions()

    # Uncomment the line below if you want to run Chrome in headless mode (without a visible browser window)
    # chrome_options.add_argument('--headless')

    # Set the path to the ChromeDriver executable
    chrome_options.add_argument(f'--webdriver.chrome.driver={chrome_driver_path}')

    # Initialize the Chrome browser with the specified options
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Start crawling recursively
        crawl_urls_recursive(driver, url)
    finally:
        # Close the browser in a finally block to ensure it gets closed even if an exception occurs
        driver.quit()

if __name__ == "__main__":
    url_to_crawl = "https://share4vn.one/0:/"
    crawl_urls(url_to_crawl)
