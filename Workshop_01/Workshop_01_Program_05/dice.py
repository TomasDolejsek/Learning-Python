"""
Workshop_01 - Program_05
----
Dice
----
(c) Tomas Dolejsek 2024-01-23

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
DiceRoll = namedtuple('DiceRoll', ['amount', 'dice', 'modifier'])


def process_input(user):
    correct_dices = (3, 4, 6, 8, 10, 12, 20, 100)

    if 'D' not in user:
        return False
    try:
        d_split = user.split('D')
        rolls = int(d_split[0]) if d_split[0] else 1

        if '+' in d_split[-1]:
            mod_split = d_split[-1].split('+')
            modifier = int(mod_split[-1])
        elif '-' in d_split[-1]:
            mod_split = d_split[-1].split('-')
            modifier = -int(mod_split[-1])
        else:
            mod_split = d_split[-1]
            modifier = 0

        dice = int(mod_split[0])
        if dice not in correct_dices:
            return False

    except ValueError:
        return False

    return DiceRoll(rolls, dice, modifier)


def calculate_roll(roll):
    suma = 0
    for _ in range(roll.amount):
        x = randint(1, roll.dice)
        print(x)
        suma += x
    suma += roll.modifier
    return suma


def main():
    roll = False
    while not roll:
        user = input("Enter roll in a form xDy+z: ").upper()
        roll = process_input(user)
        if not roll:
            print("Incorrect input!")
    print(f"The result of a {user} dice roll is: {calculate_roll(roll)}")

if __name__ == '__main__':
    main()
