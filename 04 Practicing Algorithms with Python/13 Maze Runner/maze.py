from random import randint, choice
from os.path import exists
from sys import setrecursionlimit
import dill


class Maze:
    def __init__(self, y=10, x=10):
        self.max_x = x
        self.max_y = y
        self.char = {0: '  ', 1: '\u2588\u2588', 2: '//'}
        self.path = list()
        self.adjacency_list = dict()
        self.escape = list()
        self.generate_maze()

    def generate_maze(self, verbose=False):
        frontiers = dict()
        first_cell = (randint(1, self.max_x - 2), randint(1, self.max_y - 2))
        self.path.append(first_cell)
        frontiers.update(self.find_frontiers(first_cell))
        while frontiers:
            frontier = choice(tuple(frontiers))
            self.connect_to_path(frontiers[frontier], frontier)
            del frontiers[frontier]
            frontiers.update(self.find_frontiers(frontier))
            if verbose:
                self.display()
        self.create_exits()
        self.path.sort(key=lambda x: (x[0], x[1]))

    def find_frontiers(self, cell):
        steps = ([0, 2], [2, 0], [0, -2], [-2, 0])
        new_frontiers = dict()
        for step in steps:
            front_x = cell[0] + step[0]
            front_y = cell[1] + step[1]
            if 1 <= front_x <= self.max_x - 2 and 1 <= front_y <= self.max_y - 2 \
                    and (front_x, front_y) not in self.path:
                new_frontiers[(front_x, front_y)] = cell
        return new_frontiers

    def connect_to_path(self, path_cell, frontier):
        x = min(path_cell[0], frontier[0])
        y = min(path_cell[1], frontier[1])
        if path_cell[0] == frontier[0]:
            self.path.append((path_cell[0], y + 1))
        else:
            self.path.append((x + 1, path_cell[1]))
        self.path.append(frontier)

    def create_exits(self):
        wall = min([cell[0] for cell in self.path])
        wall_cells = [x for x in self.path if x[0] == wall]
        doors = choice(wall_cells)
        for x in range(doors[0]):
            self.path.append((x, doors[1]))
        wall = max([cell[0] for cell in self.path])
        wall_cells = [x for x in self.path if x[0] == wall]
        doors = choice(wall_cells)
        for x in range(doors[0] + 1, self.max_x):
            self.path.append((x, doors[1]))

    def create_adjacency_list(self):
        for cell in self.path:
            neighbours = [el for el in self.path if (el[0] == cell[0] and abs(el[1] - cell[1]) == 1)
                          or (el[1] == cell[1] and abs(el[0] - cell[0]) == 1)]
            self.adjacency_list[cell] = neighbours

    def find_escape(self):
        self.create_adjacency_list()
        self.go_to_next_cell(self.path[0])
        self.display()
        self.escape.clear()
        self.adjacency_list.clear()

    def go_to_next_cell(self, cell):
        self.escape.append(cell)
        while cell[0] == self.max_x - 1:
            return
        for key, el in self.adjacency_list.items():
            if cell in el:
                el.remove(cell)
                self.adjacency_list[key] = el
        neighbours = self.adjacency_list[cell]
        if not neighbours:
            self.escape.pop()
            next_cell = self.escape.pop()
        else:
            next_cell = neighbours.pop()
            self.adjacency_list[cell] = neighbours
        self.go_to_next_cell(next_cell)

    def display(self):
        for y in range(self.max_y):
            for x in range(self.max_x):
                if (x, y) in self.escape:
                    print(self.char[2], end='')
                elif (x, y) in self.path:
                    print(self.char[0], end='')
                else:
                    print(self.char[1], end='')
            print()


class UserInterface:
    def __init__(self):
        self.options = {'1': 'Generate a new maze',
                        '2': 'Load a maze',
                        '0': 'Exit'}
        self.add_options = {'3': 'Save the maze',
                            '4': 'Display the maze',
                            '5': 'Find the escape',
                            '0': 'Exit'}
        self.start()

    def start(self):
        while True:
            print("=== Menu ===")
            for num, text in self.options.items():
                print(f"{num}. {text}")
            user = input().strip()
            if user not in self.options:
                print("Incorrect option. Please try again")
                continue
            if user == '1':
                print("Enter the size of a new maze")
                size = int(input())
                maze = Maze(size, size)
                maze.display()
                del self.options['0']
                self.options.update(self.add_options)
                continue
            if user == '2':
                file_name = input()
                if not exists(file_name):
                    print(f"The file {file_name} does not exist")
                    continue
                try:
                    with open(file_name, 'rb') as file:
                        maze = dill.load(file)
                except dill.UnpicklingError:
                    print("Cannot load the maze. It has an invalid format")
                    continue
                del self.options['0']
                self.options.update(self.add_options)
                continue
            if user == '3':
                file_name = input()
                with open(file_name, 'wb') as file:
                    dill.dump(maze, file)
                continue
            if user == '4':
                maze.display()
                continue
            if user == '5':
                maze.find_escape()
            if user == '0':
                print("Bye!")
                exit()


if __name__ == '__main__':
    setrecursionlimit(3000)
    UserInterface()
