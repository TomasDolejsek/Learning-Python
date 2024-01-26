"""
Workshop_01 - Program_04
----------------------
Number Guessing Game 3
----------------------
(c) Tomas Dolejsek 2024-01-28

Implement a reverse number guessing game in a web application using the Flask framework.
The user is given a form with three buttons: Too small, Too big, You win.

Store information about the current variables min and max in hidden form fields (field of the hidden type).
"""

from flask import Flask, request, render_template
from collections import namedtuple
app = Flask(__name__)
Guess = namedtuple('GuessData', ['answer', 'guess', 'min', 'max'])


def evaluate_reply(data):
    low = data.min
    high = data.max
    if data.answer == 'Too small!':
        low = data.guess
    elif data.answer == 'Too big!':
        high = data.guess
    new_guess = (high - low) // 2 + low
    if data.answer == 'You win!':
        new_guess = 'win'
    return Guess(data.answer, new_guess, low, high)


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', guess=500, min=1, max=1000)
    if request.method == 'POST':
        answer = request.form.get('user_clicked')
        low = int(request.form.get('min'))
        high = int(request.form.get('max'))
        guess = int(request.form.get('guess'))
        data = Guess(answer, guess, low, high)
        new_data = evaluate_reply(data)
        if new_data.guess == 'win':
            return render_template('win.html', guess=500, min=1, max=1000)
        else:
            return render_template('game.html', guess=new_data.guess, min=new_data.min, max=new_data.max)


if __name__ == '__main__':
    app.run()
