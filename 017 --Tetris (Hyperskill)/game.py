class Playfield:
    def __init__(self, shape, rows, columns):
        self.rows = rows
        self.columns = columns
        self.shape = shape
        self.rotation = 0
        self.states = len(self.shape)
        self.grid = list()
        self.redesign_piece_grid()

    def redesign_piece_grid(self):
        self.grid.clear()
        line = list()
        element = 0
        for i in range(self.rows):
            for j in range(self.columns):
                if element not in self.shape[self.rotation]:
                    line.append('-')
                else:
                    line.append('0')
                element += 1
            self.grid.append(line.copy())
            line.clear()

    def rotate(self):
        self.movedown()
        self.rotation += 1
        if self.rotation > self.states - 1:
            self.rotation = 0
        self.redesign_piece_grid()

    def moveleft(self):
        self.movedown()
        for rot in range(self.states):
            line = list(map(lambda x: x - 1 if (x - 1) % self.columns != self.columns - 1
                            else x + self.columns - 1, self.shape[rot]))
            self.shape[rot] = line
        self.redesign_piece_grid()
    
    def moveright(self):
        self.movedown()
        for rot in range(self.states):
            line = list(map(lambda x: x + 1 if (x + 1) % self.columns != 0
                            else x - self.columns + 1, self.shape[rot]))
            self.shape[rot] = line
        self.redesign_piece_grid()
        
    def movedown(self):
        for rot in range(self.states):
            line = list(map(lambda x: x + self.columns, self.shape[rot]))
            self.shape[rot] = line
        self.redesign_piece_grid()

    def display(self):
        for line in self.grid:
            print(*line, ' ')
        print()


class Game:
    def __init__(self):
        self.SHAPES = {'O': [[4, 14, 15, 5]],
                       'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
                       'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
                       'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
                       'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                       'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                       'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
        self.commands = ('rotate', 'left', 'right', 'down', 'exit')
        self.start()

    def start(self):
        shape = input().upper()
        grid_size = input().split()
        empty = Playfield([[-1, -1, -1, -1]], int(grid_size[1]), int(grid_size[0]))
        empty.display()
        piece = Playfield(self.SHAPES[shape], int(grid_size[1]), int(grid_size[0]))
        piece.display()
        while True:
            user = input().lower().strip()
            if user in self.commands:
                if user == 'rotate':
                    piece.rotate()
                    piece.display()
                if user == 'left':
                    piece.moveleft()
                    piece.display()
                if user == 'right':
                    piece.moveright()
                    piece.display()
                if user == 'down':
                    piece.movedown()
                    piece.display()
                if user == self.commands[-1]:
                    exit()


if __name__ == '__main__':
    Game()
