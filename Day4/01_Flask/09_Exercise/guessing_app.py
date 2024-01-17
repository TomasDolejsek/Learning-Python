"""
07_Day_4 - 01_Flask - 09_Exercise
(c) Tomas Dolejsek 2024-01-27

Write and run a simple guessing game that:
    * draws the correct answer,
    * asks the user - "Try to guess the number", displaying a form.
    * after submitting the form with the answer, prints on the screen:
        * "too little!" if the user's answer is less than the number; and the form for entering value again,
        * "too many!" if the user's answer is greater than the number; and the form for entering value again,
        * "Congratulations, you made it!" if the user guessed the number.
"""

from random import randint
from flask import Flask, request, render_template
app = Flask(__name__)


class OutOfRangeError(Exception):
    def __init__(self, message):
        super().__init__(message)


def get_number():
    while True:
        try:
            num = int(input("Guess a number (1 - 100): "))
            if not (1 <= num <= 100):
                raise OutOfRangeError
            return num
        except ValueError:
            return "That's not a number!"
        except OutOfRangeError:
            return "The number is out of range!"


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


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


if __name__ == '__main__':
    app.run()
