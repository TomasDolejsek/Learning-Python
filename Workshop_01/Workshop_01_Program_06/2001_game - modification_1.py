"""
Workshop_01 - Program_05_Mod_1
--------------------------
2001 Game - Modification_1
--------------------------
(c) Tomas Dolejsek 2024-01-24

*** Modification 1 ***
You've probably noticed that the current version of the game isn't very interactive, and it's all about clicking
the enter key. Let's try to make it a little more interactive.
    * Before each throw, give the player a choice.
    * Let them choose 2 dice from the following: D3, D4, D6, D8, D10, D12, D20, D100.
    * The player may use 2 dice of the same kind, or 2 different dice.
    * Let the choice of dice be made by the player by entering the appropriate string (one for each die).
    * You can use the code from the Dice task.
    * The computer's choice of dice should be random.

The rest of the rules remain the same.
"""

from random import randint, choice


def calculate_roll(who, rolls):
    print(f"\n{who} picked D{rolls[0]} and D{rolls[1]}.")
    print(f"{who}'s rolls: ", end='')
    x = randint(1, rolls[0])
    y = randint(1, rolls[1])
    print(f"{x} + {y} = {x + y}")
    return x + y


def calculate_score(points, roll, round_number):
    if round_number == 1:
        return points + roll
    if roll == 7:
        print("Points divided by 7!")
        return points // 7
    elif roll == 11:
        print("Points multiplied by 11!")
        return points * 11
    else:
        return points + roll


def validate_dice(dice):
    correct_dice = (3, 4, 6, 8, 10, 12, 20, 100)
    if len(dice) != 2:
        return False
    try:
        for d in dice:
            if int(d) not in correct_dice:
                return False
    except ValueError:
        return False
    return tuple(map(int, dice))


def pick_computer_dice():
    correct_dice = (3, 4, 6, 8, 10, 12, 20, 100)
    x = choice(correct_dice)
    y = choice(correct_dice)
    return x, y


def pick_player_dice():
    dice = False
    while not dice:
        print("Which dice do you want to use for this round?")
        print("Available dice are: D3, D4, D6, D8, D10, D12, D20, D100")
        print("Enter two numbers divided by SPACE: ", end='')
        dice = validate_dice(input().split())
        if not dice:
            print("Invalid input!")
    return dice


def main():
    LIMIT = 2001
    score = {'Player': 0,
             'Computer': 0}
    rolls = {'Player': [],
             'Computer': []}
    round_number = 0
    winner = False
    print(f"Welcome to {LIMIT} game!")
    while not winner:
        round_number += 1
        print(f"\nRound no. {round_number}:")
        rolls['Player'] = pick_player_dice()
        rolls['Computer'] = pick_computer_dice()

        for member in score:
            roll = calculate_roll(member, rolls[member])
            score[member] = calculate_score(score[member], roll, round_number)
            print(f"{member} score: {score[member]}")
            if score[member] >= LIMIT:
                print(f"\n{member} WINS!")
                winner = True
                break


if __name__ == '__main__':
    main()
