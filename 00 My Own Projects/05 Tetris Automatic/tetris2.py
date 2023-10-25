import time
import random
import pygame
from os import system


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
        self.score = 0

    def display(self):
        system('cls')
        print("Use arrow keys to move, esc to quit the game.")
        print("Your score:", self.score)
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

    def remove_line(self):
        for i in range(len(self.grid)):
            line = self.grid[i]
            if any(el != 'x' for el in line):
                continue
            empty_line = '-' * self.columns
            del self.grid[i]
            self.grid.insert(0, empty_line)
            new_set = set()
            for el in self.fixed_pixels:
                if el < i * self.columns:
                    new_set.add(el + self.columns)
                elif el >= (i + 1) * self.columns:
                    new_set.add(el)
            self.fixed_pixels = new_set
            self.broken_line = True
            self.score += 1
            self.remove_line()
            break


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
        next_rot = self.rotation + 1 if self.rotation + 1 <= self.states - 1 else 0
        next_shape = self.shape[next_rot]
        for el, nextel in zip(self.actual_shape, next_shape):
            if abs(el % self.columns - nextel % self.columns) > 5:
                return
        self.rotation += 1
        if self.rotation > self.states - 1:
            self.rotation = 0
        play_field.update_grid(self)
        play_field.display()

    def move_left(self):
        if self.fixed:
            return
        if any((el - 1) % self.columns == self.columns - 1 for el in self.actual_shape):
            return
        for rot in range(self.states):
            line = [el - 1 if (el - 1) % self.columns != self.columns - 1
                    else el + self.columns - 1 for el in self.shape[rot]]
            self.shape[rot] = line
        play_field.update_grid(self)
        play_field.display()

    def move_right(self):
        if self.fixed:
            return
        if any((el + 1) % self.columns == 0 for el in self.actual_shape):
            return
        for rot in range(self.states):
            line = [el + 1 if (el + 1) % self.columns != 0
                    else el - self.columns + 1 for el in self.shape[rot]]
            self.shape[rot] = line
        play_field.update_grid(self)
        play_field.display()

    def move_down(self):
        if self.fixed:
            return
        if any(el + self.columns in play_field.fixed_pixels for el in self.actual_shape):
            self.fixed = True
            play_field.update_grid(self)
            return
        for rot in range(self.states):
            line = [x + self.columns for x in self.shape[rot]]
            self.shape[rot] = line
        self.moves += 1
        play_field.update_grid(self)
        play_field.remove_line()
        play_field.display()


class Game:
    def __init__(self):
        self.SHAPES = {'O': [[4, 14, 15, 5]],
                       'I': [[4, 14, 24, 34], [3, 4, 5, 6]],
                       'S': [[5, 4, 14, 13], [4, 14, 15, 25]],
                       'Z': [[4, 5, 15, 16], [5, 15, 14, 24]],
                       'L': [[4, 14, 24, 25], [5, 15, 14, 13], [4, 5, 15, 25], [6, 5, 4, 14]],
                       'J': [[5, 15, 25, 24], [15, 5, 4, 3], [5, 4, 14, 24], [4, 14, 15, 16]],
                       'T': [[4, 14, 24, 15], [4, 13, 14, 15], [5, 15, 25, 14], [4, 5, 6, 15]]}
        self.TICK = 0.2
        self.start()

    def start(self):
        print("Tetris 2.0 with automatic movement.")
        piece = None
        pygame.init()
        pygame.display.set_mode((1, 1))
        try:
            while True:
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            piece.rotate()
                        if event.key == pygame.K_LEFT:
                            piece.move_left()
                        if event.key == pygame.K_RIGHT:
                            piece.move_right()
                        if event.key == pygame.K_DOWN:
                            piece.move_down()
                        if event.key == pygame.K_ESCAPE:
                            raise GameOverException
                if piece is None or piece.fixed:
                    shape = random.choice(list(self.SHAPES.keys()))
                    piece = GamePiece(self.SHAPES[shape], int(grid_size[0]), int(grid_size[1]))
                    play_field.update_grid(piece)
                    play_field.display()
                time.sleep(self.TICK)
                piece.move_down()
        except GameOverException as exc:
            play_field.display()
            print(exc)


if __name__ == '__main__':
    grid_size = (20, 10)
    play_field = PlayField(grid_size[0], grid_size[1])
    Game()
