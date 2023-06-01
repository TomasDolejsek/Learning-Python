import argparse
from math import floor


class SortTool:
    def process_numbers(self, data):
        print(f"Total numbers: {len(data)}")
        max_num = max(data)
        times = data.count(max_num)
        percent = floor(times / len(data) * 100)
        print(f"The greatest number: {max_num} ({times} time(s), {percent}%)")

    def process_lines(self, data):
        print(f"Total words: {len(data)}")
        max_len = sorted(data, key=len, reverse=True)[0]
        times = data.count(max_len)
        percent = floor(times / len(data) * 100)
        print(f"The longest line:\n{max_len}\n({times} time(s), {percent}%)")

    def process_words(self, data):
        print(f"Total words: {len(data)}")
        max_len = sorted(data, key=len, reverse=True)[0]
        times = data.count(max_len)
        percent = floor(times / len(data) * 100)
        print(f"The longest word: {max_len} ({times} time(s), {percent}%)")


class UserInterface:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-dataType', choices = ['long', 'line', 'word'])
        args = parser.parse_args()
        if not args:
            self.input_type = 'word'
        else:
            self.input_type = args.dataType
        self.data  = list()
        self.start()

    def start(self):
        sort_tool = SortTool()
        while True:
            try:
                if self.input_type == 'line':
                    self.data.extend(input().splitlines())
                else:
                    self.data.extend(input().split())
            except EOFError:
                break
        if self.input_type == 'long':
            sort_tool.process_numbers(self.data)
        elif self.input_type == 'line':
            sort_tool.process_lines(self.data)
        else:
            sort_tool.process_words(self.data)


if __name__ == '__main__':
    UserInterface()
