import numpy as np


class UserInterface:
    def __init__(self):
        self.start()

    def start(self):
        matrix_A = list()
        matrix_B = list()
        rows, columns = input().split()
        for i in range(int(rows)):
            row = [int(x) for x in input().split()]
            matrix_A.append(row)
        rows, columns = input().split()
        for i in range(int(rows)):
            row = [int(x) for x in input().split()]
            matrix_B.append(row)
        m_a = np.array(matrix_A)
        m_b = np.array(matrix_B)
        if m_a.shape == m_b.shape:
            m_c = m_a + m_b
            

        else:
            print("Error")


if __name__ == '__main__':
    UserInterface()
