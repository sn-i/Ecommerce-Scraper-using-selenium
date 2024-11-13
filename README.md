# Ecommerce Scraper using Selenium

Welcome to the **Ecommerce Scraper using Selenium**! This project is all about simplifying product research across multiple e-commerce platforms. It's a handy web scraper written in Python, leveraging the power of Selenium and BeautifulSoup to pull product information from three popular websites—Newegg, Microcenter, and Amazon. The scraper is built with ease of use in mind, and it collects details like product name, price, and availability, storing them neatly in CSV files. Whether you’re doing market research, looking for deals, or just curious about products, this scraper has got you covered.
## Key Features

- **Get Product Info All in One Place**: Easily extract product names, prices, and availability from Newegg, Microcenter, and Amazon.
- **Customizable ZIP Code Support**: Input a specific ZIP code to tailor product availability based on your region, offering more personalized results.
- **Data Persistence**: Collected data is saved in well-structured CSV files, making it easy for you to perform further analysis or integrate with other systems.
- **Ease of Use**: This scraper is ideal for developers, data analysts, and anyone interested in price comparison, market research, or e-commerce trends.

## Installation

To get started with the Ecommerce Scraper:

1. **Clone the Repository**

   ```sh
   git clone https://github.com/sn-i/Ecommerce-Scraper-using-selenium.git
   ```

2. **Install Required Packages**

   Ensure you have Python installed, and then run the following command to install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

## How to Use the Scraper

Running the scraper is straightforward:

1. **Start the Script**

   Execute the script by running the following command:

   ```sh
   python scraper.py
   ```

   The script will prompt you to enter the product name and ZIP code.

2. **Data Collection**

   The scraper will then search Newegg, Microcenter, and Amazon for the specified product, collect the details, and store the information in CSV files.

## Sample Output

Below is a sample of the output you can expect:

### Console Output:

```
Product: ASUS GeForce RTX 4070
Price: $599.99
Availability: In Stock
----------------------------------------
Product: MSI GeForce RTX 4070 Ventus
Price: $579.99
Availability: Out of Stock
----------------------------------------
```

### CSV Files:

The data is saved in CSV files for each website, such as:

- `newegg_scraped_data.csv`
- `microcenter_scraped_data.csv`
- `amazon_scraped_data.csv`

Each CSV file contains columns for **Product Name**, **Price**, and **Availability**, making the data easy to sort and analyze.

## Project Structure

- **`scraper.py`**: Contains the primary web scraping logic, including handling ZIP codes and navigating the sites.
- **`data.py`**: Manages storing scraped data in CSV format, ensuring data is consistently organized and accessible.

## Requirements

- **Python 3.7+**
- **Selenium**: For browser automation.
- **BeautifulSoup4**: For parsing the HTML of web pages.
- **ChromeDriver**: Managed by `webdriver_manager` for hassle-free setup.

With this scraper, you can easily track product prices, availability, and trends across multiple platforms. Whether you're a developer, researcher, or simply a bargain hunter, this tool will save you time and effort in gathering the information you need.

Happy scraping!

