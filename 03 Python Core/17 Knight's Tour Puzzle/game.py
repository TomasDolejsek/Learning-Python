class ChessPiece:
    def __init__(self, pos_x, pos_y, mark):
        self.x = pos_x
        self.y = pos_y
        self.mark = mark


class Knight(ChessPiece):
    def __init__(self, pos):
        super().__init__(pos[0], pos[1], 'x')
        self.next_positions = list()
        self.visited_squares = [[self.x, self.y], ]
        self.pos_deviations = ((-1, 2), (1, 2), (2, 1), (2, -1),
                               (1, -2), (-1, -2), (-2, -1), (-2, 1))
        self.find_next_positions()

    @property
    def nmoves(self):
        return len(self.next_positions)

    def find_next_positions(self):
        self.next_positions.clear()
        for dev in self.pos_deviations:
            self.next_positions.append([self.x + dev[0], self.y + dev[1]])
        
    def validate_next_positions(self, max_x, max_y):
        temp_list = list()
        for pos in self.next_positions:
            if (1 <= pos[0] <= max_x and 1 <= pos[1] <= max_y) \
                 and pos not in self.visited_squares:
                temp_list.append(pos)
        self.next_positions = temp_list


class ChessBoard:
    def __init__(self, dimensions, start_position):
        self.columns = dimensions[0]
        self.rows = dimensions[1]
        self.knight = Knight(start_position)
        self.knight.validate_next_positions(self.columns, self.rows)
        self.pieces = [self.knight, ]
        self.board = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.start()

    def start(self):
        for pos in self.pieces[0].next_positions:
            new_knight = Knight(pos)
            new_knight.validate_next_positions(self.columns, self.rows)
            new_knight.mark = str(new_knight.nmoves)
            self.pieces.append(new_knight)
        self.update_board()
        self.display()

    def update_board(self):
        for piece in self.pieces:
            self.board[piece.x - 1][piece.y - 1] = piece.mark

    def display(self):
        cell_size = len(str(self.columns * self.rows))
        border_len = self.columns * (cell_size + 1) + 3
        prefix_len = len(str(self.rows))
        border = f"{' ' * prefix_len}{'-' * border_len}"
        print(border)
        for y in reversed(range(1, self.rows + 1)):
            line = f"{' ' * (prefix_len - len(str(y)))}{y}| "
            for x in range(1, self.columns + 1):
                if not self.board[x - 1][y - 1]:
                    line += f"{'_' * cell_size} "
                else:
                    line += f"{' ' * (cell_size - 1)}{self.board[x - 1][y- 1]} "
            line += '|'
            print(line)
        print(border)
        print(' ' * (prefix_len + 1), end='')
        for x in range(1, self.columns + 1):
            print(f"{' ' * (cell_size - len(str(x)) + 1)}{x}", end='')


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
        chessboard = ChessBoard(dimen, knight_pos)

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
