import argparse
from math import floor


class SortTool:
    def __init__(self, data, data_type):
        self.data = data
        self.data_type = data_type
        if self.data_type == 'long':
            self.numerize_data()
        self.length = len(self.data)
        self.logger = ''

    def numerize_data(self):
        numeric_data = list()
        for num in self.data:
            try:
                numeric_data.append(int(num))
            except ValueError:
                print(f"\"{num}\" is not a long. It will be skipped.")
                continue
        self.data = numeric_data

    def sort_it_out(self, sort_how):
        item = 'number' if self.data_type == 'long' else self.data_type
        self.logger += f"Total {item}s: {self.length}\n"
        if sort_how == 'natural':
            self.sort_natural(self.data)
        elif sort_how == 'byCount':
            self.sort_by_count(self.data)
        return self.logger

    def sort_natural(self, data):
        separator = '\n' if self.data_type == 'line' else ' '
        self.logger += "Sorted data:" + separator
        self.logger += separator.join([str(x) for x in sorted(data)])

    def sort_by_count(self, data):
        counts = dict()
        for el in sorted(data):
            if el not in counts:
                counts[el] = [data.count(el), floor(data.count(el) / self.length * 100)]
        counts = sorted(counts.items(), key=lambda x: x[1])
        for count in counts:
            self.logger += f"{count[0]}: {count[1][0]} time(s), {count[1][1]}%\n"


class UserInterface:
    def __init__(self):
        args = self.get_arguments()
        self.data_type = args.dataType
        self.sorting_type = args.sortingType
        self.infile = args.inputFile
        self.outfile = args.outputFile
        self.start()

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('-dataType', choices=['long', 'line', 'word'],
                            required=False, default='word', nargs='?')
        parser.add_argument('-sortingType', choices=['natural', 'byCount'],
                            required=False, default='natural', nargs='?')
        parser.add_argument('-inputFile', required=False, default=None)
        parser.add_argument('-outputFile', required=False, default=None)
        args, unknowns = parser.parse_known_args()
        if not args.dataType:
            print("No data type defined!")
            exit()
        if not args.sortingType:
            print("No sorting type defined!")
            exit()
        for unknown in unknowns:
            print(f"\"{unknown}\" is not a valid parameter. It will be skipped.")
        return args

    def start(self):
        separator = '\n' if self.data_type == 'line' else None
        data = list()
        if self.infile:
            with open(self.infile, 'rt') as file:
                data = file.read().split(separator)
        else:
            while True:
                try:
                    data.extend(input().split(separator))
                except EOFError:
                    break
        sort_tool = SortTool(data, self.data_type)
        output_text = sort_tool.sort_it_out(self.sorting_type)
        if self.outfile:
            with open(self.outfile, 'wt') as file:
                file.write(output_text)
        else:
            print(output_text)
        

if __name__ == '__main__':
    UserInterface()
