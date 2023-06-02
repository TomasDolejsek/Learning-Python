import argparse
from math import floor


class SortTool:
    def __init__(self, data, data_type):
        self.data = data
        self.ntotal = len(self.data)
        self.data_type = 'number' if data_type == 'long' else data_type

    def sort_it_out(self, sort_how):
        print(f"Total {self.data_type}s: {self.ntotal}")
        data = [int(x) for x in self.data] if self.data_type == 'number' else self.data
        if sort_how == 'natural':
            self.sort_natural(data)
        elif sort_how == 'byCount':
            self.sort_by_count(data)

    def sort_natural(self, data):
        data.sort()
        separator = '\n' if self.data_type == 'line' else ' '
        print("Sorted data:", *data, sep=separator)

    def sort_by_count(self, data):
        counts = dict()
        data.sort()
        for el in data:
            if el not in counts:
                counts[el] = [data.count(el), floor(data.count(el) / self.ntotal * 100)]
        counts = sorted(counts.items(), key=lambda x: x[1])
        for count in counts:
            print(f"{count[0]}: {count[1][0]} time(s), {count[1][1]}%")


class UserInterface:
    def __init__(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-dataType', 
                            required=False, default='word')
        parser.add_argument('-sortingType', choices=['natural', 'byCount'],
                            required=False, default='natural')
        args = parser.parse_args()
        self.data_type = args.dataType
        self.sorting_type = args.sortingType
        self.start()

    def start(self):
        separator = '\n' if self.data_type == 'line' else None
        data = list()
        while True:
            try:
                data.extend(input().split(separator))
            except EOFError:
                break
        sort_tool = SortTool(data, self.data_type)
        sort_tool.sort_it_out(self.sorting_type)
        

if __name__ == '__main__':
    UserInterface()
