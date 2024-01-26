"""
Workshop_01 - Program_01
--------------------
Number Guessing Game
--------------------
(c) Tomas Dolejsek 2024-01-28

Write a simple number guessing game. The computer must draw a number in the range 1 – 100. Then it should:

1. Ask: "Guess the number: " and retrieve the number from the keyboard.
2. Check whether it is really a number and in case of an error display the message "It's not a number!",
and then return to point 1.
3. If the number entered by the user is smaller than the drawn number, display the message "Too small!",
and return to point 1.
4. If the number entered by the user is greater than the drawn number, display the message "Too big!",
and then return to point 1.
5. If the number entered by the user is equal to the drawn number, display the message "You win!",
and then terminate the program.
"""

from random import randint


class OutOfRangeError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_number():
    while True:
        try:
            num = int(input("Guess a number (1 - 100): "))
            if not (1 <= num <= 100):
                raise OutOfRangeError("The number is out of range!")
            return num
        except ValueError:
            print("It's not a number!")
        except OutOfRangeError as e:
            print(e)


def main():
    picked_number = randint(1, 100)
    while True:
        number = get_number()
        if number < picked_number:
            print("To small!")
        elif number > picked_number:
            print("To big!")
        elif number == picked_number:
            print("You win!")
            break


if __name__ == "__main__":
    main()
