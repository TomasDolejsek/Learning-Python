import numpy as np
import numpy.linalg as la
from io import StringIO


class PageRank:
    def __init__(self):
        self.start()

    def start(self):
        n = int(input())
        web_names = input().split()
        matrix = []
        for _ in range(n):
            line = input().split()
            line = [float(x) for x in line]
            matrix.append(line)
        L = np.array(matrix)
        query = input()
        ranks = self.page_rank(L)
        results = dict()
        for page, rank in zip(web_names, ranks):
            results[page] = rank
        results = dict(sorted(results.items(), key=lambda x: (x[1], x[0]), reverse=True))

        print(query)
        for i, name in enumerate(results.keys()):
            if i == 5:
                break
            if name == query:
                continue
            print(name)

    def page_rank(self, link_matrix, d=0.5, nusers=100, precision=0.01):
        n = len(link_matrix)
        M = self.damping_factor(link_matrix, d)
        r = nusers * np.ones(n) / n
        r_prev = r
        while True:
            r = M @ r
            if la.norm(r_prev - r) < precision:
                break
            r_prev = r
        return r

    @staticmethod
    def display(matrix):
        s = StringIO()
        np.savetxt(s, matrix, fmt='%.3f')
        print(s.getvalue())

    @staticmethod
    def damping_factor(matrix, d):
        n = len(matrix)
        J = np.ones((n, n))
        M = d * matrix + ((1 - d) / n) * J
        return M


if __name__ == '__main__':
    PageRank()
