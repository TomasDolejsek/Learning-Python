import requests
import argparse
from bs4 import BeautifulSoup


class TranslatorError(Exception):
    def __init__(self, whats_wrong):
        self.message = whats_wrong
        super().__init__(self.message)


class Translator:
    def __init__(self):
        self.SUPPORTED_LANGUAGES = {'1': 'arabic',
                                    '2': 'german',
                                    '3': 'english',
                                    '4': 'spanish',
                                    '5': 'french',
                                    '6': 'hebrew',
                                    '7': 'japanese',
                                    '8': 'dutch',
                                    '9': 'polish',
                                    '10': 'portuguese',
                                    '11': 'romanian',
                                    '12': 'russian',
                                    '13': 'turkish'}
        self.URL_BASE = "https://context.reverso.net/translation/"
        self.logger = []
        args = self.get_arguments()
        self.start(args.lang_from.lower(), args.lang_to.lower(), args.word.lower())

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('lang_from', default='english')
        parser.add_argument('lang_to', default='all')
        parser.add_argument('word')
        return parser.parse_args()

    def start(self, lang_from, lang_to, word):
        try:
            if lang_from not in self.SUPPORTED_LANGUAGES.values():
                raise TranslatorError(f"Sorry, the program doesn't support {lang_from}.")
            if lang_to not in self.SUPPORTED_LANGUAGES.values() and lang_to != 'all':
                raise TranslatorError(f"Sorry, the program doesn't support {lang_to}.")
            if lang_to != 'all':
                self.translate(lang_from, lang_to, word)
            else:
                for lang in self.SUPPORTED_LANGUAGES.values():
                    if lang != lang_from:
                        self.translate(lang_from, lang, word)
            self.print_logger()
            self.save_result(word)
        except TranslatorError as err:
            print(err)
            exit()

    def translate(self, lang_from, lang_to, word):
        url = self.get_url(lang_from, lang_to, word)
        r = requests.get(url, headers={'User-Agent': 'Opera'})
        if r.status_code != 200:
            if r.status_code == 404:
                raise TranslatorError(f"Sorry, unable to find {word}.")
            else:
                raise TranslatorError("Something wrong with your internet connection.")
        soup = BeautifulSoup(r.content, 'html.parser')
        translations = soup.find_all('span', {'class': 'display-term'})
        words = []
        for translation in translations:
            words.append(translation.text.strip())
        self.logger.append(f"\n{lang_to.capitalize()} Translation:")
        self.logger.append(f"{words[0]}")
        examples = soup.find_all('div', {'class': 'src'})
        trans_examples = soup.find_all('div', {'class': 'trg'})
        sentences = []
        for example, trans in zip(examples, trans_examples):
            sentences.append(example.text.strip())
            sentences.append(trans.text.strip())
        self.logger.append(f"\n{lang_to.capitalize()} Example:")
        self.logger.append(f"{sentences[0]}")
        self.logger.append(f"{sentences[1]}")

    def get_url(self, lang_from, lang_to, word):
        url_addon = lang_from + '-' + lang_to + '/'
        return self.URL_BASE + url_addon + word

    def print_logger(self):
        print(*self.logger, sep='\n')

    def save_result(self, word):
        file_name = word + '.txt'
        with open(file_name, 'wt', encoding='UTF-8') as file:
            file.write('\n'.join(self.logger))


if __name__ == '__main__':
    Translator()
