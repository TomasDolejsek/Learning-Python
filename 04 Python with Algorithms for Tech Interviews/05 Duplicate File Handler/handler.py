import argparse
import os
import hashlib


class FileHandler:
    def __init__(self, root, file_format, order):
        self.data = self.sort_data(self.get_files_data(root, file_format), order)
        self.duplicates = dict()

    def get_files_data(self, directory, extension):
        files_data = dict()
        for root, dirs, files in os.walk(directory, topdown=False):
            for name in files:
                if name.endswith(extension):
                    full_path = os.path.join(root, name)
                    files_data[full_path] = [os.path.getsize(full_path), self.hash_file(full_path)]
        return files_data

    @staticmethod
    def sort_data(data, order):
        if order == '1':
            sorted_data = sorted(data.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
        else:
            sorted_data = sorted(data.items(), key=lambda x: (x[1][0], x[1][1]), reverse=False)
        return dict(sorted_data)

    @staticmethod
    def hash_file(file_name):
        with open(file_name, 'rb') as file:
            hash_obj = hashlib.md5(file.read())
        return hash_obj.hexdigest()

    def group_by_size(self):
        size = 0
        for file_name, file_data in self.data.items():
            if file_data[0] != size:
                size = file_data[0]
                print(f"\n{size} bytes")
            print(file_name)

    def group_by_hash(self):
        size = 0
        hexa_hash = 0
        number = 0
        hashes = [x[1] for x in self.data.values()]
        hash_dict = {h: hashes.count(h) for h in hashes}
        for file_name, file_data in self.data.items():
            if hash_dict[file_data[1]] > 1:
                number += 1
                if file_data[0] != size:
                    size = file_data[0]
                    print(f"\n{size} bytes")
                if file_data[1] != hexa_hash:
                    hexa_hash = file_data[1]
                    print(f"Hash: {hexa_hash}")
                print(f"{number}. {file_name}")
                self.duplicates[str(number)] = [file_name, file_data[0]]

    def delete_duplicates(self, file_numbers):
        freed = 0
        for number in file_numbers:
            freed += self.duplicates[number][1]
            os.remove(self.duplicates[number][0])
        print(f"\nTotal freed up space: {freed} bytes")


class UserInterface:
    def __init__(self):
        self.start()

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser()
        parser.add_argument('folder', nargs='?')
        args = parser.parse_args()
        if not args.folder:
            print("Directory is not specified")
            exit()
        return args

    def start(self):
        root = self.get_arguments().folder
        print("Enter file format:")
        file_format = input().strip()
        print("Size sorting options:")
        print("1. Descending")
        print("2. Ascending")
        while True:
            print("\nEnter sorting option:")
            order = input().strip()
            if order not in ['1', '2']:
                print("\nWrong option")
                continue
            break
        handler = FileHandler(root, file_format, order)
        handler.group_by_size()
        while True:
            print("\nCheck for duplicates?")
            dupl = input().lower().strip()
            if dupl not in ['yes', 'no']:
                print("\nWrong option")
                continue
            break
        if dupl == 'yes':
            handler.group_by_hash()
        else:
            exit()
        while True:
            print("Delete files?")
            delete = input().strip()
            if delete not in ['yes', 'no']:
                print("Wrong option")
                continue
            break
        if delete == 'yes':
            while True:
                print("\nEnter file numbers to delete:")
                file_numbers = input().split()
                if not file_numbers or any([x not in handler.duplicates for x in file_numbers]):
                    print("\nWrong format")
                    continue
                break
            handler.delete_duplicates(file_numbers)


if __name__ == "__main__":
    UserInterface()
