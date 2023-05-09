import argparse
import os
import requests

from collections import deque
from bs4 import BeautifulSoup


class Browser:
    def __init__(self, dir):
        self.dir = dir
        self.valid_commands = ('back', 'exit')
        self.history = deque()
        self.url_start = 'https://'
        self.start()

    def start(self):
        self.create_folder(self.dir)
        previous = ''
        while True:
            user = input()
            if user in self.valid_commands:
                if user == self.valid_commands[0]:
                    if self.history:
                        self.read_webpage(self.history.pop())
                    continue
                if user == self.valid_commands[-1]:
                    exit()
            else:
                if self.read_webpage(user):
                    if previous:
                        self.history.append(previous)
                    previous = user
                continue

    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    def read_webpage(self, url):
        if url.startswith(self.url_start):
            filename = url[8:].split('.', 1)
        else:
            filename = url.split('.', 1)
            url = self.url_start + url
        path = self.dir + '\\' + filename[0]
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as file:
                print(file.read())
            return True
        else:
            try:
                r = requests.get(url)
            except requests.exceptions.ConnectionError:
                print('Invalid URL')
                return False
            soup = BeautifulSoup(r.content, 'html.parser')
            text = soup.get_text()
            print(text)
            with open(path, 'w', encoding='utf-8') as file:
                file.write(text)
            return True


class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('dir')
        self.args = parser.parse_args()

    def get_argument(self):
        return self.args.dir


if __name__ == '__main__':
    Browser(CommandLine().get_argument())
