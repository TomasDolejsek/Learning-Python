import numpy as np


class UserInterface:
    def __init__(self):
        self.start()

    def start(self):
        matrix_a = list()
        rows, columns = [int(x) for x in input().split()]
        for _ in range(rows):
            row = [int(x) for x in input().split()]
            matrix_a.append(row)
        constant = int(input())
        m_a = np.array(matrix_a)
        m_a = constant * m_a
        for row in m_a:
            print(*row, sep=' ')


if __name__ == '__main__':
    UserInterface()
