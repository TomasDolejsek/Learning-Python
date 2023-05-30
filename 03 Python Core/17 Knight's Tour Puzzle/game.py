class ChessBoardPiece:
    def __init__(self, pos_x, pos_y, name):
        self.x = pos_x
        self.y = pos_y
        self.name = name

class Knight(ChessBoardPiece):
    def __init__(self, x, y):
        super().__init__(x, y, 'X')
        self.possible_moves = list()
        self.find_possible_moves()

    def find_possible_moves(self):
        # tuple of deviations from a knight position for L-shape moves (columns, rows)
        pos_deviations = ((-1, 2), (1, 2), (2, -1), (2, 1), (1, -2), (-1, -2), (-2, 1), (-2, -1))
        self.possible_moves.clear()
        for dev in pos_deviations:
            test_pos = [self.x + dev[0], self.y + dev[1]]
            if (chess_board.columns >= test_pos[0] >= 1) and (self.rows >= test_pos[1] >= 1):
                self.possible_moves.append(test_pos)


class ChessBoard:
    def __init__(self, dimension, knight_pos):
        self.columns = dimension[0]
        self.rows = dimension[1]
        self.knight_pos = knight_pos
        self.possible_moves = list()
        self.find_possible_moves()
        self.board = [['0' * self.columns] * self.rows]
        self.display()

    def update_board(self):
        for i in range(self.rows):
            line = self.board[i]
            if self.knight_pos[]

    def display(self):
        cell_size = len(str(self.columns * self.rows))
        border_len = self.columns * (cell_size + 1) + 3
        knight = f"{' ' * (cell_size - 1)}" + 'X'
        move = f"{' ' * (cell_size - 1)}" + 'O'
        prefix_len = len(str(self.rows))
        knight_start = (cell_size + 1) * self.knight_pos[0] - len(knight)
        moves_lines = [x[1] for x in self.possible_moves]
        moves_columns = [x[0] for x in self.possible_moves]
        print(self.possible_moves, moves_lines)
        print(f"{' ' * prefix_len}{'-' * border_len}")
        for i in reversed(range(1, self.rows + 1)):
            line = f"{'_' * cell_size} " * self.columns
            if i in moves_lines:
                move_start = (cell_size + 1) * moves_columns[i] - len(move)
                line = self.rewrite_line(line, move_start, move)
            if i == self.knight_pos[1]:
                line = self.rewrite_line(line, knight_start, knight)
            print(f"{' ' * (prefix_len - len(str(i)))}{i}| {line}|")
        print(f"{' ' * prefix_len}{'-' * border_len}")
        print(' ' * (prefix_len + 1), end='')
        for i in range(1, self.columns + 1):
            print(f"{' ' * (cell_size - len(str(i)) + 1)}{i}", end='')

    def rewrite_line(self, line, pos, char):
        return line[:pos - 1] + char + line[pos - 1 + len(char):]





class UserInterface:
    def __init__(self):
        self.start()

    def start(self):
        while True:
            print("Enter your board dimensions: ", end='')
            dimen = self.check_input(input().split())
            if not dimen:
                print("Invalid dimensions!")
                continue
            break
        while True:
            print("Enter the knight's starting position: ", end='')
            knight_pos = self.check_input(input().split(), dimen)
            if not knight_pos:
                print("Invalid position!")
                continue
            break
        ChessBoard(dimen, knight_pos)

    def check_input(self, user, dim_limit=(20, 20)):
        try:
            if len(user) != 2:
                raise ValueError
            user = [int(x) for x in user]
            for i in range(2):
                if not (1 <= user[i] <= dim_limit[i]):
                    raise ValueError
            return user
        except ValueError:
            return False


if __name__ == '__main__':
    UserInterface()
