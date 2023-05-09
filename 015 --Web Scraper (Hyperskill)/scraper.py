import json
import requests

class NoQuoteError(Exception):
    def __init__(self):
        self.message = "Invalid quote resource!"
        super().__init__(self.message)


class Scraper:
    def __init__(self):
        self.start()

    def start(self):
        print("Input the URL:")
        url = input()
        r = requests.get(url)
        try:
            if r.status_code != 200:
                raise NoQuoteError
            quote = r.json()
            if 'content' not in quote.keys():
                raise NoQuoteError
            print(quote['content'])
        except NoQuoteError as noq:
            print(noq)


if __name__ == "__main__":
    Scraper()