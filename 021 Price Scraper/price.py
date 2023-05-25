import requests
from bs4 import BeautifulSoup
from datetime import date


class WrongPageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Scraper:
    def __init__(self):
        self.gold_portfolio = ({'amount': 124, 'name': '1/25oz Cesky Lev Gold Coin',
                                'url': 'https://ceskamincovna.cz/zlata-1-25oz-investicni-mince-cesky-lev-2023-stand-2646-16689-d'},
                               {'amount': 1, 'name': '1/4oz Cesky Lev Gold Coin',
                                'url': 'https://ceskamincovna.cz/zlata-1-4oz-investicni-mince-cesky-lev-2023-stand-2646-16680-d'},
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
        for i in range(len(self.gold_portfolio)):
            price = 0
            try:
                gold = self.gold_portfolio[i]
                r = requests.get(gold['url'])
                if r.status_code != 200:
                    raise WrongPageError(f"The URL: {gold['url']} returned {r.status_code}!")
                soup = BeautifulSoup(r.content, 'html.parser')
                if i < 2:
                    scripts = soup.find_all('script')
                    for script in scripts:
                        for line in script:
                            index = line.find('value')
                            if index != -1:
                                price = line[index + 7: index + 12]
                                price = ''.join([x for x in price if x.isnumeric()])
                else:
                    price = soup.find('span', {'class': 'fs-4 c-gold'}).text
                    price = ''.join([x for x in price if x.isnumeric()])
                self.add_to_logger(gold, int(price))
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
