import argparse
import os


class Browser:
    def __init__(self, dir):
        self.dir = dir
        self.nytimes_com = '''
        This New Liquid Is Magnetic, and Mesmerizing

        Scientists have created "soft" magnets that can flow 
        and change shape, and that could be a boon to medicine 
        and robotics. (Source: New York Times)


        Most Wikipedia Profiles Are of Men. This Scientist Is Changing That.

        Jessica Wade has added nearly 700 Wikipedia biographies for
        important female and minority scientists in less than two 
        years.

        '''
        self.bloomberg_com = '''
        The Space Race: From Apollo 11 to Elon Musk

        It's 50 years since the world was gripped by historic images
        of Apollo 11, and Neil Armstrong -- the first man to walk 
        on the moon. It was the height of the Cold War, and the charts
        were filled with David Bowie's Space Oddity, and Creedence's 
        Bad Moon Rising. The world is a very different place than 
        it was 5 decades ago. But how has the space race changed since
        the summer of '69? (Source: Bloomberg)


        Twitter CEO Jack Dorsey Gives Talk at Apple Headquarters

        Twitter and Square Chief Executive Officer Jack Dorsey 
        addressed Apple Inc. employees at the iPhone maker’s headquarters
        Tuesday, a signal of the strong ties between the Silicon Valley giants.
        '''
        self.valid_urls = ('nytimes.com', 'bloomberg.com')
        self.start()

    def start(self):
        self.create_folder(self.dir)
        while True:
            url = input()
            if url == 'exit':
                exit()
            if not self.check_url(url) or url not in self.valid_urls:
                print("Invalid URL")
                continue
            if url == self.valid_urls[0]:
                print(self.nytimes_com)
                self.save_file(url, self.nytimes_com)
                continue
            if url == self.valid_urls[1]:
                print(self.bloomberg_com)
                self.save_file(url, self.bloomberg_com)
                continue

    def create_folder(self, folder):
        if not os.path.exists(folder):
            os.mkdir(folder)

    def check_url(self, url):
        return True if url.count('.') > 0 else False

    def save_file(self, url, text):
        filename = self.dir + '\\' + url.split('.', 1)[0]
        if not os.path.exists(filename):
            with open(filename, 'w') as file:
                file.write(text)

class CommandLine:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('dir', help='Name of a directory for storing webpages data.')
        self.args = parser.parse_args()

    def get_argument(self):
        return self.args.dir

if __name__ == '__main__':
    Browser(CommandLine().get_argument())
