"""
Workshop_01 - Program_05
----
Dice
----
(c) Tomas Dolejsek 2024-01-28

Board games and pen-and-paper RPG games use many types of dice, not just the well-known cubic ones.
One of the most popular dice are, for example, a ten-sided one or even a hundred-sided one! Since dice are often tossed
in games, writing "e.g. roll two ten-sided dice and add 20 to the result" each time would be boring, difficult,
and wasting huge amounts of paper. In such situations, the code "roll 2D10+20" is used.

The code for such a die has the following formula: xDy+z
where:
    * y – type of dice to use (e.g. D6, D10),
    * x – number of dice rolled; for a single roll this parameter is omitted,
    * z – modifier - number to add (or subtract) to the result of the roll (optional).

Examples:

2D10+10: roll 2 D10 dice, add 10 to the result,
D6: a single roll of a cubic die,
2D3: roll 2 three-sided dice,
D12-1: roll one D12 die, subtract 1 from the result.
Write a function that will:

take such code as a string in the parameter,
recognize all input data:
    * type of dice,
    * number of rolls,
    * modifier,
return an appropriate message if the given string is invalid,
simulate the rolls and return the result.
Types of dice used in games: D3, D4, D6, D8, D10, D12, D20, D100.
"""

from random import randint
from collections import namedtuple
DiceRoll = namedtuple('DiceRoll', ['number', 'dice', 'modifier'])


def process_input(user):
    correct_dice = (3, 4, 6, 8, 10, 12, 20, 100)
    signs = ('+', '-')
    d_index = user.find('D')
    if d_index == -1:
        return False

    for sign in signs:
        mod_index = user.find(sign)
        if mod_index != -1:
            break
    if mod_index == -1:  # no modifier
        mod_index = len(user)

    rolls = user[:d_index]  # everything before 'D' means number of rolls
    dice = user[d_index + 1:mod_index]  # type of dice
    modifier = user[mod_index:]
    try:
        rolls = int(rolls) if rolls else 1
        dice = int(dice)
        modifier = int(modifier) if modifier else 0
        if dice not in correct_dice:
            return False
    except ValueError:
        return False

    return DiceRoll(rolls, dice, modifier)


def calculate_roll(roll):
    suma = roll.modifier
    print("Rolls: ", end='')
    for _ in range(roll.number):
        x = randint(1, roll.dice)
        print(f"{x} ", end='')
        suma += x
    return suma


def main():
    roll = False
    while not roll:
        user = input("Enter roll in a form xDy+z: ").upper()
        roll = process_input(user)
        if not roll:
            print("Incorrect input!")
    print(f"\nThe result of a {user} dice roll is: {calculate_roll(roll)}")


if __name__ == '__main__':
    main()
