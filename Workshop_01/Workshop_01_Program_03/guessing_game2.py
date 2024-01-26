"""
Workshop_01 - Program_03
----------------------
Number Guessing Game 2
----------------------
(c) Tomas Dolejsek 2024-01-15

The user should think of a number between 1 and 1000, and the computer should guess it. The computer
will do it in no more than 10 moves (provided that the player is not cheating).

The player's task will be to give appropriate answers: "Too small", "Too big", "You win".
"""


def player_input():
    answers = ('too big', 'too small', 'you win')
    while True:
        print(f"Possible answers: {' - '.join(answers)}")
        player = input()
        if player not in answers:
            print("I don't understand. Please enter one of the possible answers.")
            continue
        return player


def main():
    limit = 1000
    print(f"Think about a number from 1 to {limit} and let me guess it!")
    low, high = 1, limit
    attempts = 0
    while True:
        guess = (high - low) // 2 + low
        attempts += 1
        print(f"Attempt no. {attempts}, guessing {guess}.")
        answer = player_input()
        if answer == 'too big':
            high = guess
        elif answer == 'too small':
            low = guess
        elif answer == 'you win':
            break
    print(f"I won! And I needed only {attempts} attempt{'s' if attempts > 1 else ''}!")


if __name__ == '__main__':
    main()
