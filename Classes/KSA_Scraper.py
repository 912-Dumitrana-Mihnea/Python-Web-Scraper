from bs4 import BeautifulSoup
import requests
from Classes.Product_Class import Product

class KSA_Scraper():

    # ksa_link is the link to the ksaretail.ro page with the products needed to be scraped
    def __init__(self, ksa_link: str) -> None: 
        raw_product_list = self.get_raw_product_list(ksa_link) # list with raw html of the products
        self.product_list = self.get_product_list(raw_product_list) # list with the products as product objects
    
    def get_raw_product_list(self, ksa_link: str) -> list:
        url = ksa_link
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        raw_product_list = soup.find_all('div', {'class': 'o_wsale_product_grid_wrapper o_wsale_product_grid_wrapper_1_1'})
        return raw_product_list
    
    def get_product_list(self, raw_product_list: list) -> list:
        product_list = []
        for product in raw_product_list:
            name = product.find('a', {'class': 'product_name'}).text.strip()
            prices = product.find_all('span', {'class': 'oe_currency_value'})
            print(prices)
            price = float(prices[0].text.strip().replace('.', '').replace(',', '.'))
            if len(prices) == 2:
                full_price = float(prices[1].text.strip().replace('.', '').replace(',', '.'))
            else:
                full_price = None
            link = product.find('a', {'class': 'product_name'}).get('href') # we get the link to the product
            link = 'https://www.ksaretail.ro' + link # we add the domain url to the link
            product_list.append(Product(name, price, full_price, link))
        return product_list
