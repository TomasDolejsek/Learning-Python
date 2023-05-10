import requests

from bs4 import BeautifulSoup


class WrongPageError(Exception):
    def __init__(self):
        self.message = "Invalid page!"
        super().__init__(self.message)


class Scraper:
    def __init__(self):
        self.start()

    def start(self):
        header = dict()
        print("Input the URL:")
        url = input()
        try:
            if 'nature.com' not in url or 'articles' not in url:
                raise WrongPageError
            r = requests.get(url, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if r.status_code != 200:
                raise WrongPageError
            soup = BeautifulSoup(r.content, 'html.parser')
            header['title'] = soup.find('title').text
            for tag in soup.find_all('meta'):
                if tag.get('property') == 'og:description':
                    header['description'] = tag.get('content')
            print(header)
        except WrongPageError as err:
            print(err)


if __name__ == "__main__":
    Scraper()
