import requests
from bs4 import BeautifulSoup


class Translator:
    def __init__(self):
        self.SUPPORTED_LANGUAGES = ('en', 'fr')
        self.URL_BASE = "https://context.reverso.net/translation/"
        self.start()

    def start(self):
        print("Type \"en\" if you want to translate from French into English, "
              "or \"fr\" if you want to translate from English into French:")
        while True:
            language = input().lower().strip()
            if language not in self.SUPPORTED_LANGUAGES:
                print("Invalid input")
                continue
            break
        print("Type the word you want to translate:")
        word = input()
        print(f"You chose \"{language}\" as the language to translate \"{word}\" to.")
        self.translate(language, word)

    def translate(self, language, word):
        url_addon = 'english-french/' if language == 'fr' else 'french-english/'
        url = self.URL_BASE + url_addon + word
        print(url)
        r = requests.get(url, headers={'User-Agent': 'Opera'})
        print(r.status_code, end=' ')
        if r.status_code == 200:
            print('OK')
        else:
            print('NOK')
        print('Translations')
        soup = BeautifulSoup(r.content, 'html.parser')
        translates = soup.find_all('a', {'class': 'translation ltr dict n'})
        print(translates.data-term)


if __name__ == '__main__':
    Translator()
