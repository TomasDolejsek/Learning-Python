import numpy as np
import numpy.linalg as la
from io import StringIO


class PageRank:
    def __init__(self):
        self.L = np.array([[0, 1/2, 1/3, 0, 0, 0],
                           [1/3, 0, 0, 0, 1/2, 0],
                           [1/3, 1/2, 0, 1, 0, 1/2],
                           [1/3, 0, 1/3, 0, 1/2, 1/2],
                           [0, 0, 0, 0, 0, 0],
                           [0, 0, 1/3, 0, 0, 0]])
        self.USERS = 100
        self.start()

    @property
    def nsites(self):
        return len(self.L)

    def start(self):
        r = self.USERS * np.ones(self.nsites) / self.nsites
        r = self.L @ r
        self.display(r)
        for i in range(10):
            r = self.L @ r
        self.display(r)
        r_prev = r
        while True:
            r = self.L @ r
            if la.norm(r_prev - r) < 0.01:
                break
            r_prev = r
        self.display(r)

    @staticmethod
    def display(matrix):
        s = StringIO()
        np.savetxt(s, matrix, fmt='%.3f')
        print(s.getvalue())

    def get_eigs(self, matrix):
        e_vals, e_vecs = la.eig(matrix)
        vec = np.transpose(e_vecs)[0]
        return [(x * self.USERS / sum(vec)).real for x in vec]


if __name__ == '__main__':
    PageRank()
