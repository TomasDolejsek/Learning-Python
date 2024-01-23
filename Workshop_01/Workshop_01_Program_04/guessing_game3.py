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


def evaluate_reply(answer):
    global low, high
    if answer == 'Too small!':
        low = guess
    elif answer == 'Too big!':
        high = guess
    return answer == 'You win!'


def reset_game():
    global low, high
    low, high = 1, 1000


@app.route("/", methods=['GET', 'POST'])
def index():
    global guess
    if request.method == 'GET':
        return render_template('index.html', display=None)
    if request.method == 'POST':
        answer = request.form.get('user_clicked')
        won = evaluate_reply(answer)
        if won:
            reset_game()
        guess = (high - low) // 2 + low if not won else 'won'
        return render_template('index.html', display=guess)


if __name__ == '__main__':
    low, high = 1, 1000
    guess = (high - low) // 2 + low
    app.run()
