"""
Workshop_01 - Program_04
----------------------
Number Guessing Game 2
----------------------
(c) Tomas Dolejsek 2024-01-15

Implement a reverse number guessing game in a web application using the Flask framework.
The user is given a form with three buttons: Too small, Too big, You win.

Store information about the current variables min and max in hidden form fields (field of the hidden type).
"""

from flask import Flask

app = Flask(__name__)


def player_input():
    answers = ('too big', 'too small', 'you win')
    while True:
        print(f"Possible answers: {' - '.join(answers)}")
        player = input()
        if player not in answers:
            print("I don't understand. Please enter one of the possible answers.")
            continue
        return player


@app.route("/")
def main():
    limit = 1000
    print(f"Think about a number from 0 to {limit} and let me guess it!")
    low, high = 1, limit
    attempts = 0
    while True:
        guess = (high - low) // 2 + low
        attempts += 1
        print(f"Attempt no. {attempts}, guessing {guess}. How did I do?")
        answer = player_input()
        if answer == 'too big':
            high = guess
        elif answer == 'too small':
            low = guess
        elif answer == 'you win':
            break
    print(f"I won! And I needed only {attempts} attempt{'s' if attempts > 1 else ''}!")


if __name__ == '__main__':
    app.run()
