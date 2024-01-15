"""
05_Day_3 - 02_Error_handling - 02_Exercise
(c) Tomas Dolejsek 2024-01-27

In the file **exercise2.py** you will find a simple guessing game: the computer draws a number from 1 to 10, then tells
you to guess it. Analyse the code. Run the program. Try to enter an incorrect number and see how the program behaves in
this situation.

Improve the code so that it does not terminate with an error message after entering an incorrect value, but informs
the user about the error and continues its operation.

**Hint: See what exception is reported and handle it appropriately.**
"""

from random import randint

guessed = False
rnd = randint(1, 10)

while not guessed:
    str_num = input("Enter number (1 - 10): ")
    try:
        num = int(str_num)
        if not (1 <= num <= 10):
            raise ValueError
        if num == rnd:
            print("Great!")
            guessed = True
        else:
            print("Wrong!")
    except ValueError:
        print("Incorrect input! Please enter a number 1 - 10.")
