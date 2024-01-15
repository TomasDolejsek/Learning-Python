"""
06_Day_3_-_homework - 02_Exercise
(c) Tomas Dolejsek 2024-01-27

Write a function named `div` that:

* asks the user to enter 2 numbers from the keyboard,
* converts the entered data into natural numbers,
* divides one number by the other,
* displays the result.

Additionally, you should protect against all possible errors (incorrect data, division by zero).
"""


def div():
    try:
        num1, num2 = input("Enter two numbers: ").split()
        print(int(num1) / int(num2))
    except ZeroDivisionError:
        print("Division by zero!")
    except ValueError:
        print("Incorrect input, enter two numbers, please.")


if __name__ == '__main__':
    div()
