import pandas as pd
from bs4 import BeautifulSoup
from requests import get

from config.config import (HEADERS, LAMODA)


class LamodaScraper:
    categories = []
    id_ = []
    category = []
    names = []
    price_no_discount = []
    price_discount = []
    all_clothes = []
    brands = []

    def create(self):
        for page in range(1, 2):
            lamoda = LAMODA + str(page)
            response = get(lamoda, headers=HEADERS)
            html_soup = BeautifulSoup(response.text, 'html.parser')
            clothes_containers = html_soup.find_all('div', class_='products-list-item')
            self.all_clothes.append(clothes_containers)

    def find_price(self):
        for bunch in self.all_clothes:
            for cloth in bunch:
                prices = cloth.find_all('span', class_='price')
                for price in prices:
                    if price.find_all('span', class_='price__old'):
                        price_before = int(''.join(price.find('span', class_='price__old').text.split()))
                        price_with_discount = int(''.join(price.find('span', class_='price__action').text.split()))
                        self.price_no_discount.append(price_before)
                        self.price_discount.append(price_with_discount)

                    elif price.find_all('span', class_='price__action'):
                        price_with_discount = int(''.join(price.find('span', class_='price__action').text.split()))
                        price_before = int(''.join(price.find('span', class_='price__actual').text.split()))
                        self.price_discount.append(price_with_discount)
                        self.price_no_discount.append(price_before)
                    else:
                        price_before = int(''.join(price.find('span', class_='price__actual').text.split()))
                        self.price_discount.append(price_before)
                        self.price_no_discount.append(price_before)

    def find_id(self):
        for bunch in self.all_clothes:
            for cloth in bunch:
                self.id_.append(cloth['data-sku'])

    def find_category_name_brand(self):
        for bunch in self.all_clothes:
            for cloth in bunch:
                brand = cloth.find('div', class_='products-list-item__brand').text.split()[0]

                category_and_name = (cloth.find('div', class_='products-list-item__brand')) \
                    .find('span', class_='products-list-item__type')

                category = category_and_name.text.split()[0]
                name = ' '.join(category_and_name.text.split())
                self.categories.append(category)
                self.names.append(name)
                self.brands.append(brand)

    def write_to_csv(self, filename):
        lamoda_cloth = pd.DataFrame({
            'ID': self.id_,
            'Brand': self.brands,
            'Name': self.names,
            'Original Price': self.price_no_discount,
            'Price': self.price_discount,
            'Category': self.categories
        }, columns=['ID', 'Brand', 'Name', 'Original Price', 'Price', 'Category'])
        lamoda_cloth.to_csv(filename, index=False)

    def main(self):
        self.create()
        self.find_price()
        self.find_category_name_brand()
        self.find_id()
        self.write_to_csv('new.csv')


scrapper = LamodaScraper()
scrapper.main()
