"""
05_Day_3 - 02_Error_handling - 03_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function named `divide` that takes two arguments: `a` and `b`. They must be natural numbers.
The function has to:

* check if `a` and `b` are numbers,
* handle the problem of dividing by zero.

Both of the above cases must be handled by exception catching.

If either of the above (invalid) cases is not satisfied, the function should return `None`.
"""


def divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Division by zero!")
    except TypeError:
        print("Enter only numbers!")


number1 = 10
number2 = 0
print(divide(number1, number2))
