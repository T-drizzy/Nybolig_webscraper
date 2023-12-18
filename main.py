import requests
from bs4 import BeautifulSoup
import time
import csv

# URL of the Nybolig page for scraping
NB_root_url = 'https://www.nybolig.dk/til-salg/hus/aarhus-8000-8210'

# Defining the addon for multiple pages
NB_addon_page_num = 5
page_shift = 1

# List of URL's to get through
NB_all_url =['https://www.nybolig.dk/til-salg/hus/aarhus-8000-8210',]

# Loop to add the extra webpages to scrape containing the addon
for page_url in range(NB_addon_page_num):
    NB_addon_url = f'?page={page_shift}'
    page_url = 'https://www.nybolig.dk/til-salg/hus/aarhus-8000-8210'+ NB_addon_url
    page_shift += 1
    NB_all_url.append(page_url)

# Send a GET request to the URL
NB_response = requests.get(NB_root_url)

### MANGLER ET FOR LOOP FOR AT TJEKKE ALLE SIDER.
x = 1
y = 2

for x in range(y):
    x+=2
    print(x)
    
# Check if the response status code is 200 (OK)
if NB_response.status_code == 200:
    # Extract the HTML content from the response
    NB_html = NB_response.text

    # Parse the HTML content with BeautifulSoup
    soup = BeautifulSoup(NB_html, 'html.parser')

    # Find all elements with class "tile__price" for house prices
    NB_prices = soup.findAll('p', class_="tile__price")

    # Find all elements with class "tile__address" for house addresses
    NB_location = soup.findAll('p', class_="tile__address")

    # Find all elements with class "tile__mix" for extra information
    NB_extra = soup.findAll('p', class_="tile__mix")

    # Base key for the house data dictionary
    base_house_data_key = 'house_'

    # Dictionary to store house data
    house_data = {}

    # Loop iterates over the zipped tuples, unpacking them into three variables: house_index, house_address, house_price, and extra_info.
    for house_index, (house_address, house_price, extra_info) in enumerate(zip(NB_location, NB_prices, NB_extra)):
        # Create a unique key for each house
        house_data_key = f'{base_house_data_key}{house_index}'

        # Populate the house_data dictionary with detailed information for each house
        house_data[house_data_key] = {
            'address': house_address.text.strip(),
            'price': house_price.text.strip(),
            'extra_info': extra_info.text.strip()
        }

def store_data_in_csv(data, csv_file_path='house_data.csv'):
    """
    Save data to a CSV file.

    Args:
        data (dict): Dictionary containing the data.
        csv_file_path (str): Path to the CSV file. Default is 'house_data.csv'.
    """
    # Open the CSV file for writing
    with open(csv_file_path, 'w', newline='') as csvfile:
        # Define the fieldnames for the CSV file
        csv_fieldnames = ['house_key', 'address', 'price', 'extra_info']

        # Create a CSV DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=csv_fieldnames)
       
        # Write the header to the CSV file
        writer.writeheader()

        # Write data rows to the CSV file
        for house_data_key, house_info in data.items():
            writer.writerow({
                'house_key': house_data_key,
                'address': house_info['address'],
                'price': house_info['price'],
                'extra_info': house_info['extra_info'],
            })

        # Print a confirmation message
        print(f'Data saved to {csv_file_path}')

store_data_in_csv(house_data)
