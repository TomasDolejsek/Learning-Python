class ChessBoard:
    def __init__(self, knight_pos):
        self.knight_pos = knight_pos
        self.display()

    def display(self):
        print(f" {'-' * 19}")
        for i in reversed(range(1, 9)):
            line = '_ ' * 8
            if i == self.knight_pos[1]:
                line = line[:(self.knight_pos[0] * 2) - 2] + 'X' + line[(self.knight_pos[0] * 2) - 1:]
            print(f"{i}| {line}|")
        print(f" {'-' * 19}")
        print("   1 2 3 4 5 6 7 8")


class UserInterface:
    def __init__(self):
        self.start()

    def start(self):
        knight_pos = input("Enter the knight's starting position: ").split()
        try:
            if len(knight_pos) != 2:
                raise ValueError
            knight_pos = [int(x) for x in knight_pos]
            for el in knight_pos:
                if not (1 <= el <= 8):
                    raise ValueError
        except ValueError:
            print("Invalid dimensions!")
            exit()
        ChessBoard(knight_pos)


if __name__ == '__main__':
    UserInterface()
