import requests
from bs4 import BeautifulSoup
from datetime import date


class WrongPageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Scraper:
    def __init__(self):
        self.gold_portfolio = ({'id': '76172-610', 'amount': 124, 'name': '1/25oz Cesky Lev Gold Coin',
                                'url': 'https://ceskamincovna.cz/zlate-investicni-mince-cesky-lev-1753-p/'},
                               {'id': '76357-610', 'amount': 1, 'name': '1/4oz Cesky Lev Gold Coin',
                                'url': 'https://ceskamincovna.cz/zlate-investicni-mince-cesky-lev-1753-p/'},
                               {'amount': 3, 'name': '2.5g Argor Heraeus Gold Bar',
                                'url': 'https://zlataky.cz/2-5g-argor-heraeus-sa-svycarsko-investicni-zlaty-slitek'},
                               {'amount': 1, 'name': '5g Argor Heraeus Gold Bar',
                                'url': 'https://zlataky.cz/5-g-argor-heraeus-sa-svycarsko-investicni-zlaty-slitek'},
                               {'amount': 3, 'name': '1/4oz Wiener Philharmoniker Gold Coin',
                                'url': 'https://zlataky.cz/zlata-investicni-mince-wiener-philharmoniker-1-4-oz'},
                               {'amount': 1, 'name': '1/4oz Britannia Gold Coin',
                                'url': 'https://zlataky.cz/zlata-investicni-mince-britannia-1-4-oz'},
                               {'amount': 4, 'name': '1/4oz Maple Leaf Gold Coin',
                                'url': 'https://zlataky.cz/zlata-investicni-mince-maple-leaf-1-4-oz'})
        self.total = 0
        self.logger = list()
        self.start()

    def start(self):
        i = 0
        while i < len(self.gold_portfolio):
            try:
                r = requests.get(self.gold_portfolio[i]['url'])
                if r.status_code != 200:
                    raise WrongPageError(f"The URL: {self.gold_portfolio[i]['url']} returned {r.status_code}!")
                soup = BeautifulSoup(r.content, 'html.parser')
                if i < 2:
                    scripts = soup.find_all('script')
                    found = False
                    for script in scripts:
                        for line in script:
                            index0 = line.find(self.gold_portfolio[0]['id'])
                            index1 = line.find(self.gold_portfolio[1]['id'])
                            if index0 != -1 and index1 != -1:
                                found = True
                                price = str(line)[index0 + 23: index0 + 28]
                                price = ''.join([x for x in price if x.isnumeric()])
                                self.add_to_logger(self.gold_portfolio[0], int(price))
                                price = str(line)[index1 + 23: index1 + 28]
                                price = ''.join([x for x in price if x.isnumeric()])
                                self.add_to_logger(self.gold_portfolio[1], int(price))
                                break
                        if found:
                            i = 2
                            break
                else:
                    price = soup.find('span', {'class': 'fs-4 c-gold'}).text
                    price = ''.join([x for x in price if x.isnumeric()])
                    self.add_to_logger(self.gold_portfolio[i], int(price))
                    i += 1
            except WrongPageError as err:
                print(err)
                continue
        self.print_logger()
        while True:
            try:
                mincovna = int(input('Ceska Mincovna: '))
                if mincovna < 0:
                    raise ValueError
                break
            except ValueError:
                continue
        print(f"Total: {self.total + mincovna} Czk")

    def add_to_logger(self, item, price):
        self.total += price * item['amount']
        self.logger.append(f"{item['name']}: {price} Czk")
        
    def print_logger(self):
        print(date.today())
        print('\n'.join(self.logger))


if __name__ == "__main__":
    Scraper()
