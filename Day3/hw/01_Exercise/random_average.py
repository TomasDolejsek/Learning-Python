"""
06_Day_3_-_homework - 01_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function `random_average(n)` that draws `n` natural numbers from 1 to 100, sums them,
and returns the arithmetic mean of these numbers.
"""

import random


def random_average(n):
    suma = 0
    for _ in range(n):
        suma += random.randint(1, 100)
    return suma / n


if __name__ == '__main__':
    a = 10
    print(random_average(a))
