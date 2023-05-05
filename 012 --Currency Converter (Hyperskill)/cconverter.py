import json
import requests


class Converter:
    def __init__(self):
        self.urlpage = 'http://www.floatrates.com/daily/'
        self.currencies = ('ARS', 'AUD', 'CZK', 'HNL', 'MAD', 'RUB')
        self.start()

    def start(self):
        user = input().upper()
        if user not in self.currencies:
            print("Unsupported currency.")
            exit()
        url = self.urlpage + user.lower() + '.json'
        page = requests.get(url)
        data = json.loads(page.text)
        for cur, info in data.items():
            if cur == 'usd' or key == 'eur':
                print(info)


if __name__ == '__main__':
    Converter()