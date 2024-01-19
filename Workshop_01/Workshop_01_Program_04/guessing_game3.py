"""
Workshop_01 - Program_04
----------------------
Number Guessing Game 3
----------------------
(c) Tomas Dolejsek 2024-01-15

Implement a reverse number guessing game in a web application using the Flask framework.
The user is given a form with three buttons: Too small, Too big, You win.

Store information about the current variables min and max in hidden form fields (field of the hidden type).
"""

from flask import Flask, request, render_template
app = Flask(__name__)


def evaluate_reply(answer, guess, high, low):
    global won
    if answer == 'too big':
        high = guess
    elif answer == 'too small':
        low = guess
    elif answer == 'you win':
        won = True
    return high, low


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/game", methods=['GET', 'POST'])
def game():
    global min, max, won
    if request.method == 'GET':
        render_template('game.html', guess=[(max - min) // 2 + min), won]
    if request.method == 'POST':
        reply = request.form['reply']
        min, max = evaluate_reply(reply, guess)
        guess = [(max - min) // 2 + min)
        render_template('index.html', guess=


if __name__ == '__main__':
    min, max = 1, 1000
    won = False
    
    app.run()
