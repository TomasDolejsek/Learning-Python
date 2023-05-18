class GameOverException(Exception):
    def __init__(self):
        super().__init__("Game Over!")


class PlayField:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = ['-' * self.columns] * self.rows
        self.fixed_pixels = set()
        self.broken_line = False

    def display(self):
        for line in self.grid:
            line = map(lambda el: '0' if el == 'x' else el, line)
            print(' '.join(line))
        print()

    def update_grid(self, piece):
        if self.broken_line:
            return
        if any(el >= (self.rows - 1) * self.columns for el in piece.actual_shape):
            if piece.moves > 0:
                piece.fixed = True
        if any(el + self.columns in self.fixed_pixels for el in piece.actual_shape):
            if piece.moves > 0:
                piece.fixed = True
        if piece.fixed:
            self.fixed_pixels.update(piece.actual_shape)
        element = 0
        for i in range(self.rows):
            new_line = ''
            for j in range(self.columns):
                if element in piece.actual_shape \
                 or element in self.fixed_pixels:
                    if element in self.fixed_pixels:
                        new_line += 'x'
                    else:
                        new_line += '0'
                else:
                    new_line += '-'
                element += 1
            self.grid[i] = new_line
        if any(num <= self.columns - 1 for num in self.fixed_pixels):
            raise GameOverException

    def remove_bottom_line(self):
        bottom_line = self.grid[self.rows - 1]
        if any(el != 'x' for el in bottom_line):
            return
        empty_line = '-' * self.columns
        self.grid.pop()
        self.grid.insert(0, empty_line)
        new_set = set()
        for el in self.fixed_pixels:
            if el < (self.rows - 1) * self.columns:
                new_set.add(el + self.columns)
        self.fixed_pixels = new_set
        self.broken_line = True
        self.remove_bottom_line()


class GamePiece:
    def __init__(self, shape, rows, columns):
        self.rows = rows
        self.columns = columns
        self.shape = shape.copy()
        self.states = len(self.shape)
        self.rotation = 0
        self.moves = 0
        self.fixed = False
        play_field.broken_line = False

    @property
    def actual_shape(self):
        return self.shape[self.rotation]

    def rotate(self):
        if self.fixed:
            return
        self.rotation += 1
        if self.rotation > self.states - 1:
            self.rotation = 0
        self.move_down()

    def move_left(self):
        if self.fixed:
            return
        if any((el - 1) % self.columns == self.columns - 1 for el in self.actual_shape):
            self.move_down()
            return
        for rot in range(self.states):
            line = [el - 1 if (el - 1) % self.columns != self.columns - 1
                    else el + self.columns - 1 for el in self.shape[rot]]
            self.shape[rot] = line
        self.move_down()

    def move_right(self):
        if self.fixed:
            return
        if any((el + 1) % self.columns == 0 for el in self.actual_shape):
            self.move_down()
            return
        for rot in range(self.states):
            line = [el + 1 if (el + 1) % self.columns != 0
                    else el - self.columns + 1 for el in self.shape[rot]]
            self.shape[rot] = line
        self.move_down()

    def move_down(self):
        if self.fixed:
            return
        if any(el + self.columns in play_field.fixed_pixels for el in self.actual_shape):
            self.fixed = True
            return
        for rot in range(self.states):
            line = [x + self.columns for x in self.shape[rot]]
            self.shape[rot] = line
        self.moves += 1


class Game:
    def __init__(self):
        self.SHAPES = {'O': [[4, 14, 15, 5]],
                       'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
                       'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
                       'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
                       'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                       'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                       'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
        self.commands = ('piece', 'rotate', 'left', 'right', 'down', 'break', 'exit')
        self.start()

    def start(self):
        play_field.display()
        piece = None
        try:
            while True:
                user = input().lower().strip()
                if user in self.commands:
                    if user == 'piece':
                        shape = input().upper().strip()
                        if shape not in self.SHAPES.keys():
                            continue
                        piece = GamePiece(self.SHAPES[shape], int(grid_size[1]), int(grid_size[0]))
                        play_field.update_grid(piece)
                        play_field.display()
                    if user == 'rotate':
                        piece.rotate()
                        play_field.update_grid(piece)
                        play_field.display()
                    if user == 'left':
                        piece.move_left()
                        play_field.update_grid(piece)
                        play_field.display()
                    if user == 'right':
                        piece.move_right()
                        play_field.update_grid(piece)
                        play_field.display()
                    if user == 'down':
                        piece.move_down()
                        play_field.update_grid(piece)
                        play_field.display()
                    if user == 'break':
                        play_field.remove_bottom_line()
                        play_field.display()
                    if user == 'exit':
                        exit()
        except GameOverException as exc:
            play_field.display()
            print(exc)


if __name__ == '__main__':
    grid_size = input().split()
    play_field = PlayField(int(grid_size[1]), int(grid_size[0]))
    Game()
