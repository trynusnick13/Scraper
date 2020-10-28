from time import sleep
from bs4 import BeautifulSoup
from requests import get
import pandas as pd


categories = []
id_ = []
category = []
names = []
price_no_discount = []
price_discount = []
all_clothes = []
brands = []

headers = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'
                ' (KHTML, like Gecko) Version/14.0'
                ' Safari/605.1.15'})
# for i in clothes_containers:
#     if (i.text.split()[0]) in categories:
#         categories[i.text.split()[0]] += 1
#     else:
#         categories[i.text.split()[0]] = 1
def collect_all_products():
    pass

def find_price(all_clothes):
    for bunch in all_clothes:
        for cloth in bunch:
            prices = cloth.find_all('span', class_='price')
            for price in prices:
                if price.find_all('span', class_='price__old'):
                    price_before = int(''.join(price.find('span', class_='price__old').text.split()))
                    price_with_discount = int(''.join(price.find('span', class_='price__action').text.split()))
                    price_no_discount.append(price_before)
                    price_discount.append(price_with_discount)

                elif price.find_all('span', class_='price__action'):
                    price_with_discount = int(''.join(price.find('span', class_='price__action').text.split()))
                    price_before = int(''.join(price.find('span', class_='price__actual').text.split()))
                    price_discount.append(price_with_discount)
                    price_no_discount.append(price_before)
                else:
                    price_before = int(''.join(price.find('span', class_='price__actual').text.split()))
                    price_discount.append(price_before)
                    price_no_discount.append(price_before)

def find_id(all_clothes):
    for bunch in all_clothes:
        for cloth in bunch:
            id_.append(cloth['data-sku'])

def find_category_name_brand(all_clothes):
    for bunch in all_clothes:
        for cloth in bunch:
            brand = cloth.find('div', class_='products-list-item__brand').text.split()[0]

            category_and_name = (cloth.find('div', class_='products-list-item__brand')) \
                .find('span', class_='products-list-item__type')

            category = category_and_name.text.split()[0]
            name = ' '.join(category_and_name.text.split())
            categories.append(category)
            names.append(name)
            brands.append(brand)


for page in range(1, 19):
    lamoda = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page=' + str(page)
# lamoda = 'https://www.lamoda.ru/c/355/clothes-zhenskaya-odezhda/?sitelink=topmenuW&l=3&page=1'
    response = get(lamoda, headers=headers)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    clothes_containers = html_soup.find_all('div', class_='products-list-item')
    all_clothes.append(clothes_containers)
    print(len(clothes_containers))
    sleep(1.2)
find_price(all_clothes)
find_category_name_brand(all_clothes)
find_id(all_clothes)

        # cloth.find('div', class_='products-list-item__brand').text.split()

print(brands, len(brands), sep='\n')
print(names, len(names), sep='\n')
print(categories, len(categories), sep='\n')
print(id_, len(id_), sep='\n')
print(price_no_discount, len(price_no_discount), sep='\n')
print(price_discount, len(price_discount), sep='\n')

lamoda_cloth = pd.DataFrame({
    'ID': id_,
    'Brand': brands,
    'Name': names,
    'Original Price': price_no_discount,
    'Price': price_discount,
    'Category': categories
}, columns=['ID', 'Brand', 'Name', 'Original Price', 'Price', 'Category'])
lamoda_cloth.to_csv('lamoda.csv', index=False)


