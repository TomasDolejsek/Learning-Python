class UserInterface:
    def __init__(self):
        self.data = list()
        self.start()

    def start(self):
        while True:
            try:
                self.data.extend(input().split())
            except EOFError:
                break
        print(f"Total numbers: {len(self.data)}")
        max_num = max(self.data)
        times = self.data.count(max_num)
        print(f"The greatest number: {max_num} ({times} time(s))")


if __name__ == '__main__':
    UserInterface()
