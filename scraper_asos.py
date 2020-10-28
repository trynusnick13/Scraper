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

brands = []
all_clothes = []
asos_categories = ['кардиган', 'джемпер', 'водолазка', 'платье', 'джоггеры', 'футболка', 'топ',
                   'комбинезон', 'костюм', 'куртка', 'леггинсы', 'рубашка', 'блейзер', 'свитшот', 'худи',
                   'юбка', 'лонгслив', 'джоггеры', 'пуховик', 'бюстгалтер', 'ромпер', 'Платье', 'Колготки',
                   'cardigan', 'set', 'Костюм', 'Боди', 'боди', 'брюки', 'Топ', 'Футболка', 'Рубашка', 'Леггинсы',
                   'Кардиган', 'кофта', 'Худи', 'сарафан', 'блузка', 'Пуховик', 'Водолазка', 'Носки', 'комплект',
                   'Лонгслив', 'Набор', 'пижама', 'купальник', 'бюстгальтер', 'парео', 'джинсы', 'майка',
                   'стринги', 'Блузка', 'бикини', 'Свитер', 'термобель', 'hoodie', 'Пальто', 'пальто', 'Свитшот',
                   'жилет', 'пиджак', 'шорты', 'Бикини', 'тренч', 'джеггинсы', 'sweat', 'трусы', 'Дубленка',
                   'халат', 'Майка', 'тайтсы', 'Юбка', 'Чиносы', 'Джоггеры', 'Джемпер', 'Брюки', 'Кимоно', 'Юбка',
                   'Шорты', 'пояс', 'свитшот', 'Джинсы', 'Комбинезон', 'Ромпер', 'боксеры', 'сорочка', 'поло',
                   'чиносы', 'бомбер', 'бралетт', 'Туника', 'джоггер', 'бралетт', 'Комплект', 'маска', 'Легинсы',
                   'jumper', 'top', 'леггинс', '']


brands_all = []
def collect_all_brands():
    asos_brands = 'https://www.asos.com/ru/women/a-to-z-of-brands/cat/?cid=1340&nlid=ww|бренды|топ+бренды'
    response_brands = get(asos_brands, headers=headers)
    html_soup_brands = BeautifulSoup(response_brands.text, 'html.parser')
    # print(response_brands)

    brands_containers = html_soup_brands.find_all('a', class_='m1iDoiz')
    for brand in brands_containers:
        # print(brand.text.strip())
        brands_all.append(brand.text)
    # print(len(brands_all), brands_all)

def find_prices(clothes_containers):
    for cloth in clothes_containers:
        # print(int(''.join((cloth.find('span', '_16nzq18').text.split(','))[0].split())))
        price_no_discount.append(int(''.join((cloth.find('span', '_16nzq18').text.split(','))[0].split())))
        price_discount.append(int(''.join((cloth.find('span', '_16nzq18').text.split(','))[0].split())))

def find_id(clothes_containers):
    for cloth in clothes_containers:
        # print(cloth['id'].lstrip('product-'))
        id_.append(cloth['id'].lstrip('product-'))

def find_brand(html_soup):
    name_containers = html_soup.find_all('div', class_='_3J74XsK')
    collect_all_brands()
    for cloth in name_containers:
        print(cloth.text)
        for i in brands_all:
            if i in cloth.text:
                brands.append(i)
    print(brands)

headers = ({'User-Agent':
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15'
                ' (KHTML, like Gecko) Version/14.0'
                ' Safari/605.1.15'})
for page in range(1, 15):
    asos = 'https://www.asos.com/ru/women/novinki/novinki-odezhda/cat/?cid=2623&currentpricerange=350-38290&nlid=ww|одежда|сортировать%20по%20типу%20продукта&page=' + str(page)
    response = get(asos, headers=headers)

    html_soup = BeautifulSoup(response.text, 'html.parser')
    clothes_containers = html_soup.find_all('article', class_='_2qG85dG')
    name_containers = html_soup.find_all('div', class_='_3J74XsK')
    collect_all_brands()
    brands_all.extend(['As you', 'AS YOU', 'ASOS LUXE', 'ASOS DESIGN', 'As You', 'Style Cheat Becca',
                       'Kavu', 'ASYOU', 'ASOS 4505', 'Tommy Jeans', 'Minga London', 'Cotton:On', 'Abercrombie & Fitch',
                       '& Other Stories', 'New Look', '4th + Reckless', 'Bluebella', 'puma', 'Pull & Bear',
                       'ASOS DESIGN'])
    find_id(clothes_containers)
    find_prices(clothes_containers)
    # find_prices(clothes_containers)
    for cloth in name_containers:
        added = False
        names.append(cloth.text)
        for i in brands_all:
            if i in cloth.text:
                brands.append(i.capitalize())
                added = True
                break
        if not added:
            print(cloth.text, '   I have no brands')
            brands.append('As You')

    for cloth in name_containers:
        added = False
        for i in asos_categories:
            if i in cloth.text:
                categories.append(i.capitalize())
                added = True
                break
        if not added:
            print(cloth.text, '   I have no category')

print(len(categories), len(brands), len(id_), len(price_no_discount))
asos_cloth = pd.DataFrame({
    'ID': id_,
    'Brand': brands,
    'Name': names,
    'Original Price': price_no_discount,
    'Price': price_discount,
    'Category': categories
}, columns=['ID', 'Brand', 'Name', 'Original Price', 'Price', 'Category'])
asos_cloth.to_csv('asos_1.csv', index=False)
# print(asos_categories, brands_all, sep='\n')







