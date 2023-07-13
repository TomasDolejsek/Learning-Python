class Movies:
    def __init__(self):
        self.MOVIES_FILENAME = 'Data/movies.csv'
        self.movies = []
        self.start()

    def start(self):
        with open(self.MOVIES_FILENAME, 'rt', encoding='UTF-8') as file:
            for line in file:
                data = line.rsplit(',', 1)
                name = data[0].replace('"', '')
                rating = float(data[1].replace('\n', ''))
                self.movies.append([name, rating])
        #sorted_movies = self.bubble_sort(self.movies)
        sorted_movies = self.merge_sort(self.movies)
        self.binary_search(sorted_movies)

    def merge_sort(self, data):
        if len(data) > 1:
            middle = len(data) // 2
            left = data[:middle]
            right = data[middle:]
            self.merge_sort(left)
            self.merge_sort(right)
            i = j = k = 0
            while i < len(left) and j < len(right):
                if left[i][1] <= right[j][1]:
                    data[k] = left[i]
                    i += 1
                else:
                    data[k] = right[j]
                    j += 1
                k += 1
            while i < len(left):
                data[k] = left[i]
                i += 1
                k += 1
            while j < len(right):
                data[k] = right[j]
                j += 1
                k += 1
        return data

    @staticmethod
    def bubble_sort(data):
        nelements = len(data)
        i = 0
        while i < nelements - 1:
            for j in range(nelements - 1):
                if data[j][1] > data[j + 1][1]:
                    temp = data[j]
                    data[j] = data[j + 1]
                    data[j + 1] = temp
            i += 1
        return data

    @staticmethod
    def binary_search(data):
        low = 0
        high = len(data) - 1
        while True:
            middle = (low + high) // 2
            if data[middle][1] < 6:
                low = middle + 1
            elif data[middle][1] > 6:
                high = middle - 1
            else:
                low_index = middle
                high_index = middle
                while data[low_index - 1][1] == 6:
                    low_index -= 1
                while data[high_index + 1][1] == 6:
                    high_index += 1
                for i in range(low_index, high_index + 1):
                    print(f"{data[i][0]} - {data[i][1]}")
                break


if __name__ == '__main__':
    Movies()
