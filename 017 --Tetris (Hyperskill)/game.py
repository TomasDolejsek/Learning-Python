class GameOverException(Exception):
    def __init__(self):
        super().__init__("Game Over!")


class PlayField:
    def __init__(self, rows, columns):
        self.rows = rows
        self.columns = columns
        self.grid = ['-' * self.columns] * self.rows
        self.fixed_pixels = set()

    def display(self):
        for line in self.grid:
            line = map(lambda el: '0' if el == 'x' else el, line)
            print(' '.join(line))
        print()

    def update_grid(self, piece):
        if any(el >= (self.rows - 1) * self.columns for el in piece.actual_shape):
            piece.fixed = True
        if any(el + self.columns in self.fixed_pixels for el in piece.actual_shape):
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


class GamePiece:
    def __init__(self, shape, rows, columns):
        self.rows = rows
        self.columns = columns
        self.shape = shape.copy()
        self.rotation = 0
        self.fixed = False
        self.grid = list()
        self.update_piece()
        
    @property
    def actual_shape(self):
        return self.shape[self.rotation]
    
    @property
    def states(self):
        return len(self.shape)
    
    def update_piece(self):
        self.grid.clear()
        line = list()
        element = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if element not in self.actual_shape:
                    line.append('-')
                else:
                    line.append('0')
                element += 1
            self.grid.append(line.copy())
            line.clear()

    def rotate(self):
        if self.fixed:
            return
        self.rotation += 1
        if self.rotation > self.states - 1:
            self.rotation = 0
        self.update_piece()
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
        self.update_piece()
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
        self.update_piece()
        self.move_down()

    def move_down(self):
        if self.fixed:
            return
        for rot in range(self.states):
            line = [x + self.columns for x in self.shape[rot]]
            self.shape[rot] = line
        self.update_piece()


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
                    if user == 'exit':
                        exit()
        except GameOverException as exc:
            play_field.display()
            print(exc)


if __name__ == '__main__':
    grid_size = input().split()
    play_field = PlayField(int(grid_size[1]), int(grid_size[0]))
    Game()
