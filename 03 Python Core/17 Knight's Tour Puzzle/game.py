class ChessPiece:
    def __init__(self, pos_x, pos_y, mark):
        self.x = pos_x
        self.y = pos_y
        self.mark = mark


class Knight(ChessPiece):
    def __init__(self, pos):
        super().__init__(pos[0], pos[1], 'x')
        self.next_positions = list()
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

    def validate_next_positions(self, max_x, max_y, visited):
        temp_list = list()
        for pos in self.next_positions:
            if (1 <= pos[0] <= max_x and 1 <= pos[1] <= max_y) \
                 and pos not in visited:
                temp_list.append(pos)
        self.next_positions = temp_list

    def move(self, where):
        self.x = where[0]
        self.y = where[1]
        self.find_next_positions()


class ChessBoard:
    def __init__(self, dimensions, start_position):
        self.columns = dimensions[0]
        self.rows = dimensions[1]
        self.knight = Knight(start_position)
        self.visited_squares = [[self.knight.x, self.knight.y], ]
        self.knight.validate_next_positions(self.columns, self.rows, self.visited_squares)
        self.pieces = [self.knight, ]
        self.board = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        self.create_adjacents()

    @property
    def nvisited(self):
        return len(self.visited_squares)

    @property
    def more_moves(self):
        return self.knight.nmoves > 0

    @property
    def all_visited(self):
        return self.nvisited == self.columns * self.rows

    def create_adjacents(self):
        for pos in self.pieces[0].next_positions:
            new_knight = Knight(pos)
            new_knight.validate_next_positions(self.columns, self.rows, self.visited_squares)
            new_knight.mark = str(new_knight.nmoves)
            self.pieces.append(new_knight)
        self.update_board()
        self.display()

    def move_knight(self, new_pos):
        self.pieces = self.pieces[:1]
        self.visited_squares.append(new_pos)
        self.knight.move(new_pos)
        self.knight.validate_next_positions(self.columns, self.rows, self.visited_squares)
        self.create_adjacents()

    def move_ok(self, where):
        return where in self.knight.next_positions

    def update_board(self):
        self.board = [[None for _ in range(self.rows)] for _ in range(self.columns)]
        for pos in self.visited_squares:
            self.board[pos[0] - 1][pos[1] - 1] = '*'
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
        print()


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
        while chessboard.more_moves:
            while True:
                print("Enter your next move: ", end='')
                next_move = self.check_input(input().split(), dimen)
                if not next_move or not chessboard.move_ok(next_move):
                    print("Invalid move!")
                    continue
                break
            chessboard.move_knight(next_move)
        if chessboard.all_visited:
            print("What a great tour! Congratulations!")
        else:
            print("No more possible moves!")
            print(f"Your knight visited {chessboard.nvisited} squares!")

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
