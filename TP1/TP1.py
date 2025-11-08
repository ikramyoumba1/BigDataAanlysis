import requests
from bs4 import BeautifulSoup
import pandas as pd

# ----------------------------------------------------
# 1. Fetch page content and collect 1000 products
# ----------------------------------------------------

print("--- Starting to collect 1000 products ---")

products_data = []
base_url = "https://scrapeme.live/shop/page/{}/"
page_num = 1

while len(products_data) < 1000:
    current_url = base_url.format(page_num)
    
    try:
        print(f"Fetching page {page_num}: {current_url}")
        response = requests.get(current_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        product_containers = soup.find_all('li', class_='product')
        
        if not product_containers:
            print("No more products found. Stopping.")
            break
            
        for product in product_containers:
            if len(products_data) >= 1000:
                break
                
            title_element = product.find('h2', class_='woocommerce-loop-product__title')
            title = title_element.text.strip() if title_element else 'N/A'
            
            price_element = product.find('span', class_='woocommerce-Price-amount')
            price = price_element.text.strip() if price_element else 'N/A'
            
            products_data.append({
                'Title': title,
                'Price': price
            })
        
        print(f"Collected {len(products_data)} products so far...")
        page_num += 1
        
    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch page {page_num}: {e}")
        break

# ----------------------------------------------------
# 2. Save exactly 1000 products to CSV
# ----------------------------------------------------

if len(products_data) > 1000:
    products_data = products_data[:1000]

df = pd.DataFrame(products_data)
csv_file_name = 'products_data_1000.csv'
df.to_csv(csv_file_name, index=False, encoding='utf-8', sep=',')

print(f"\n--- Data Storage Complete ---")
print(f"✅ Successfully saved EXACTLY {len(df)} products in the file: {csv_file_name}")

print("\nFirst 5 rows of the CSV file:")
print(df.head())

print(f"\nLast 5 rows of the CSV file:")
print(df.tail())

print(f"\n📊 Summary:")
print(f"Total products collected: {len(products_data)}")
print(f"Pages scraped: {page_num - 1}")
print(f"CSV file: {csv_file_name}")
