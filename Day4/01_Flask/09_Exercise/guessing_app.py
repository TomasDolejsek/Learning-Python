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
    def __init__(self):
        super().__init__()


def get_result(num, picked):
    while True:
        try:
            num = int(num)
            if not (1 <= num <= 100):
                raise OutOfRangeError
            return validate_number(num, picked)
        except ValueError:
            return "That's not a number!"
        except OutOfRangeError:
            return "The number is out of range!"


def validate_number(number, picked_number):
    if number < picked_number:
        return "To small!"
    elif number > picked_number:
        return "To big!"
    elif number == picked_number:
        return "You win!"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        picked_number = randint(1, 100)
        return render_template('index.html', secret_number=picked_number, result=None)
    if request.method == 'POST':
        guess = request.form['number']
        picked_number = int(request.form['secret_number'])
        result = get_result(guess, picked_number)
        return render_template('index.html', number=guess, secret_number=picked_number, result=result)


if __name__ == '__main__':
    app.run()
