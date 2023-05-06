import json
import requests


class Converter:
    def __init__(self):
        self.urlpage = 'http://www.floatrates.com/daily/'
        self.currency_rates = dict()
        self.main_currency =''
        self.start()

    def start(self):
        self.main_currency = input().lower()
        if self.main_currency != 'usd':
            self.import_rates('usd')
        if self.main_currency != 'eur':
            self.import_rates('eur')
        while True:
            cur2 = input().lower()
            if not cur2:
                break
            howmany = float(input())
            result = self.get_rates(cur2) * howmany
            print(f"You received {result:.2f} {cur2.upper()}.")

    def import_rates(self, searched_cur):
        url = self.urlpage + self.main_currency + '.json'
        r = requests.get(url)
        curdata = r.json()[searched_cur]
        self.currency_rates[searched_cur] = curdata['rate']
        return curdata['rate']

    def get_rates(self, currency):
        print("Checking the cache...")
        if currency in self.currency_rates.keys():
            print("Oh! It is in the cache!")
            return self.currency_rates[currency]
        else:
            print("Sorry, but it is not in the cache!")
            return self.import_rates(currency)


if __name__ == '__main__':
    Converter()
