"""
Workshop_01 - Program_02
---------------
LOTTO Simulator
---------------
(c) Tomas Dolejsek 2024-01-28

LOTTO is a numeric game that involves drawing 6 numbers from the range of 1 – 49. The player's task is to correctly
guess the drawn numbers. You are rewarded if you correctly match 3, 4, 5 or 6 numbers.

Write a program that:

1. asks user to select 6 numbers, while checking the following conditions:
    - whether the string entered is a valid number,
    - whether the user has not entered a given number before,
    - if the number is in the range of 1-49,
2. after entering 6 numbers, sorts them in ascending order and displays them on the screen,
3. draws 6 numbers from the range and displays them on the screen,
4. informs the player how many numbers they have matched.
"""

from random import shuffle


class InvalidNumberError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_numbers():
    n = 0
    numbers = []
    while n < 6:
        try:
            number = int(input(f"Enter {n + 1}. number (1 - 49): "))
            if not (1 <= number <= 49):
                raise InvalidNumberError("The number is out of range! Try again.")
            if number in numbers:
                raise InvalidNumberError("You've already picked that number! Try again.")
            numbers.append(number)
            n += 1
        except ValueError:
            print("That's not a number! Try again.")
        except InvalidNumberError as e:
            print(e)
    return numbers


def lotto_picks():
    numbers = list(range(1, 50))
    shuffle(numbers)
    return numbers[:6]


def main():
    player = sorted(get_numbers())
    computer = sorted(lotto_picks())
    correct = 0
    for num in player:
        if num in computer:
            correct += 1
    print(f"\nYou have picked these numbers: {' - '.join(map(str, player))}")
    print(f"Computer picked these numbers: {' - '.join(map(str, computer))}")
    print(f"You correctly picked {correct} number{'s' if correct != 1 else ''}.")


if __name__ == '__main__':
    main()
