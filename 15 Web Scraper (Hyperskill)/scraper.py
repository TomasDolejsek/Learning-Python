import string
import requests
import os
from bs4 import BeautifulSoup


class WrongPageError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class Scraper:
    def __init__(self):
        self.URL = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020'
        self.start()

    def start(self):
        try:
            number = int(input())
            about = input()
            r = requests.get(self.URL, headers={'Accept-Language': 'en-US,en;q=0.5'})
            if r.status_code != 200:
                raise WrongPageError (f'The URL returned {r.status_code}!')
            links = self.find_articles(r.content, about)
            for i in range(1, number + 1):
                dirname = 'Page_' + str(i)
                if not os.path.exists(dirname):
                    os.mkdir(dirname)
                os.chdir(dirname)
                if links:
                    self.process_article(links[i - 1])
                os.chdir(os.pardir)
        except WrongPageError as err:
            print(err)
        except ValueError:
            print('Wrong number!')

    def find_articles(self, content, about):
        links = list()
        soup = BeautifulSoup(content, 'html.parser')
        articles = soup.find_all('article')
        for article in articles:
            span = article.find('span', {'class': 'c-meta__type'}, text=about)
            if span:
                link = article.find('a', {'data-track-action': 'view article'})
                links.append('https://www.nature.com' + link['href'])
        return links

    def process_article(self, link):
        r = requests.get(link, headers={'Accept-Language': 'en-US,en;q=0.5'})
        soup = BeautifulSoup(r.content, 'html.parser')
        title = soup.find('title')
        filename = ''
        for letter in title.text:
            if letter in string.punctuation or letter in string.whitespace:
                filename += '_'
            else:
                filename += letter
        if filename[-1] == '_':
            filename = filename[:-1] + '.txt'
        else:
            filename += '.txt'
        teaser = soup.find('p', {"class": "article__teaser"})
        self.save_article(filename, teaser.text)

    def save_article(self, filename, data):
        with open(filename, 'wb') as file:
            file.write(data.encode(encoding='utf-8'))
        print(f"Article {filename} saved.")


if __name__ == "__main__":
    Scraper()
