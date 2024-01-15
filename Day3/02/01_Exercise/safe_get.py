"""
05_Day_3 - 02_Error_handling - 01_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function named `safe_get` which takes two parameters:

* `l`: any list,
* `index`: number.

The function should return the element of the list that has the given `index`. If there is no such element,
it should return `None`.

**Note:** do this using exception handling.
"""


def safe_get(l, index):
    try:
        return l[index]
    except IndexError:
        return None


a = [0, 1, 2, 3]
print(safe_get(a, 1))
print(safe_get(a, 10))
