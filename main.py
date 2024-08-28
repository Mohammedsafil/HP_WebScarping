import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to scrape
url = "https://www.hp.com/in-en/shop/laptops-tablets.html?no-cache-proxy=true=1&processortype=intel-core-i7"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# Initialize a list to store the extracted data
data = []

# Find all the laptop items in the list
laptop_list = soup.find('ol', class_="products list items product-items grid").find_all('li',
                                                                                        class_="item product product-item g-col-4 g-col-xl-4 g-col-lg-6")

for laptop in laptop_list:
    # Extract the product link and title
    product_link_tag = laptop.find('a', class_="product-item-link")
    href = product_link_tag.get('href') if product_link_tag else None

    # Extract the title text within the h2 tag
    title_tag = product_link_tag.find('h2', class_="plp-h2-title stellar-title__small") if product_link_tag else None
    title = title_tag.get_text(strip=True) if title_tag else None

    # Extract the features
    features_div = laptop.find('div', class_="product-desc-features stellar-body__small")
    features = [feature.get_text() for feature in features_div.find_all('li')] if features_div else []

    # Join the features list into a single string
    features_str = "; ".join(features)

    # Extract the price details
    price_container = laptop.find('div', class_="price-box")

    # Initialize variables to store price details
    starting_price = None
    discount_price = None
    final_price = None
    installment_price = None

    if price_container:
        # Extract the starting price
        starting_price_tag = price_container.find('span', class_="price")
        starting_price = starting_price_tag.get_text() if starting_price_tag else None

        # Extract the discount price, but only if the discount tag is found
        discount_price_tag = price_container.find('div', class_="mrp discount mrp-discount stellar-body__extra-small")
        if discount_price_tag:
            discount_price_span = discount_price_tag.find('span', class_="price")
            discount_price = discount_price_span.get_text() if discount_price_span else None

        # Extract the final price (including taxes)
        final_price_tag = price_container.find('span', class_="price-wrapper price-including-tax")
        final_price = final_price_tag.get_text() if final_price_tag else None

        # Extract installment price if available
        installment_price_tag = price_container.find('div', class_="msi-lowest-price-show-plp")
        installment_price = installment_price_tag.find('span',
                                                       class_="price").get_text() if installment_price_tag else None

    # Append the data to the list
    data.append({
        "Title": title,
        "Link": href,
        "Features": features_str,
        "Starting Price": starting_price,
        "Discount Price": discount_price,
        "Final Price (Incl. Tax)": final_price,
        "Installment Price": installment_price
    })

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file = "laptops_data.xlsx"
df.to_excel(output_file, index=False)

print(f"Data has been written to {output_file}")
