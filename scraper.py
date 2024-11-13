from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
from data import Data


class Scraper:
    def __init__(self, headless=False):
        self.chrome_options = Options()

        if headless:
            self.chrome_options.add_argument("--headless")
        self.service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.data_handler = Data()

    def scrape_newegg(self, product_name, zip_code):
        max_retries = 3
        retry_count = 0
        scraped_data = []

        while retry_count < max_retries:
            try:
                self.driver.get("https://www.newegg.com/")

                wait = WebDriverWait(self.driver, 30)
                time.sleep(4)

                try:
                    zip_box = wait.until(EC.element_to_be_clickable(
                        (By.XPATH, '//*[@id="app"]/header/div[1]/div[1]/div[1]/div[2]/a/div[2]')))
                    zip_box.click()

                    zip_change = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                                        '//*[@id="app"]/header/div[1]/div[1]/div[1]/div[3]/div/div/div/div/div[2]/div[4]/div/div/input')))
                    zip_change.clear()
                    zip_change.send_keys(zip_code)

                    zip_apply = wait.until(
                        EC.element_to_be_clickable((By.XPATH,
                                                    '//*[@id="app"]/header/div[1]/div[1]/div[1]/div[3]/div/div/div/div/div[2]/div[4]/div/button')))
                    zip_apply.click()

                    zip_done = wait.until(EC.element_to_be_clickable(
                        (By.XPATH,
                         '//*[@id="app"]/header/div[1]/div[1]/div[1]/div[3]/div/div/div/div/div[2]/div[7]/button')))
                    zip_done.click()
                    time.sleep(2)
                except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                    print(f"An error occurred while changing ZIP code: {e}")

                search_box = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="app"]/header/div[1]/div[1]/div[1]/div[3]/form/div/div[1]/input')))

                search_box.clear()
                search_box.send_keys(product_name)
                time.sleep(1)
                search_box.send_keys(Keys.ENTER)
                print(f"Search submitted for product: {product_name}")

                wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'item-cell')))
                print("Product listings page loaded.")

                soup = BeautifulSoup(self.driver.page_source, 'html.parser')

                product_list = soup.find_all('div', class_='item-cell')

                if not product_list:
                    print("No products found. Please check the search term or HTML structure.")
                    self.driver.save_screenshot(f'newegg_no_products_retry_{retry_count + 1}.png')
                    retry_count += 1
                    time.sleep(2)
                    continue

                print("Showing Newegg output")
                print("-" * 80)

                for product in product_list:
                    try:
                        product_name_tag = product.find('a', class_='item-title')
                        product_name = product_name_tag.text.strip() if product_name_tag else "Name not available"

                        price_tag = product.find('li', class_='price-current')
                        price = price_tag.text.strip() if price_tag else "Price not available"

                        availability_tag = product.find('button', class_='btn-primary')
                        availability = "In Stock" if availability_tag else "Out of Stock"

                        print(f"Product: {product_name}")
                        print(f"Price: {price}")
                        print(f"Availability: {availability}")
                        print("-" * 40)

                        scraped_data.append([product_name, price, availability])

                    except AttributeError as e:
                        print(f"Attribute error occurred while extracting product details: {e}")
                        continue

                self.data_handler.store_data(scraped_data, filename="newegg_scraped_data.csv")
                return

            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                print(f"An error occurred during attempt {retry_count + 1}: {e}")
                self.driver.save_screenshot(f'newegg_error_retry_{retry_count + 1}.png')
                retry_count += 1
                time.sleep(3)

        print("Failed to complete scraping after multiple attempts.")

    def scrape_microcenter(self, product_name):
        try:
            self.driver.get("https://www.microcenter.com/")

            wait = WebDriverWait(self.driver, 20)
            search_box = wait.until(EC.visibility_of_element_located((By.ID, 'search-query')))

            self.driver.execute_script("arguments[0].value = '';", search_box)

            self.driver.execute_script("arguments[0].value = arguments[1];", search_box, product_name)

            form = self.driver.find_element(By.ID, 'searchForm')
            self.driver.execute_script("arguments[0].submit();", form)

            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'product_wrapper')))

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            product_list = soup.find_all('li', class_='product_wrapper')

            scraped_data = []

            print("Showing microcenter output")
            print("-" * 80)
            for product in product_list:
                try:
                    product_name_tag = product.find('a', class_='productClickItemV2')
                    if product_name_tag:
                        product_name = product_name_tag.get('data-name', '').strip()
                        if not product_name:
                            product_name = product_name_tag.text.strip()
                    else:
                        product_name = "Name not available"

                    price_wrapper = product.find('div', class_='price')
                    price_tag = price_wrapper.find('span', {'itemprop': 'price'}) if price_wrapper else None
                    if price_tag:
                        price = price_tag.text.strip().replace("Our price ", "").replace("$", "").strip()
                    else:
                        price = "Price not available"

                    availability_tag = product.find('button', class_='btn-add')
                    availability = "In Stock" if availability_tag else "Out of Stock"

                    print(f"Product: {product_name}")
                    print(f"Price: ${price}")
                    print(f"Availability: {availability}")
                    print("-" * 40)

                    scraped_data.append([product_name, price, availability])

                except Exception as e:
                    print(f"An error occurred with a product: {e}")
                    continue

            self.data_handler.store_data(scraped_data, filename="microcenter_scraped_data.csv")

        except Exception as e:
            print(f"An error occurred on Micro Center: {e}")

    def scrape_amazon(self, product_name, zip_code):
        try:
            self.driver.get("https://www.amazon.com/")
            wait = WebDriverWait(self.driver, 20)
            time.sleep(2)

            zip_box = wait.until(EC.element_to_be_clickable((By.ID, 'nav-global-location-popover-link')))
            zip_box.click()

            zip_change = wait.until(EC.element_to_be_clickable((By.ID, 'GLUXZipUpdateInput')))
            zip_change.clear()
            zip_change.send_keys(zip_code)

            zip_apply = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="GLUXZipUpdate"]/span/input')))
            zip_apply.click()

            zip_done = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="a-popover-1"]/div/div[2]/span/span/span/button')))
            zip_done.click()
            time.sleep(2)

            search_box = wait.until(EC.element_to_be_clickable((By.ID, "twotabsearchtextbox")))
            search_box.clear()
            search_box.send_keys(product_name)
            search_box.send_keys(Keys.ENTER)
            print(f"Search submitted for product: {product_name}")

            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 's-main-slot')))
            time.sleep(2)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})

            scraped_data = []

            print("Showing amazon output")
            print("-" * 80)
            for idx, product in enumerate(product_containers):
                try:
                    name_tag = product.find('span', class_='a-size-medium a-color-base a-text-normal')
                    product_name = name_tag.text.strip() if name_tag else "Name not available"

                    price_whole = product.find('span', class_='a-price-whole')
                    price_fraction = product.find('span', class_='a-price-fraction')
                    if price_whole:
                        price = f"${price_whole.text.strip()}"
                        if price_fraction:
                            price += f".{price_fraction.text.strip()}"
                    else:
                        price = "Price not available"

                    availability_tag = product.find('span', class_='a-price')
                    if availability_tag:
                        availability = "In Stock"
                    else:
                        availability = "Out of Stock"

                    print(f"Product: {product_name}")
                    print(f"Price: {price}")
                    print(f"Availability: {availability}")
                    print("-" * 40)

                    scraped_data.append([product_name, price, availability])

                    if "More results" in product_name or idx >= 15:
                        break

                except AttributeError as e:
                    print(f"Attribute error occurred while extracting product details: {e}")
                    continue

            # Store the scraped data
            self.data_handler.store_data(scraped_data, filename="amazon_scraped_data.csv")

        except (TimeoutException, NoSuchElementException) as e:
            print(f"An error occurred while scraping Amazon: {e}")
        finally:
            self.driver.quit()

    def search_all_sites(self, product_name, zip_code):
        self.scrape_newegg(product_name, zip_code)
        self.scrape_microcenter(product_name)
        self.scrape_amazon(product_name, zip_code)

    def close_driver(self):
        self.driver.quit()


if __name__ == "__main__":
    product_name = input("Enter the product you want to search for: ")
    zip_code = input("Enter zip code you want to search for: ")

    scraper = Scraper(headless=False)
    scraper.search_all_sites(product_name, zip_code)
    scraper.close_driver()
