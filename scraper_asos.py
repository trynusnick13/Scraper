from bs4 import BeautifulSoup
from requests import get

from config.config import (HEADERS, ASOS_CATEGORIES, ASOS_BRANDS, ASOS)


class AsosScraper:

    categories = []
    id_ = []
    category = []
    names = []
    price_no_discount = []
    price_discount = []
    brands = []
    all_clothes = []
    brands_all = []
    clothes_containers = None
    name_containers = None
    html_soup = None

    def collect_all_brands(self):
        response_brands = get(ASOS_BRANDS, headers=HEADERS)
        html_soup_brands = BeautifulSoup(response_brands.text, 'html.parser')
        brands_containers = html_soup_brands.find_all('a', class_='m1iDoiz')
        for brand in brands_containers:
            self.brands_all.append(brand.text)

    def find_prices(self,):
        for cloth in self.clothes_containers:
            self.price_no_discount.append(int(''.join((cloth.find('span', '_16nzq18').text.split(','))[0].split())))
            self.price_discount.append(int(''.join((cloth.find('span', '_16nzq18').text.split(','))[0].split())))

    def find_id(self, ):
        for cloth in self.clothes_containers:
            self.id_.append(cloth['id'].lstrip('product-'))

    def find_brand(self):
        name_containers = self.html_soup.find_all('div', class_='_3J74XsK')
        self.collect_all_brands()
        for cloth in name_containers:
            for i in self.brands_all:
                if i in cloth.text:
                    self.brands.append(i)

    def create(self):
        for page in range(2, 3):
            asos = ASOS + str(page)
            response = get(asos, headers=HEADERS)
            self.html_soup = BeautifulSoup(response.text, 'html.parser')
            self.clothes_containers = self.html_soup.find_all('article', class_='_2qG85dG')
            self.name_containers = self.html_soup.find_all('div', class_='_3J74XsK')
            self.collect_all_brands()
            self.brands_all.extend(['As you', 'AS YOU', 'ASOS LUXE', 'ASOS DESIGN', 'As You', 'Style Cheat Becca',
                               'Kavu', 'ASYOU', 'ASOS 4505', 'Tommy Jeans', 'Minga London', 'Cotton:On', 'Abercrombie & Fitch',
                               '& Other Stories', 'New Look', '4th + Reckless', 'Bluebella', 'puma', 'Pull & Bear',
                               'ASOS DESIGN'])
    def find_brand(self):
        for cloth in self.name_containers:
            added = False
            self.names.append(cloth.text)
            for i in self.brands_all:
                if i in cloth.text:
                    print(i + '|||||||' + cloth.text)
                    self.brands.append(i.capitalize())
                    added = True
                    break
            if not added:
                print(cloth.text, '   I have no brands')
                self.rands.append('Default Brand')

    def find_category(self):
        for cloth in self.name_containers:
            added = False
            for i in ASOS_CATEGORIES:
                if i in cloth.text:

                    self.categories.append(i.capitalize())
                    added = True
                    break
            if not added:
                print(cloth.text, '   I have no category')

    def main(self):
        self.create()
        self.collect_all_brands()
        self.find_prices()
        self.find_id()
        # self.find_brand()
        for cloth in self.name_containers:
            added = False
            self.names.append(cloth.text)
            for i in self.brands_all:
                if i in cloth.text:
                    self.brands.append(i.capitalize())
                    added = True
                    break
            if not added:
                print(cloth.text, '   I have no brands')
                self.rands.append('Default Brand')

        for cloth in self.name_containers:
            added = False
            for i in ASOS_CATEGORIES:
                if i in cloth.text:

                    self.categories.append(i.capitalize())
                    added = True
                    break
            if not added:
                print(cloth.text, '   I have no category')

    def write_to_csv(self, filename):
        print(len(self.categories), len(self.brands), len(self.id_), len(self.price_no_discount))
        asos_cloth = pd.DataFrame({
            'ID': self.id_,
            'Brand': self.brands,
            'Name': self.names,
            'Original Price': self.price_no_discount,
            'Price': self.price_discount,
            'Category': self.categories
        }, columns=['ID', 'Brand', 'Name', 'Original Price', 'Price', 'Category'])
        asos_cloth.to_csv(filename, index=False)


if __name__ == '__main__':
    scraper = AsosScraper()
    scraper.main()
    print(len(scraper.categories), len(scraper.brands), len(scraper.id_), len(scraper.price_no_discount))
    scraper.write_to_csv('testing.csv')







