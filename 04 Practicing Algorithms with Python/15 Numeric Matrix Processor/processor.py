from numpy import shape


class MatrixProcessor:
    def define_matrix(self, word):
        matrix = []
        print(f"Enter size of {word} matrix: ", end='')
        rows, columns = [int(x) for x in input().split()]
        print(f"Enter {word} matrix:")
        for _ in range(rows):
            row = [float(x) for x in input().split()]
            matrix.append(row[:columns])
        return matrix

    def add(self, m_a=None, m_b=None):
        if not m_a:
            m_a = self.define_matrix('first')
        if not m_b:
            m_b = self.define_matrix('second')
        if shape(m_a) == shape(m_b):
            m_c = [[x + y for x, y in zip(row_a, row_b)] for row_a, row_b in zip(m_a, m_b)]
            return m_c
        else:
            return "The operation cannot be performed.\n"

    def constant_multiply(self, constant=None, m_a=None):
        if not m_a:
            m_a = self.define_matrix('the')
        if not constant:
            constant = float(input("Enter constant: "))
        m_b = [[constant * x for x in row] for row in m_a]
        return m_b

    def matrices_multiply(self, m_a=None, m_b=None):
        if not m_a:
            m_a = self.define_matrix('first')
        if not m_b:
            m_b = self.define_matrix('second')
        rows_a = len(m_a)
        cols_a = len(m_a[0])
        rows_b = len(m_b)
        cols_b = len(m_b[0])
        m_c = []
        if cols_a == rows_b:
            for i in range(rows_a):
                new_row = []
                for j in range(cols_b):
                    element = 0
                    for k in range(cols_a):
                        element += m_a[i][k] * m_b[k][j]
                    new_row.append(element)
                m_c.append(new_row)
            return m_c
        else:
            return "The operation cannot be performed.\n"

    def transpose(self, along, m_a=None):
        if not m_a:
            m_a = self.define_matrix('the')
        rows = len(m_a)
        cols = len(m_a[0])
        m_b = []
        if along == '1':
            for j in range(cols):
                new_row = []
                for i in range(rows):
                    new_row.append(m_a[i][j])
                m_b.append(new_row)
        elif along == '2':
            for j in reversed(range(cols)):
                new_row = []
                for i in reversed(range(rows)):
                    new_row.append(m_a[i][j])
                m_b.append(new_row)
        elif along == '3':
            for row in m_a:
                new_row = []
                for j in reversed(range(cols)):
                    new_row.append(row[j])
                m_b.append(new_row)
        elif along == '4':
            for row in reversed(m_a):
                m_b.append(row)
        return m_b

    def determinant(self, m_a=None):
        if not m_a:
            m_a = self.define_matrix('the')
        rows = len(m_a)
        cols = len(m_a[0])
        if rows == cols:
            if rows == 1:
                return m_a[0][0]
            if rows == 2:
                return m_a[0][0] * m_a[1][1] - m_a[1][0] * m_a[0][1]
            else:
                det = 0
                for j in range(cols):
                    det += m_a[0][j] * self.cofactor(m_a, 0, j)
                return det
        else:
            return "The operation cannot be performed.\n"

    def inverse(self, m_a=None):
        if not m_a:
            m_a = self.define_matrix('the')
        rows = len(m_a)
        cols = len(m_a[0])
        det_a = self.determinant(m_a)
        if det_a != 0:
            m_b = []
            for i in range(rows):
                new_row = []
                for j in range(cols):
                    new_row.append(self.cofactor(m_a, i, j))
                m_b.append(new_row)
            return self.constant_multiply((1 / det_a), self.transpose('1', m_b))
        else:
            return "This matrix doesn't have an inverse.\n"

    def submatrix(self, matrix, i, j):
        size = len(matrix)
        sub = [[matrix[y][x] for x in range(size) if (y != i and x != j)] for y in range(size)]
        sub.remove([])
        return sub

    def cofactor(self, matrix, i, j):
        sign = (-1) ** (i + j)
        minor = self.determinant(self.submatrix(matrix, i, j))
        return sign * minor


class UserInterface:
    def __init__(self):
        self.menu = {'1': 'Add matrices',
                     '2': 'Multiply matrix by a constant',
                     '3': 'Multiply matrices',
                     '4': 'Transpose matrix',
                     '5': 'Calculate a determinant',
                     '6': 'Inverse matrix',
                     '0': 'Exit'}
        self.start()

    def start(self):
        processor = MatrixProcessor()
        while True:
            for num, choice in self.menu.items():
                print(f"{num}. {choice}")
            command = input("Your choice: ")
            if command == '1':
                self.print_result(processor.add())
                continue
            if command == '2':
                self.print_result(processor.constant_multiply())
                continue
            if command == '3':
                self.print_result(processor.matrices_multiply())
                continue
            if command == '4':
                along = self.transpose_menu()
                self.print_result(processor.transpose(along))
                continue
            if command == '5':
                self.print_result([[processor.determinant()], ])
                continue
            if command == '6':
                self.print_result(processor.inverse())
                continue
            if command == '0':
                break

    def transpose_menu(self):
        menu = {'1': 'Main diagonal',
                '2': 'Side diagonal',
                '3': 'Vertical line',
                '4': 'Horizontal line'}
        for num, choice in menu.items():
            print(f"{num}. {choice}")
        command = input("Your choice: ")
        return command

    def print_result(self, result):
        if isinstance(result, str):
            print(result)
        else:
            print("The result is:")
            for row in result:
                print(*row, sep=' ')
            print()


if __name__ == '__main__':
    UserInterface()
